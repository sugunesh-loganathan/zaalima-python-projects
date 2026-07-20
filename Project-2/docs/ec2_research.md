Amazon EC2 Research
1. What is Amazon EC2?

Amazon Elastic Compute Cloud (Amazon EC2) is a web service provided by Amazon Web Services (AWS) that allows users to launch virtual servers, known as EC2 instances, in the cloud. It enables scalable computing capacity without purchasing physical hardware.

2. Why is EC2 used?

EC2 is used for:

Hosting web applications
Running backend APIs
Machine Learning workloads
Data Processing
Testing and Development
Batch Jobs
3. Important EC2 Components
EC2 Instance

A virtual machine running in AWS.

Amazon Machine Image (AMI)

A template used to launch EC2 instances.

Instance Type

Defines CPU, Memory, Storage and Network capacity.

Examples:

t2.micro
t3.small
m5.large
Key Pair

Used for securely connecting to EC2 instances using SSH.

Security Group

Acts as a virtual firewall that controls inbound and outbound traffic.

Elastic IP

A static public IPv4 address that can be associated with an EC2 instance.

4. EC2 Instance States
Pending
Running
Stopping
Stopped
Shutting-down
Terminated
5. Common boto3 EC2 APIs
describe_instances()

run_instances()

start_instances()

stop_instances()

terminate_instances()

describe_instance_status()

describe_tags()
6. Information Required by Our Scanner

The EC2 Scanner should collect:

Instance ID
Instance Name
Instance Type
State
Launch Time
Public IP
Private IP
Elastic IP
Availability Zone
Region
Security Groups
Attached Volumes
Tags
7. Possible Future Checks

Our scanner may later detect:

Idle EC2 instances
Stopped instances
Unused instances
CPU Utilization