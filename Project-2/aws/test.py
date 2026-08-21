#EC2 SERVICE

#
# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.ec2 import EC2Service


# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)

# ec2 = EC2Service(factory)

# instances = ec2.list_instances()

# for instance in instances:
#     print(instance)


#EBS SERVICE

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.ebs import EBSService

# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)
# ebs = EBSService(factory)

# # API sirf ek baar call hogi
# volumes = ebs.list_volumes()

# if not volumes:
#     print("No EBS volumes found.")
# else:
#     print(f"Total Volumes: {len(volumes)}")
#     for volume in volumes:
#         print(volume)

# print("\nUnattached Volumes:")

# # Pehle se fetched data pass kar rahe hain
# unused = ebs.get_unattached_volumes(volumes)

# if not unused:
#     print("No unattached volumes found.")
# else:
#     for volume in unused:
#         print(volume)

#EIP(ELASTIC IP)

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.eip import ElasticIPService

# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)

# eip = ElasticIPService(factory)

# addresses = eip.list_addresses()

# if not addresses:
#     print("No Elastic IPs found.")
# else:
#     print(f"Total Elastic IPs: {len(addresses)}")
#     for address in addresses:
#         print(address)

# print("\nUnassociated Elastic IPs:")

# unused = eip.get_unassociated_addresses(addresses)

# if not unused:
#     print("No unassociated Elastic IPs found.")
# else:
#     for address in unused:
#         print(address)

# CLUDWATCH
# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.eip import ElasticIPService

# auth = AWSAuth(
#     profile_name="default",
#     region_name="ap-south-1"
# )

# factory = AWSClientFactory(auth)

# eip = ElasticIPService(factory)

# # Pagination internally handle hogi
# addresses = eip.list_addresses()

# if not addresses:
#     print("No Elastic IPs found.")
# else:
#     print(f"Total Elastic IPs: {len(addresses)}")
#     print()

#     for address in addresses:
#         print(address)

# print("\nUnassociated Elastic IPs:")

# unused = eip.get_unassociated_addresses(addresses)

# if not unused:
#     print("No unassociated Elastic IPs found.")
# else:
#     for address in unused:
#         print(address)



# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.ec2 import EC2Service
# from aws.ebs import EBSService
# from aws.eip import ElasticIPService


# def main():

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     factory = AWSClientFactory(auth)

#     print("=" * 50)
#     print("AWS MODULE INTEGRATION TEST")
#     print("=" * 50)

#     # ---------------- EC2 ---------------- #

#     print("\nEC2")

#     ec2 = EC2Service(factory)

#     instances = ec2.list_instances()

#     print(f"Instances Found: {len(instances)}")

#     # ---------------- EBS ---------------- #

#     print("\nEBS")

#     ebs = EBSService(factory)

#     volumes = ebs.list_volumes()

#     print(f"Volumes Found: {len(volumes)}")

#     print(
#         f"Unattached Volumes: {len(ebs.get_unattached_volumes(volumes))}"
#     )

#     # ---------------- Elastic IP ---------------- #

#     print("\nElastic IP")

#     eip = ElasticIPService(factory)

#     addresses = eip.list_addresses()

#     print(f"Elastic IPs Found: {len(addresses)}")

#     print(
#         f"Unassociated Elastic IPs: {len(eip.get_unassociated_addresses(addresses))}"
#     )

#     print("\nAll AWS services are working successfully.")


# if __name__ == "__main__":
#     main()

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService


# def main():

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     factory = AWSClientFactory(auth)

#     cleanup = CleanupService(factory)

#     print("=" * 50)
#     print("Cleanup Module Test")
#     print("=" * 50)

#     unused_volumes = cleanup.get_unused_volumes()

#     print(f"Unused Volumes : {len(unused_volumes)}")

#     unused_eips = cleanup.get_unused_elastic_ips()

#     print(f"Unused Elastic IPs : {len(unused_eips)}")


# if __name__ == "__main__":
#     main()

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService


# def main():

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     factory = AWSClientFactory(auth)

#     cleanup = CleanupService(factory)

#     print("=" * 50)
#     print("WEEK 3 - DAY 2 RESOURCE VALIDATION TEST")
#     print("=" * 50)

#     # --------------------------------------------------
#     # EBS Validation
#     # --------------------------------------------------

#     print("\nEBS Resource Validation")

#     unused_volumes = cleanup.get_unused_volumes()

#     print(f"Validated Unused Volumes: {len(unused_volumes)}")

#     for volume in unused_volumes:
#         print(
#             f"Volume: {volume['VolumeId']} | "
#             f"State: {volume['State']} | "
#             f"Attachments: {volume['Attachments']}"
#         )

#     # --------------------------------------------------
#     # Elastic IP Validation
#     # --------------------------------------------------

