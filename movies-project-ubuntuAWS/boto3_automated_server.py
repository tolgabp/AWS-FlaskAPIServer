import boto3 , os

key_path = '/Users/mikeyang/Desktop/Cloud_Based/cctkey1.pem'
sec_gr = 'sg-046122f5e215dc6b8'
ami_id = 'ami-0499632f10efc5a62'
region = 'eu-central-1'
tag_name = {"Key": "Name", "Value": "mk-python-server"}

client = boto3.client('ec2', region_name=region)

response = client.run_instances(
    BlockDeviceMappings=[
        {
            'DeviceName': '/dev/sda1',
            'Ebs': {
                'DeleteOnTermination': True,
                'VolumeSize': 8,
                'VolumeType': 'gp2'
            },
        },
    ],
    ImageId=ami_id,
    InstanceType='t3.micro',
    KeyName=os.path.basename(key_path).split('.')[0],
    MaxCount=1,
    MinCount=1,
    UserData='''#!/bin/bash
    yum update -y
    yum -y install httpd
    systemctl start httpd.service
    systemctl enable httpd.service
    echo Hello > /var/www/html/index.html    
    ''',
    Monitoring={
        'Enabled': False
    },
    SecurityGroupIds=[
        sec_gr,
    ],
    TagSpecifications=[{'ResourceType': 'instance',
                        'Tags': [tag_name]}]
)

instid = response['Instances'][0]['InstanceId']
print(instid)
