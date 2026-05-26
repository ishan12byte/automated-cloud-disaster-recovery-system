import boto3

def lambda_handler(event, context):

    print("Lambda started")

    ec2 = boto3.resource('ec2', region_name='eu-north-1')

    response = ec2.create_instances(
        ImageId='ami-042be8759132097a1',
        MinCount=1,
        MaxCount=1,
        InstanceType='t3.micro',
        KeyName='dr-keypair',
        SecurityGroupIds=['sg-0378df273cc0c3f7b'],
        SubnetId='YOUR_SUBNET_ID'
    )

    instance = response[0]

    print(f"Created instance: {instance.id}")

    return {
        'statusCode': 200,
        'body': f'Recovery instance launched: {instance.id}'
    }