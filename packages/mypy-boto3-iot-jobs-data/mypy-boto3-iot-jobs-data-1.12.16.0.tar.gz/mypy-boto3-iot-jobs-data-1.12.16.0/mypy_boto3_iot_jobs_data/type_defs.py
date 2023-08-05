"""
Main interface for iot-jobs-data service type definitions.

Usage::

    from mypy_boto3.iot_jobs_data.type_defs import JobExecutionTypeDef

    data: JobExecutionTypeDef = {...}
"""
import sys
from typing import Dict, List

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal
if sys.version_info >= (3, 8):
    from typing import TypedDict
else:
    from typing_extensions import TypedDict


__all__ = (
    "JobExecutionTypeDef",
    "DescribeJobExecutionResponseTypeDef",
    "JobExecutionSummaryTypeDef",
    "GetPendingJobExecutionsResponseTypeDef",
    "StartNextPendingJobExecutionResponseTypeDef",
    "JobExecutionStateTypeDef",
    "UpdateJobExecutionResponseTypeDef",
)

JobExecutionTypeDef = TypedDict(
    "JobExecutionTypeDef",
    {
        "jobId": str,
        "thingName": str,
        "status": Literal[
            "QUEUED",
            "IN_PROGRESS",
            "SUCCEEDED",
            "FAILED",
            "TIMED_OUT",
            "REJECTED",
            "REMOVED",
            "CANCELED",
        ],
        "statusDetails": Dict[str, str],
        "queuedAt": int,
        "startedAt": int,
        "lastUpdatedAt": int,
        "approximateSecondsBeforeTimedOut": int,
        "versionNumber": int,
        "executionNumber": int,
        "jobDocument": str,
    },
    total=False,
)

DescribeJobExecutionResponseTypeDef = TypedDict(
    "DescribeJobExecutionResponseTypeDef", {"execution": JobExecutionTypeDef}, total=False
)

JobExecutionSummaryTypeDef = TypedDict(
    "JobExecutionSummaryTypeDef",
    {
        "jobId": str,
        "queuedAt": int,
        "startedAt": int,
        "lastUpdatedAt": int,
        "versionNumber": int,
        "executionNumber": int,
    },
    total=False,
)

GetPendingJobExecutionsResponseTypeDef = TypedDict(
    "GetPendingJobExecutionsResponseTypeDef",
    {
        "inProgressJobs": List[JobExecutionSummaryTypeDef],
        "queuedJobs": List[JobExecutionSummaryTypeDef],
    },
    total=False,
)

StartNextPendingJobExecutionResponseTypeDef = TypedDict(
    "StartNextPendingJobExecutionResponseTypeDef", {"execution": JobExecutionTypeDef}, total=False
)

JobExecutionStateTypeDef = TypedDict(
    "JobExecutionStateTypeDef",
    {
        "status": Literal[
            "QUEUED",
            "IN_PROGRESS",
            "SUCCEEDED",
            "FAILED",
            "TIMED_OUT",
            "REJECTED",
            "REMOVED",
            "CANCELED",
        ],
        "statusDetails": Dict[str, str],
        "versionNumber": int,
    },
    total=False,
)

UpdateJobExecutionResponseTypeDef = TypedDict(
    "UpdateJobExecutionResponseTypeDef",
    {"executionState": JobExecutionStateTypeDef, "jobDocument": str},
    total=False,
)
