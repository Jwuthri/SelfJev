#!/usr/bin/env bash
# usage: [SPOT=1] scripts/aws/aws_launch.sh NAME HOURS "REGION:TYPE ..." -> launches in the first REGION:TYPE with capacity (default VPC).
#   e.g. scripts/aws/aws_launch.sh selfjev-jev-soft 5 "us-east-2:g6e.2xlarge us-east-1:g6e.2xlarge us-west-2:g6e.2xlarge"
# AGENTS.md conventions: tags Name/Project=personal-jev, SSH-only security group from this machine's IP, own key pair
# (~/.ssh/NAME-REGION.pem), `shutdown -h +HOURS*60` in user data with terminate-on-shutdown as the cost cap.
# State: runs/aws/NAME.instance ("id type region") and runs/aws/NAME-REGION.sg. When done, clean up:
#   aws ec2 terminate-instances --instance-ids ID; aws ec2 wait instance-terminated --instance-ids ID
#   aws ec2 delete-security-group --group-id SG; aws ec2 delete-key-pair --key-name NAME; rm ~/.ssh/NAME-REGION.pem
set -uo pipefail
SP=runs/aws; NAME=$1; HOURS=$2; CANDIDATES=$3
mkdir -p $SP
export AWS_PROFILE=connectly
TAGS="{Key=Name,Value=$NAME},{Key=Project,Value=personal-jev},{Key=Owner,Value=julien}"
MYIP=$(curl -s https://checkip.amazonaws.com)
UD=$(printf '#!/bin/bash\n# cost cap: power off (=> terminate) after %s hours no matter what\nshutdown -h +%s\n' $HOURS $((HOURS * 60)) | base64)
umask 077
MARKET=(); [[ -n ${SPOT:-} ]] && MARKET=(--instance-market-options 'MarketType=spot,SpotOptions={SpotInstanceType=one-time,InstanceInterruptionBehavior=terminate}')
for C in $CANDIDATES; do
  REGION=${C%%:*}; TYPE=${C##*:}; export AWS_DEFAULT_REGION=$REGION
  VPC=$(aws ec2 describe-vpcs --filters Name=is-default,Values=true --query 'Vpcs[0].VpcId' --output text)
  [[ -f ~/.ssh/$NAME-$REGION.pem ]] || aws ec2 create-key-pair --key-name $NAME --key-type ed25519 --tag-specifications "ResourceType=key-pair,Tags=[$TAGS]" --query KeyMaterial --output text > ~/.ssh/$NAME-$REGION.pem
  SG=$(cat "$SP/$NAME-$REGION.sg" 2>/dev/null) || {
    SG=$(aws ec2 create-security-group --group-name $NAME-ssh --description "$NAME GPU box: SSH from one IP only" --vpc-id $VPC --tag-specifications "ResourceType=security-group,Tags=[$TAGS]" --query GroupId --output text)
    aws ec2 authorize-security-group-ingress --group-id $SG --protocol tcp --port 22 --cidr $MYIP/32 > /dev/null
    echo "$SG" > "$SP/$NAME-$REGION.sg"; }
  AMI=$(aws ssm get-parameter --name /aws/service/deeplearning/ami/x86_64/base-oss-nvidia-driver-gpu-ubuntu-22.04/latest/ami-id --query Parameter.Value --output text)
  for SUB in $(aws ec2 describe-subnets --filters Name=vpc-id,Values=$VPC --query 'Subnets[].SubnetId' --output text); do
    OUT=$(aws ec2 run-instances --image-id $AMI --instance-type $TYPE --key-name $NAME --security-group-ids $SG --subnet-id $SUB --associate-public-ip-address --count 1 ${MARKET[@]+"${MARKET[@]}"} --instance-initiated-shutdown-behavior terminate --user-data "$UD" --block-device-mappings 'DeviceName=/dev/sda1,Ebs={VolumeSize=250,VolumeType=gp3,DeleteOnTermination=true}' --tag-specifications "ResourceType=instance,Tags=[$TAGS]" "ResourceType=volume,Tags=[$TAGS]" --query 'Instances[0].InstanceId' --output text 2>&1)
    if [[ $OUT == i-* ]]; then echo "LAUNCHED $REGION $TYPE $SUB $OUT at $(date +%H:%M)"; echo "$OUT $TYPE $REGION" > "$SP/$NAME.instance"; exit 0; fi
    echo "  $REGION $TYPE $SUB: $(echo "$OUT" | grep -oE 'InsufficientInstanceCapacity|MaxSpotInstanceCountExceeded|SpotMaxPriceTooLow|Unsupported|VcpuLimitExceeded|An error occurred \([A-Za-z]+\)' | head -1)"
  done
done
exit 1