#     print("\nElastic IP Resource Validation")

#     unused_eips = cleanup.get_unused_elastic_ips()

#     print(f"Validated Unused Elastic IPs: {len(unused_eips)}")

#     for address in unused_eips:
#         print(
#             f"Public IP: {address['PublicIp']} | "
#             f"InstanceId: {address['InstanceId']}"
#         )

#     print("\nResource validation completed successfully.")


# if __name__ == "__main__":
#     main()

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService


# def main():

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     factory = AWSClientFactory(auth)

#     cleanup = CleanupService(factory)

#     print("=" * 60)
#     print("WEEK 3 - DAY 3 DRY RUN TEST")
#     print("=" * 60)

#     result = cleanup.dry_run()

#     print("\nLocal Dry Run Validation")

#     test_volume = {
#         "VolumeId": "vol-test-123",
#         "State": "available",
#         "Attachments": 0
#     }

#     test_eip = {
#         "PublicIp": "1.2.3.4",
#         "InstanceId": None
#     }

#     print(
#         "Test EBS eligible:",
#         cleanup.validate_volume(test_volume)
#     )

#     print(
#         "Test EIP eligible:",
#         cleanup.validate_elastic_ip(test_eip)
#     )


# if __name__ == "__main__":
#     main()

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService


# def main():

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     factory = AWSClientFactory(auth)

#     cleanup = CleanupService(factory)

#     print("=" * 60)
#     print("WEEK 3 - DAY 4 CLEANUP HELPER TEST")
#     print("=" * 60)

#     # --------------------------------------------------
#     # Dry Run
#     # --------------------------------------------------

#     result = cleanup.dry_run()

#     print("\nCleanup Summary")

#     print(
#         f"EBS cleanup candidates: "
#         f"{len(result['volumes'])}"
#     )

#     print(
#         f"Elastic IP cleanup candidates: "
#         f"{len(result['elastic_ips'])}"
#     )

#     # --------------------------------------------------
#     # Local Helper Tests
#     # --------------------------------------------------

#     print("\nLocal Cleanup Helper Tests")

#     volume_result = cleanup.cleanup_volume(
#         "vol-test-123",
#         dry_run=True
#     )

#     print("EBS Helper:")
#     print(volume_result)

#     eip_result = cleanup.cleanup_elastic_ip(
#         "eipalloc-test-123",
#         dry_run=True
#     )

#     print("Elastic IP Helper:")
#     print(eip_result)


# if __name__ == "__main__":
#     main()


# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService
# from aws.exceptions import AWSCleanupError


# def main():

#     # --------------------------------------------------
#     # AWS AUTHENTICATION
#     # --------------------------------------------------

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     # --------------------------------------------------
#     # AWS CLIENT FACTORY
#     # --------------------------------------------------

#     factory = AWSClientFactory(auth)

#     # --------------------------------------------------
#     # CLEANUP SERVICE
#     # --------------------------------------------------

#     cleanup = CleanupService(factory)

#     print("=" * 60)
#     print("WEEK 3 - DAY 5 EXCEPTION HANDLING TEST")
#     print("=" * 60)

#     # --------------------------------------------------
#     # DRY RUN TEST
#     # --------------------------------------------------

#     print("\nCleanup Dry Run")

#     result = cleanup.dry_run()

#     print("\nCleanup Summary")

#     print(
#         f"EBS cleanup candidates: "
#         f"{len(result['volumes'])}"
#     )

#     print(
#         f"Elastic IP cleanup candidates: "
#         f"{len(result['elastic_ips'])}"
#     )

#     # --------------------------------------------------
#     # LOCAL CLEANUP HELPER TEST
#     # --------------------------------------------------

#     print("\nLocal Cleanup Helper Tests")

#     try:

#         volume_result = cleanup.cleanup_volume(
#             "vol-test-123",
#             dry_run=True
#         )

#         print("EBS Helper:")
#         print(volume_result)

#     except AWSCleanupError as e:

#         print(f"EBS Cleanup Error: {e}")

#     try:

#         eip_result = cleanup.cleanup_elastic_ip(
#             "eipalloc-test-123",
#             dry_run=True
#         )

#         print("Elastic IP Helper:")
#         print(eip_result)

#     except AWSCleanupError as e:

#         print(f"Elastic IP Cleanup Error: {e}")

#     # --------------------------------------------------
#     # EXCEPTION VALIDATION TEST
#     # --------------------------------------------------

#     print("\nException Handling Tests")

#     # EBS invalid input

#     try:

#         cleanup.cleanup_volume(
#             "",
#             dry_run=True
#         )

#     except ValueError as e:

#         print(f"EBS Validation Error: {e}")

#     # Elastic IP invalid input

#     try:

