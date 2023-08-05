"""
Main interface for workmailmessageflow service client

Usage::

    import boto3
    from mypy_boto3.workmailmessageflow import WorkMailMessageFlowClient

    session = boto3.Session()

    client: WorkMailMessageFlowClient = boto3.client("workmailmessageflow")
    session_client: WorkMailMessageFlowClient = session.client("workmailmessageflow")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Any, Dict, TYPE_CHECKING
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_workmailmessageflow.type_defs import GetRawMessageContentResponseTypeDef


__all__ = ("WorkMailMessageFlowClient",)


class Exceptions:
    ClientError: Boto3ClientError
    ResourceNotFoundException: Boto3ClientError


class WorkMailMessageFlowClient:
    """
    [WorkMailMessageFlow.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.can_paginate)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.generate_presigned_url)
        """

    def get_raw_message_content(self, messageId: str) -> GetRawMessageContentResponseTypeDef:
        """
        [Client.get_raw_message_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/workmailmessageflow.html#WorkMailMessageFlow.Client.get_raw_message_content)
        """
