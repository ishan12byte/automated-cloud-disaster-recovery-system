# Recovery Time Objective (RTO) Report

## Project Name

Automated Cloud Disaster Recovery System

## Objective

Measure the time required to restore service after a failure event.

## Failure Scenario

The primary EC2 instance was intentionally stopped to validate the disaster recovery workflow.

## Recovery Workflow

Primary EC2
↓
CloudWatch Alarm / EventBridge
↓
AWS Lambda
↓
Recovery EC2 Launch
↓
SNS Notification

## Test Results

| Parameter | Observation |
|---|---|
| Monitoring Service | CloudWatch |
| State Recovery | EventBridge |
| Recovery Engine | AWS Lambda |
| Notification Service | Amazon SNS |
| Backup Method | AMI |
| Recovery Status | Successful |

## Observed RTO

Failure Detection Time:
2026-06-09 XX:XX:XX

Recovery Completion Time:
2026-06-09 XX:XX:XX

Observed Infrastructure RTO:
17.14 seconds

## Notes

The measured RTO represents infrastructure recovery time until the recovery EC2 instance entered the running state. Application-level availability may vary depending on initialization time.

## Conclusion

The disaster recovery workflow successfully restored infrastructure automatically and generated RTO metrics through Lambda execution.
