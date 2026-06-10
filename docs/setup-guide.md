# Setup Guide

## AWS Services Used

- Amazon EC2
- AWS Lambda
- Amazon CloudWatch
- Amazon EventBridge
- Amazon SNS
- Amazon Machine Images (AMI)
- Amazon EBS Snapshots

## Deployment Steps

1. Launch the primary EC2 instance hosting the web application.
2. Install and configure Apache on the primary instance.
3. Create an EBS snapshot and AMI backup.
4. Replicate the AMI to a secondary AWS region.
5. Configure CloudWatch alarms for EC2 health monitoring.
6. Configure EventBridge rules for EC2 state-change recovery.
7. Deploy the Lambda recovery function.
8. Configure SNS email notifications.
9. Simulate failure conditions.
10. Validate automated recovery and observe Recovery Time Objective (RTO).
