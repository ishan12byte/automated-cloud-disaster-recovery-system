import boto3
import time
from datetime import datetime

# ==========================
# CONFIGURATION
# ==========================

SNS_TOPIC_ARN = "YOUR_AWS_ARN"

PRIMARY = {
    "region": "eu-north-1",
    "ami": "AMI_ID",
    "subnet": "PRIMARY_SUBNET_ID",
    "security_group": "SECURITY_GROUP_ID",
    "key_pair": "dr-keypair",
    "name": "Recovered-Server-Primary"
}

BACKUP = {
    "region": "ap-southeast-1",
    "ami": "BACKUP_AMI_ID",
    "subnet": "BACKUP_SUBNET_ID",
    "security_group": "BACKUP_SECURITY_GROUP_ID",
    "key_pair": "dr-keypair",
    "name": "Recovered-Server-Backup"
}

# Set to False if you don't want automatic cross-region failover
ENABLE_CROSS_REGION_FAILOVER = True


# ==========================
# HELPER FUNCTION
# ==========================

def launch_instance(config):
    """
    Launch EC2 instance using supplied configuration.
    """

    ec2_resource = boto3.resource(
        "ec2",
        region_name=config["region"]
    )

    ec2_client = boto3.client(
        "ec2",
        region_name=config["region"]
    )

    response = ec2_resource.create_instances(
        ImageId=config["ami"],
        MinCount=1,
        MaxCount=1,
        InstanceType="t3.micro",
        KeyName=config["key_pair"],
        SecurityGroupIds=[config["security_group"]],
        SubnetId=config["subnet"],
        TagSpecifications=[
            {
                "ResourceType": "instance",
                "Tags": [
                    {
                        "Key": "Name",
                        "Value": config["name"]
                    }
                ]
            }
        ]
    )

    instance = response[0]

    print(f"Recovery instance created: {instance.id}")

    waiter = ec2_client.get_waiter("instance_running")

    waiter.wait(
        InstanceIds=[instance.id]
    )

    return instance.id


# ==========================
# LAMBDA HANDLER
# ==========================

def lambda_handler(event, context):

    start_time = time.time()

    failure_detected = datetime.utcnow()

    sns = boto3.client(
        "sns",
        region_name=PRIMARY["region"]
    )

    print("===== DR WORKFLOW STARTED =====")
    print(f"Failure detected at: {failure_detected}")

    failover_type = "Primary Recovery"

    recovery_region = PRIMARY["region"]

    try:

        instance_id = launch_instance(PRIMARY)

    except Exception as e:

        print(f"Primary region recovery failed: {e}")

        if not ENABLE_CROSS_REGION_FAILOVER:
            raise

        failover_type = "Cross-Region Recovery"

        recovery_region = BACKUP["region"]

        instance_id = launch_instance(BACKUP)

    recovery_completed = datetime.utcnow()

    rto = round(
        time.time() - start_time,
        2
    )

    print(f"Recovery completed at: {recovery_completed}")
    print(f"Observed RTO: {rto} seconds")
    print(f"Recovery region: {recovery_region}")
    print(f"Failover type: {failover_type}")

    sns.publish(
        TopicArn=SNS_TOPIC_ARN,
        Subject="AWS Disaster Recovery Activated",
        Message=f"""
Disaster Recovery Report

Failure detected:
{failure_detected}

Recovery Instance:
{instance_id}

Recovery Region:
{recovery_region}

Failover Type:
{failover_type}

Recovery completed:
{recovery_completed}

Observed RTO:
{rto} seconds

Status:
Recovery Successful
"""
    )

    return {
        "statusCode": 200,
        "instance_id": instance_id,
        "recovery_region": recovery_region,
        "failover_type": failover_type,
        "rto_seconds": rto,
        "failure_detected": str(failure_detected),
        "recovery_completed": str(recovery_completed)
    }
