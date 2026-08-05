import time
from functools import wraps

from botocore.exceptions import ClientError

from utils.logger import logger


def aws_retry(max_retries=3, delay=1):
    """
    Retry decorator for AWS API calls.
    Retries only on throttling or request limit errors.
    """

    def decorator(func):

        @wraps(func)
        def wrapper(*args, **kwargs):

            current_delay = delay

            for attempt in range(1, max_retries + 1):

                try:
                    return func(*args, **kwargs)

                except ClientError as e:

                    error_code = e.response["Error"]["Code"]

                    if error_code in (
                        "Throttling",
                        "ThrottlingException",
                        "RequestLimitExceeded",
                        "TooManyRequestsException",
                    ):

                        logger.warning(
                            f"Retry {attempt}/{max_retries} "
                            f"after throttling ({error_code})..."
                        )

                        if attempt == max_retries:
                            raise

                        time.sleep(current_delay)
                        current_delay *= 2

                    else:
                        raise

        return wrapper

    return decorator