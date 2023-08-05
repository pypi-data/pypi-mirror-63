"""
Main interface for iot-jobs-data service client

Usage::

    import boto3
    from mypy_boto3.iot_jobs_data import IoTJobsDataPlaneClient

    session = boto3.Session()

    client: IoTJobsDataPlaneClient = boto3.client("iot-jobs-data")
    session_client: IoTJobsDataPlaneClient = session.client("iot-jobs-data")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, TYPE_CHECKING
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_iot_jobs_data.type_defs import (
    DescribeJobExecutionResponseTypeDef,
    GetPendingJobExecutionsResponseTypeDef,
    StartNextPendingJobExecutionResponseTypeDef,
    UpdateJobExecutionResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("IoTJobsDataPlaneClient",)


class Exceptions:
    CertificateValidationException: Boto3ClientError
    ClientError: Boto3ClientError
    InvalidRequestException: Boto3ClientError
    InvalidStateTransitionException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    ServiceUnavailableException: Boto3ClientError
    TerminalStateException: Boto3ClientError
    ThrottlingException: Boto3ClientError


class IoTJobsDataPlaneClient:
    """
    [IoTJobsDataPlane.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.can_paginate)
        """

    def describe_job_execution(
        self,
        jobId: str,
        thingName: str,
        includeJobDocument: bool = None,
        executionNumber: int = None,
    ) -> DescribeJobExecutionResponseTypeDef:
        """
        [Client.describe_job_execution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.describe_job_execution)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.generate_presigned_url)
        """

    def get_pending_job_executions(self, thingName: str) -> GetPendingJobExecutionsResponseTypeDef:
        """
        [Client.get_pending_job_executions documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.get_pending_job_executions)
        """

    def start_next_pending_job_execution(
        self, thingName: str, statusDetails: Dict[str, str] = None, stepTimeoutInMinutes: int = None
    ) -> StartNextPendingJobExecutionResponseTypeDef:
        """
        [Client.start_next_pending_job_execution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.start_next_pending_job_execution)
        """

    def update_job_execution(
        self,
        jobId: str,
        thingName: str,
        status: Literal[
            "QUEUED",
            "IN_PROGRESS",
            "SUCCEEDED",
            "FAILED",
            "TIMED_OUT",
            "REJECTED",
            "REMOVED",
            "CANCELED",
        ],
        statusDetails: Dict[str, str] = None,
        stepTimeoutInMinutes: int = None,
        expectedVersion: int = None,
        includeJobExecutionState: bool = None,
        includeJobDocument: bool = None,
        executionNumber: int = None,
    ) -> UpdateJobExecutionResponseTypeDef:
        """
        [Client.update_job_execution documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/iot-jobs-data.html#IoTJobsDataPlane.Client.update_job_execution)
        """
