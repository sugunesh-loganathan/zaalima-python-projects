# Project 2 - Cloud Infrastructure Auditor & Cost Optimizer

## Scanner Module

The scanner module analyzes AWS resources and identifies resources that may require optimization or cleanup.

### Implemented Scanners

- EC2 Scanner
- EBS Scanner
- Elastic IP Scanner
- CloudWatch Utilization Scanner

### Cleanup Recommendation Module

The cleanup module can:

- Detect unattached EBS volumes.
- Detect unassociated Elastic IP addresses.
- Detect potentially idle EC2 resources using CPU utilization.
- Generate resource-specific cleanup recommendations.
- Assign recommendation priorities.
- Handle missing CloudWatch utilization data safely.

### Testing

The cleanup recommendation module includes unit tests covering:

- Unused resource detection.
- Idle resource detection.
- Cleanup recommendations.
- Resource association checks.
- Missing CPU utilization data.
- Normal resources requiring no action.

### Week 3 Status

Week 3 - Cleanup Scanner: **Completed**

The Cleanup Recommendation Module is ready for further integration and refinement.