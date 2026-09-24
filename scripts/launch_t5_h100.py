"""Launch the authorized conditional H100 comparison, reusing this job's Ohio SG/key.

The encoder-target correction also authorizes using this host for the corrected training run. Failed capacity attempts do not
create resources; ambiguous failures stop instead of trying another AZ.
"""
import base64,json,subprocess
from pathlib import Path
ROOT=Path('reports/t5_round2b_2026-09-24')
REGION='us-east-2';NAME='selfjev-t5-r2b-h100-20260924'
def aws(*a):
    p=subprocess.run(['aws',*a,'--region',REGION,'--output','json','--no-cli-pager'],capture_output=True,text=True)
    if p.returncode:raise RuntimeError(p.stderr.strip())
    return json.loads(p.stdout or '{}')

def main():
    output=ROOT/'h100_cloud.json'
    if output.exists() and json.loads(output.read_text()).get('instance_id'):
        raise RuntimeError('An H100 instance is already recorded; inspect it instead of launching another')
    prior=json.loads((ROOT/'cloud_us-east-2.json').read_text());ami=json.loads((ROOT/'ami_ohio.json').read_text())
    subs=aws('ec2','describe-subnets','--filters','Name=default-for-az,Values=true')['Subnets']
    state={'region':REGION,'name':NAME,'instance_type':'p5.4xlarge','hourly_usd':6.88,'shutdown_hours':3,
           'shared_security_group':prior['security_group'],'shared_key_name':prior['key_name'],'attempts':[]}
    tags=[{'Key':'Name','Value':NAME},{'Key':'Project','Value':'personal-jev'},{'Key':'Experiment','Value':'t5-round2b-h100'}]
    for sub in sorted(subs,key=lambda x:x['AvailabilityZone']):
        az=sub['AvailabilityZone']
        request={'ImageId':ami['ImageId'],'InstanceType':'p5.4xlarge','MinCount':1,'MaxCount':1,'KeyName':prior['key_name'],
            'NetworkInterfaces':[{'DeviceIndex':0,'SubnetId':sub['SubnetId'],'Groups':[prior['security_group']],'AssociatePublicIpAddress':True}],
            'BlockDeviceMappings':[{'DeviceName':'/dev/sda1','Ebs':{'VolumeSize':200,'VolumeType':'gp3','DeleteOnTermination':True,'Encrypted':True}}],
            'MetadataOptions':{'HttpTokens':'required'},'InstanceInitiatedShutdownBehavior':'terminate',
            'UserData':base64.b64encode(b'#!/bin/bash\nset -eu\nshutdown -h +180\n').decode(),
            'TagSpecifications':[{'ResourceType':r,'Tags':tags} for r in ['instance','volume']],
            'ClientToken':NAME+'-'+az}
        path=ROOT/f'h100_launch_{az}.json';path.write_text(json.dumps(request,indent=2))
        try:
            r=aws('ec2','run-instances','--cli-input-json','file://'+str(path.resolve()))
            i=r['Instances'][0];state.update(instance_id=i['InstanceId'],launch_time=i['LaunchTime'],availability_zone=i['Placement']['AvailabilityZone'])
            (ROOT/'h100_launch_result.json').write_text(json.dumps(r,indent=2));output.write_text(json.dumps(state,indent=2));print(state,flush=True);return
        except RuntimeError as e:
            state['attempts'].append({'availability_zone':az,'error':str(e)});output.write_text(json.dumps(state,indent=2))
            if not any(s in str(e) for s in ['InsufficientInstanceCapacity','Unsupported']):raise
    print('No H100 capacity found; no H100 instance launched. Attempts recorded.',flush=True)
if __name__=='__main__':main()