#         cleanup.cleanup_elastic_ip(
#             "",
#             dry_run=True
#         )

#     except ValueError as e:

#         print(f"Elastic IP Validation Error: {e}")

#     # --------------------------------------------------
#     # COMPLETED
#     # --------------------------------------------------

#     print("\n" + "=" * 60)
#     print("WEEK 3 - DAY 5 TEST COMPLETED")
#     print("=" * 60)


# if __name__ == "__main__":
#     main()

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService
# from aws.exceptions import AWSCleanupError


# def main():

#     # --------------------------------------------------
#     # AWS AUTHENTICATION
#     # --------------------------------------------------

#     auth = AWSAuth(
#         profile_name="default",
#         region_name="ap-south-1"
#     )

#     # --------------------------------------------------
#     # AWS CLIENT FACTORY
#     # --------------------------------------------------

#     factory = AWSClientFactory(auth)

#     # --------------------------------------------------
#     # CLEANUP SERVICE
#     # --------------------------------------------------

#     cleanup = CleanupService(factory)

#     print("=" * 60)
#     print("WEEK 3 - DAY 6 CLEANUP SUMMARY TEST")
#     print("=" * 60)

#     # --------------------------------------------------
#     # CLEANUP SUMMARY
#     # --------------------------------------------------

#     try:

#         summary = cleanup.generate_summary(
#             dry_run=True
#         )

#         cleanup.display_summary(summary)

#     except AWSCleanupError as e:

#         print(f"\nCleanup Error: {e}")

#     except Exception as e:

#         print(f"\nUnexpected Error: {e}")

#     # --------------------------------------------------
#     # SUMMARY DATA TEST
#     # --------------------------------------------------

#     print("\nSummary Data")

#     print(summary)


# if __name__ == "__main__":
#     main()

# from aws.auth import AWSAuth
# from aws.client_factory import AWSClientFactory
# from aws.cleanup import CleanupService
# from aws.exceptions import AWSCleanupError


# def main():

#     # ==================================================
#     # AWS AUTHENTICATION
#     # ==================================================

#     print("=" * 60)
#     print("WEEK 3 - DAY 7 FINAL CLEANUP INTEGRATION TEST")
#     print("=" * 60)

#     try:

#         auth = AWSAuth(
#             profile_name="default",
#             region_name="ap-south-1"
#         )

#         # ==================================================
#         # AWS CLIENT FACTORY
#         # ==================================================

#         factory = AWSClientFactory(auth)

#         # ==================================================
#         # CLEANUP SERVICE
#         # ==================================================

#         cleanup = CleanupService(factory)

#         # ==================================================
#         # FINAL WORKFLOW
#         # ==================================================

#         result = cleanup.run_cleanup_workflow(
#             dry_run=True
#         )

#         # ==================================================
#         # FINAL RESULT
#         # ==================================================

#         print("\n")
#         print("=" * 60)
#         print("FINAL CLEANUP WORKFLOW RESULT")
#         print("=" * 60)

#         print(
#             f"Status : {result['status']}"
#         )

#         print(
#             f"Mode   : {result['mode']}"
#         )

#         # ==================================================
#         # FINAL SUMMARY
#         # ==================================================

#         summary = result["summary"]

#         print("\nFinal Resource Summary")

#         print(
#             f"EBS Volumes Scanned : "
#             f"{summary['ebs']['total']}"
#         )

#         print(
#             f"EBS Cleanup Candidates : "
#             f"{summary['ebs']['cleanup_candidates']}"
#         )

#         print(
#             f"Elastic IPs Scanned : "
#             f"{summary['elastic_ips']['total']}"
#         )

#         print(
#             f"Elastic IP Cleanup Candidates : "
#             f"{summary['elastic_ips']['cleanup_candidates']}"
#         )

#         print("\nCleanup Recommendations")

#         if summary["recommendations"]:

#             for recommendation in summary["recommendations"]:

#                 print(
#                     f"- "
#                     f"{recommendation['resource_type']} | "
#                     f"{recommendation['resource_id']} | "
#                     f"{recommendation['recommendation']}"
#                 )

#         else:

#             print("No cleanup recommendations.")

#         # ==================================================
#         # SAFETY CONFIRMATION
#         # ==================================================

#         print("\nSafety Check")

#         if result["mode"] == "dry_run":

#             print(
#                 "PASS - Dry Run enabled."
#             )

#             print(
#                 "PASS - No AWS resources were modified."
#             )

#         print("\n")
#         print("=" * 60)
#         print("WEEK 3 - DAY 7 TEST COMPLETED")
#         print("=" * 60)

#     except AWSCleanupError as e:

#         print("\nCleanup Error:")
#         print(e)

#     except Exception as e:

#         print("\nUnexpected Error:")
#         print(e)


# if __name__ == "__main__":
#     main()