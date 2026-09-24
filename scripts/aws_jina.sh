#!/usr/bin/env bash
# One GPU box for the jina run: launch | run | log | pull | terminate. State: reports/jina_r2b/aws.json.
# Conventions: SSH-only SG from this machine's /32, own key pair, user-data auto-shutdown (terminate), tags Name/Project,
# everything deleted by `terminate`. Never touches other instances.
set -euo pipefail
export AWS_PROFILE=connectly AWS_DEFAULT_REGION=us-east-1
NAME=selfjev-jina-20260924; TYPE=${TYPE:-g5.xlarge}; ST=reports/jina_r2b/aws.json; PEM=$HOME/.ssh/$NAME.pem
SSH="ssh -i $PEM -o StrictHostKeyChecking=no -o UserKnownHostsFile=/dev/null -o LogLevel=ERROR"
mkdir -p reports/jina_r2b
ip() { python3 -c "import json; print(json.load(open('$ST'))['ip'])"; }
case ${1:-} in
launch)
  [ -f $ST ] && { echo "state file exists: $ST (terminate first)"; exit 1; }
  AMI=$(aws ssm get-parameter --name /aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-gpu-ubuntu-22.04/latest/ami-id --query Parameter.Value --output text)
  VPC=$(aws ec2 describe-vpcs --filters Name=isDefault,Values=true --query 'Vpcs[0].VpcId' --output text)
  SG=$(aws ec2 create-security-group --group-name $NAME --description "$NAME ssh only" --vpc-id $VPC --query GroupId --output text)
  aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 22 --cidr "$(curl -4 -s ifconfig.me)/32" > /dev/null
  aws ec2 create-key-pair --key-name $NAME --query KeyMaterial --output text > $PEM && chmod 600 $PEM
  ID=""
  for AZ in us-east-1a us-east-1b us-east-1c us-east-1d us-east-1f; do
    SUBNET=$(aws ec2 describe-subnets --filters Name=default-for-az,Values=true Name=availability-zone,Values=$AZ --query 'Subnets[0].SubnetId' --output text)
    [ "$SUBNET" = "None" ] && continue
    if ID=$(aws ec2 run-instances --image-id "$AMI" --instance-type "$TYPE" --key-name $NAME --subnet-id "$SUBNET" --security-group-ids "$SG" \
          --associate-public-ip-address --instance-initiated-shutdown-behavior terminate --user-data "#!/bin/bash
shutdown -h +${SHUTDOWN_MIN:-360}" \
          --block-device-mappings '[{"DeviceName":"/dev/sda1","Ebs":{"VolumeSize":120,"VolumeType":"gp3","DeleteOnTermination":true}}]' \
          --tag-specifications "ResourceType=instance,Tags=[{Key=Name,Value=$NAME},{Key=Project,Value=personal-jev}]" \
          --query 'Instances[0].InstanceId' --output text 2> /tmp/aws_jina_err); then
      echo "launched $ID in $AZ ($TYPE)"; break
    elif grep -q InsufficientInstanceCapacity /tmp/aws_jina_err; then echo "no $TYPE capacity in $AZ"; ID=""
    else cat /tmp/aws_jina_err; exit 1; fi
  done
  [ -n "$ID" ] || { echo "no capacity in any AZ; SG $SG and key $NAME left for a retry (terminate cleans them)"; echo "{\"sg\": \"$SG\"}" > $ST; exit 1; }
  aws ec2 wait instance-running --instance-ids "$ID"
  IP=$(aws ec2 describe-instances --instance-ids "$ID" --query 'Reservations[0].Instances[0].PublicIpAddress' --output text)
  echo "{\"instance_id\": \"$ID\", \"ip\": \"$IP\", \"sg\": \"$SG\", \"type\": \"$TYPE\", \"launched_utc\": \"$(date -u +%FT%TZ)\"}" > $ST
  cat $ST ;;
run)
  IP=$(ip); until $SSH ubuntu@$IP true 2> /dev/null; do sleep 10; done
  rsync -az --delete -e "$SSH" --exclude .venv --exclude runs --exclude reports --exclude .git --exclude docs --exclude 'data/*/' \
    --exclude '__pycache__' ./ ubuntu@$IP:SelfJev/
  $SSH ubuntu@$IP 'cd SelfJev && mkdir -p runs reports calib && nohup bash scripts/run_jina_gpu.sh > run_jina.log 2>&1 < /dev/null &'
  echo "started on $IP" ;;
log) $SSH ubuntu@$(ip) 'tail -n ${N:-40} SelfJev/run_jina.log' ;;
pull)
  IP=$(ip)
  rsync -az -e "$SSH" ubuntu@$IP:SelfJev/runs/jina_r2b ./runs/ 2> /dev/null || true
  rsync -az -e "$SSH" ubuntu@$IP:SelfJev/runs/jina_r2b.log ./runs/ 2> /dev/null || true
  rsync -az -e "$SSH" ubuntu@$IP:SelfJev/reports/jina_r2b ubuntu@$IP:SelfJev/reports/jina_zeroshot ./reports/ 2> /dev/null || true
  rsync -az -e "$SSH" ubuntu@$IP:SelfJev/calib/jina_r2b.json ./calib/ 2> /dev/null || true
  rsync -az -e "$SSH" ubuntu@$IP:SelfJev/run_jina.log ./reports/jina_r2b/box_run.log 2> /dev/null || true
  echo pulled ;;
terminate)
  ID=$(python3 -c "import json; print(json.load(open('$ST')).get('instance_id',''))"); SG=$(python3 -c "import json; print(json.load(open('$ST'))['sg'])")
  [ -n "$ID" ] && { aws ec2 terminate-instances --instance-ids "$ID" > /dev/null; aws ec2 wait instance-terminated --instance-ids "$ID"; echo "terminated $ID"; }
  aws ec2 delete-security-group --group-id "$SG" && echo "deleted SG $SG"
  aws ec2 delete-key-pair --key-name $NAME && rm -f $PEM && echo "deleted key $NAME"
  mv $ST reports/jina_r2b/aws_done.json ;;
*) echo "usage: $0 launch|run|log|pull|terminate"; exit 1 ;;
esac
