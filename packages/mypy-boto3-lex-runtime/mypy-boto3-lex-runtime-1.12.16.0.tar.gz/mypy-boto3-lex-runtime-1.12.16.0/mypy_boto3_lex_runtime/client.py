"""
Main interface for lex-runtime service client

Usage::

    import boto3
    from mypy_boto3.lex_runtime import LexRuntimeServiceClient

    session = boto3.Session()

    client: LexRuntimeServiceClient = boto3.client("lex-runtime")
    session_client: LexRuntimeServiceClient = session.client("lex-runtime")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import Any, Dict, IO, List, TYPE_CHECKING, Union
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_lex_runtime.type_defs import (
    DeleteSessionResponseTypeDef,
    DialogActionTypeDef,
    GetSessionResponseTypeDef,
    IntentSummaryTypeDef,
    PostContentResponseTypeDef,
    PostTextResponseTypeDef,
    PutSessionResponseTypeDef,
)


__all__ = ("LexRuntimeServiceClient",)


class Exceptions:
    BadGatewayException: Boto3ClientError
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    ConflictException: Boto3ClientError
    DependencyFailedException: Boto3ClientError
    InternalFailureException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    LoopDetectedException: Boto3ClientError
    NotAcceptableException: Boto3ClientError
    NotFoundException: Boto3ClientError
    RequestTimeoutException: Boto3ClientError
    UnsupportedMediaTypeException: Boto3ClientError


class LexRuntimeServiceClient:
    """
    [LexRuntimeService.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.can_paginate)
        """

    def delete_session(
        self, botName: str, botAlias: str, userId: str
    ) -> DeleteSessionResponseTypeDef:
        """
        [Client.delete_session documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.delete_session)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.generate_presigned_url)
        """

    def get_session(
        self, botName: str, botAlias: str, userId: str, checkpointLabelFilter: str = None
    ) -> GetSessionResponseTypeDef:
        """
        [Client.get_session documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.get_session)
        """

    def post_content(
        self,
        botName: str,
        botAlias: str,
        userId: str,
        contentType: str,
        inputStream: Union[bytes, IO],
        sessionAttributes: str = None,
        requestAttributes: str = None,
        accept: str = None,
    ) -> PostContentResponseTypeDef:
        """
        [Client.post_content documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.post_content)
        """

    def post_text(
        self,
        botName: str,
        botAlias: str,
        userId: str,
        inputText: str,
        sessionAttributes: Dict[str, str] = None,
        requestAttributes: Dict[str, str] = None,
    ) -> PostTextResponseTypeDef:
        """
        [Client.post_text documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.post_text)
        """

    def put_session(
        self,
        botName: str,
        botAlias: str,
        userId: str,
        sessionAttributes: Dict[str, str] = None,
        dialogAction: DialogActionTypeDef = None,
        recentIntentSummaryView: List[IntentSummaryTypeDef] = None,
        accept: str = None,
    ) -> PutSessionResponseTypeDef:
        """
        [Client.put_session documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/lex-runtime.html#LexRuntimeService.Client.put_session)
        """
