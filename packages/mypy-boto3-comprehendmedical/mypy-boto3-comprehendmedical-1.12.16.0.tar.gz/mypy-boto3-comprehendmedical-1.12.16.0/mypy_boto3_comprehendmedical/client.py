"""
Main interface for comprehendmedical service client

Usage::

    import boto3
    from mypy_boto3.comprehendmedical import ComprehendMedicalClient

    session = boto3.Session()

    client: ComprehendMedicalClient = boto3.client("comprehendmedical")
    session_client: ComprehendMedicalClient = session.client("comprehendmedical")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, TYPE_CHECKING
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_comprehendmedical.type_defs import (
    ComprehendMedicalAsyncJobFilterTypeDef,
    DescribeEntitiesDetectionV2JobResponseTypeDef,
    DescribePHIDetectionJobResponseTypeDef,
    DetectEntitiesResponseTypeDef,
    DetectEntitiesV2ResponseTypeDef,
    DetectPHIResponseTypeDef,
    InferICD10CMResponseTypeDef,
    InferRxNormResponseTypeDef,
    InputDataConfigTypeDef,
    ListEntitiesDetectionV2JobsResponseTypeDef,
    ListPHIDetectionJobsResponseTypeDef,
    OutputDataConfigTypeDef,
    StartEntitiesDetectionV2JobResponseTypeDef,
    StartPHIDetectionJobResponseTypeDef,
    StopEntitiesDetectionV2JobResponseTypeDef,
    StopPHIDetectionJobResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("ComprehendMedicalClient",)


class Exceptions:
    ClientError: Boto3ClientError
    InternalServerException: Boto3ClientError
    InvalidEncodingException: Boto3ClientError
    InvalidRequestException: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError
    ServiceUnavailableException: Boto3ClientError
    TextSizeLimitExceededException: Boto3ClientError
    TooManyRequestsException: Boto3ClientError
    ValidationException: Boto3ClientError


class ComprehendMedicalClient:
    """
    [ComprehendMedical.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.can_paginate)
        """

    def describe_entities_detection_v2_job(
        self, JobId: str
    ) -> DescribeEntitiesDetectionV2JobResponseTypeDef:
        """
        [Client.describe_entities_detection_v2_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_entities_detection_v2_job)
        """

    def describe_phi_detection_job(self, JobId: str) -> DescribePHIDetectionJobResponseTypeDef:
        """
        [Client.describe_phi_detection_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.describe_phi_detection_job)
        """

    def detect_entities(self, Text: str) -> DetectEntitiesResponseTypeDef:
        """
        [Client.detect_entities documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.detect_entities)
        """

    def detect_entities_v2(self, Text: str) -> DetectEntitiesV2ResponseTypeDef:
        """
        [Client.detect_entities_v2 documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.detect_entities_v2)
        """

    def detect_phi(self, Text: str) -> DetectPHIResponseTypeDef:
        """
        [Client.detect_phi documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.detect_phi)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.generate_presigned_url)
        """

    def infer_icd10_cm(self, Text: str) -> InferICD10CMResponseTypeDef:
        """
        [Client.infer_icd10_cm documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.infer_icd10_cm)
        """

    def infer_rx_norm(self, Text: str) -> InferRxNormResponseTypeDef:
        """
        [Client.infer_rx_norm documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.infer_rx_norm)
        """

    def list_entities_detection_v2_jobs(
        self,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListEntitiesDetectionV2JobsResponseTypeDef:
        """
        [Client.list_entities_detection_v2_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_entities_detection_v2_jobs)
        """

    def list_phi_detection_jobs(
        self,
        Filter: ComprehendMedicalAsyncJobFilterTypeDef = None,
        NextToken: str = None,
        MaxResults: int = None,
    ) -> ListPHIDetectionJobsResponseTypeDef:
        """
        [Client.list_phi_detection_jobs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.list_phi_detection_jobs)
        """

    def start_entities_detection_v2_job(
        self,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = None,
        ClientRequestToken: str = None,
        KMSKey: str = None,
    ) -> StartEntitiesDetectionV2JobResponseTypeDef:
        """
        [Client.start_entities_detection_v2_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_entities_detection_v2_job)
        """

    def start_phi_detection_job(
        self,
        InputDataConfig: InputDataConfigTypeDef,
        OutputDataConfig: OutputDataConfigTypeDef,
        DataAccessRoleArn: str,
        LanguageCode: Literal["en"],
        JobName: str = None,
        ClientRequestToken: str = None,
        KMSKey: str = None,
    ) -> StartPHIDetectionJobResponseTypeDef:
        """
        [Client.start_phi_detection_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.start_phi_detection_job)
        """

    def stop_entities_detection_v2_job(
        self, JobId: str
    ) -> StopEntitiesDetectionV2JobResponseTypeDef:
        """
        [Client.stop_entities_detection_v2_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_entities_detection_v2_job)
        """

    def stop_phi_detection_job(self, JobId: str) -> StopPHIDetectionJobResponseTypeDef:
        """
        [Client.stop_phi_detection_job documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/comprehendmedical.html#ComprehendMedical.Client.stop_phi_detection_job)
        """
