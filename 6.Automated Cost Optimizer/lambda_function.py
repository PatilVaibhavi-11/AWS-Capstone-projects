from datetime import datetime, timedelta
import boto3

ec2 = boto3.client('ec2')
cloudwatch = boto3.client('cloudwatch')

def lambda_handler(event, context):
    
    instances = ec2.describe_instances()

    for reservation in instances['Reservations']:
        for instance in reservation['Instances']:
            
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            
            if state != 'running':
                continue

            # Get CPU utilization
            metrics = cloudwatch.get_metric_statistics(
                Namespace='AWS/EC2',
                MetricName='CPUUtilization',
                Dimensions=[
                    {'Name': 'InstanceId', 'Value': instance_id}
                ],
                StartTime=datetime.utcnow() - timedelta(minutes=10),
                EndTime=datetime.utcnow(),
                Period=300,
                Statistics=['Average']
            )

            if metrics['Datapoints']:
                avg_cpu = metrics['Datapoints'][0]['Average']
                
                print(f"{instance_id} CPU: {avg_cpu}")

                if avg_cpu < 5:
                    print(f"Stopping instance {instance_id}")
                    ec2.stop_instances(InstanceIds=[instance_id])

    return "Done"