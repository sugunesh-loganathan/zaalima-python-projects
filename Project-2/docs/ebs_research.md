# Amazon EBS Research

## 1. What is Amazon EBS?

Amazon Elastic Block Store (Amazon EBS) is a block storage service provided by Amazon Web Services (AWS). It provides persistent storage volumes that can be attached to Amazon EC2 instances.

Unlike instance storage, data stored on EBS remains available even after the EC2 instance is stopped or restarted.

---

## 2. Why is Amazon EBS Used?

Amazon EBS is commonly used for:

- Operating system storage
- Application data
- Database storage
- File systems
- Backup storage
- Persistent application data

---

## 3. Key EBS Concepts

### EBS Volume

A virtual hard disk attached to an EC2 instance.

### Snapshot

A point-in-time backup of an EBS volume stored in Amazon S3.

### Availability Zone

An EBS volume can only be attached to an EC2 instance in the same Availability Zone.

### Volume Types

- gp3 (General Purpose SSD)
- gp2 (General Purpose SSD)
- io1 / io2 (Provisioned IOPS SSD)
- st1 (Throughput Optimized HDD)
- sc1 (Cold HDD)

---

## 4. Volume States

- Creating
- Available
- In-use
- Deleting
- Deleted

---

## 5. Common boto3 APIs

- describe_volumes()
- create_volume()
- delete_volume()
- attach_volume()
- detach_volume()
- describe_snapshots()

---

## 6. Information Required by Our Scanner

The EBS Scanner should collect:

- Volume ID
- Volume Name
- Volume Size (GB)
- Volume Type
- State
- Availability Zone
- Attached EC2 Instance ID
- Encryption Status
- Snapshot Information
- Creation Time
- Tags

---

## 7. Possible Cleanup Checks

The Cleanup Scanner may detect:

- Unattached EBS volumes
- Unused volumes
- Old snapshots
- Unencrypted volumes
- Oversized unused volumes

---

## 8. Notes

Amazon EBS is billed based on the provisioned storage size. Unused or unattached volumes can increase AWS costs, making regular scanning and cleanup important.