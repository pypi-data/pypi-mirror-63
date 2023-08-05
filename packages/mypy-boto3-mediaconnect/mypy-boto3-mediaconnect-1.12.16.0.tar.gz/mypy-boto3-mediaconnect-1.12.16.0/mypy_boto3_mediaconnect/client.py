"""
Main interface for mediaconnect service client

Usage::

    import boto3
    from mypy_boto3.mediaconnect import MediaConnectClient

    session = boto3.Session()

    client: MediaConnectClient = boto3.client("mediaconnect")
    session_client: MediaConnectClient = session.client("mediaconnect")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
import sys
from typing import Any, Dict, List, TYPE_CHECKING, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_mediaconnect.paginator import ListEntitlementsPaginator, ListFlowsPaginator
from mypy_boto3_mediaconnect.type_defs import (
    AddFlowOutputsResponseTypeDef,
    AddOutputRequestTypeDef,
    CreateFlowResponseTypeDef,
    DeleteFlowResponseTypeDef,
    DescribeFlowResponseTypeDef,
    GrantEntitlementRequestTypeDef,
    GrantFlowEntitlementsResponseTypeDef,
    ListEntitlementsResponseTypeDef,
    ListFlowsResponseTypeDef,
    ListTagsForResourceResponseTypeDef,
    RemoveFlowOutputResponseTypeDef,
    RevokeFlowEntitlementResponseTypeDef,
    SetSourceRequestTypeDef,
    StartFlowResponseTypeDef,
    StopFlowResponseTypeDef,
    UpdateEncryptionTypeDef,
    UpdateFlowEntitlementResponseTypeDef,
    UpdateFlowOutputResponseTypeDef,
    UpdateFlowSourceResponseTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("MediaConnectClient",)


class Exceptions:
    AddFlowOutputs420Exception: Boto3ClientError
    BadRequestException: Boto3ClientError
    ClientError: Boto3ClientError
    CreateFlow420Exception: Boto3ClientError
    ForbiddenException: Boto3ClientError
    GrantFlowEntitlements420Exception: Boto3ClientError
    InternalServerErrorException: Boto3ClientError
    NotFoundException: Boto3ClientError
    ServiceUnavailableException: Boto3ClientError
    TooManyRequestsException: Boto3ClientError


class MediaConnectClient:
    """
    [MediaConnect.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client)
    """

    exceptions: Exceptions

    def add_flow_outputs(
        self, FlowArn: str, Outputs: List[AddOutputRequestTypeDef]
    ) -> AddFlowOutputsResponseTypeDef:
        """
        [Client.add_flow_outputs documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.add_flow_outputs)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.can_paginate)
        """

    def create_flow(
        self,
        Name: str,
        Source: SetSourceRequestTypeDef,
        AvailabilityZone: str = None,
        Entitlements: List[GrantEntitlementRequestTypeDef] = None,
        Outputs: List[AddOutputRequestTypeDef] = None,
    ) -> CreateFlowResponseTypeDef:
        """
        [Client.create_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.create_flow)
        """

    def delete_flow(self, FlowArn: str) -> DeleteFlowResponseTypeDef:
        """
        [Client.delete_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.delete_flow)
        """

    def describe_flow(self, FlowArn: str) -> DescribeFlowResponseTypeDef:
        """
        [Client.describe_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.describe_flow)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.generate_presigned_url)
        """

    def grant_flow_entitlements(
        self, Entitlements: List[GrantEntitlementRequestTypeDef], FlowArn: str
    ) -> GrantFlowEntitlementsResponseTypeDef:
        """
        [Client.grant_flow_entitlements documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.grant_flow_entitlements)
        """

    def list_entitlements(
        self, MaxResults: int = None, NextToken: str = None
    ) -> ListEntitlementsResponseTypeDef:
        """
        [Client.list_entitlements documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.list_entitlements)
        """

    def list_flows(self, MaxResults: int = None, NextToken: str = None) -> ListFlowsResponseTypeDef:
        """
        [Client.list_flows documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.list_flows)
        """

    def list_tags_for_resource(self, ResourceArn: str) -> ListTagsForResourceResponseTypeDef:
        """
        [Client.list_tags_for_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.list_tags_for_resource)
        """

    def remove_flow_output(self, FlowArn: str, OutputArn: str) -> RemoveFlowOutputResponseTypeDef:
        """
        [Client.remove_flow_output documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.remove_flow_output)
        """

    def revoke_flow_entitlement(
        self, EntitlementArn: str, FlowArn: str
    ) -> RevokeFlowEntitlementResponseTypeDef:
        """
        [Client.revoke_flow_entitlement documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.revoke_flow_entitlement)
        """

    def start_flow(self, FlowArn: str) -> StartFlowResponseTypeDef:
        """
        [Client.start_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.start_flow)
        """

    def stop_flow(self, FlowArn: str) -> StopFlowResponseTypeDef:
        """
        [Client.stop_flow documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.stop_flow)
        """

    def tag_resource(self, ResourceArn: str, Tags: Dict[str, str]) -> None:
        """
        [Client.tag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.tag_resource)
        """

    def untag_resource(self, ResourceArn: str, TagKeys: List[str]) -> None:
        """
        [Client.untag_resource documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.untag_resource)
        """

    def update_flow_entitlement(
        self,
        EntitlementArn: str,
        FlowArn: str,
        Description: str = None,
        Encryption: UpdateEncryptionTypeDef = None,
        Subscribers: List[str] = None,
    ) -> UpdateFlowEntitlementResponseTypeDef:
        """
        [Client.update_flow_entitlement documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_entitlement)
        """

    def update_flow_output(
        self,
        FlowArn: str,
        OutputArn: str,
        CidrAllowList: List[str] = None,
        Description: str = None,
        Destination: str = None,
        Encryption: UpdateEncryptionTypeDef = None,
        MaxLatency: int = None,
        Port: int = None,
        Protocol: Literal["zixi-push", "rtp-fec", "rtp", "zixi-pull", "rist"] = None,
        RemoteId: str = None,
        SmoothingLatency: int = None,
        StreamId: str = None,
    ) -> UpdateFlowOutputResponseTypeDef:
        """
        [Client.update_flow_output documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_output)
        """

    def update_flow_source(
        self,
        FlowArn: str,
        SourceArn: str,
        Decryption: UpdateEncryptionTypeDef = None,
        Description: str = None,
        EntitlementArn: str = None,
        IngestPort: int = None,
        MaxBitrate: int = None,
        MaxLatency: int = None,
        Protocol: Literal["zixi-push", "rtp-fec", "rtp", "zixi-pull", "rist"] = None,
        StreamId: str = None,
        WhitelistCidr: str = None,
    ) -> UpdateFlowSourceResponseTypeDef:
        """
        [Client.update_flow_source documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Client.update_flow_source)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_entitlements"]
    ) -> ListEntitlementsPaginator:
        """
        [Paginator.ListEntitlements documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Paginator.ListEntitlements)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_flows"]) -> ListFlowsPaginator:
        """
        [Paginator.ListFlows documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/mediaconnect.html#MediaConnect.Paginator.ListFlows)
        """
