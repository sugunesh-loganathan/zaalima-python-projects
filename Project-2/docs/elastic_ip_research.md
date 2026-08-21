# Amazon Elastic IP Research

## 1. What is Amazon Elastic IP?

Amazon Elastic IP (EIP) is a static public IPv4 address provided by AWS. It can be associated with an EC2 instance and remains allocated to your AWS account until you release it.

Unlike a normal public IP address, an Elastic IP does not change when you stop and start an EC2 instance (if it remains associated).

---

## 2. Why is Elastic IP Used?

Elastic IPs are used for:

- Hosting websites
- Public APIs
- Remote access (SSH/RDP)
- Disaster recovery
- Static IP requirements

---

## 3. Key Concepts

### Elastic IP

A static public IPv4 address that belongs to your AWS account.

### Association

An Elastic IP can be associated with an EC2 instance or a network interface.

### Disassociation

An Elastic IP can be detached from an instance without being released.

### Release

Releasing an Elastic IP permanently returns it to AWS.

---

## 4. Common boto3 APIs

- describe_addresses()
- allocate_address()
- associate_address()
- disassociate_address()
- release_address()

---

## 5. Information Required by Our Scanner

The Elastic IP Scanner should collect:

- Allocation ID
- Association ID
- Public IP Address
- Associated EC2 Instance ID
- Network Interface ID
- Region
- Tags

---

## 6. Possible Cleanup Checks

The Cleanup Scanner may detect:

- Unassociated Elastic IPs
- Unused Elastic IPs
- Elastic IPs not attached to any EC2 instance

Unused Elastic IPs may incur AWS charges.

---

## 7. Scanner Design Notes

The Elastic IP Scanner will use the EC2 boto3 client.

Primary API:

- describe_addresses()

The scanner should return standardized information for every Elastic IP so that cleanup recommendations can be generated later.