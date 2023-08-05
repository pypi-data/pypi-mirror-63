"""
Main interface for ecr service type definitions.

Usage::

    from mypy_boto3.ecr.type_defs import LayerFailureTypeDef

    data: LayerFailureTypeDef = {...}
"""
from datetime import datetime
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
    "LayerFailureTypeDef",
    "LayerTypeDef",
    "BatchCheckLayerAvailabilityResponseTypeDef",
    "ImageIdentifierTypeDef",
    "ImageFailureTypeDef",
    "BatchDeleteImageResponseTypeDef",
    "ImageTypeDef",
    "BatchGetImageResponseTypeDef",
    "CompleteLayerUploadResponseTypeDef",
    "ImageScanningConfigurationTypeDef",
    "RepositoryTypeDef",
    "CreateRepositoryResponseTypeDef",
    "DeleteLifecyclePolicyResponseTypeDef",
    "DeleteRepositoryPolicyResponseTypeDef",
    "DeleteRepositoryResponseTypeDef",
    "AttributeTypeDef",
    "ImageScanFindingTypeDef",
    "ImageScanFindingsTypeDef",
    "ImageScanStatusTypeDef",
    "DescribeImageScanFindingsResponseTypeDef",
    "DescribeImagesFilterTypeDef",
    "ImageScanFindingsSummaryTypeDef",
    "ImageDetailTypeDef",
    "DescribeImagesResponseTypeDef",
    "DescribeRepositoriesResponseTypeDef",
    "AuthorizationDataTypeDef",
    "GetAuthorizationTokenResponseTypeDef",
    "GetDownloadUrlForLayerResponseTypeDef",
    "LifecyclePolicyRuleActionTypeDef",
    "LifecyclePolicyPreviewResultTypeDef",
    "LifecyclePolicyPreviewSummaryTypeDef",
    "GetLifecyclePolicyPreviewResponseTypeDef",
    "GetLifecyclePolicyResponseTypeDef",
    "GetRepositoryPolicyResponseTypeDef",
    "InitiateLayerUploadResponseTypeDef",
    "LifecyclePolicyPreviewFilterTypeDef",
    "ListImagesFilterTypeDef",
    "ListImagesResponseTypeDef",
    "TagTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "PaginatorConfigTypeDef",
    "PutImageResponseTypeDef",
    "PutImageScanningConfigurationResponseTypeDef",
    "PutImageTagMutabilityResponseTypeDef",
    "PutLifecyclePolicyResponseTypeDef",
    "SetRepositoryPolicyResponseTypeDef",
    "StartImageScanResponseTypeDef",
    "StartLifecyclePolicyPreviewResponseTypeDef",
    "UploadLayerPartResponseTypeDef",
    "WaiterConfigTypeDef",
)

LayerFailureTypeDef = TypedDict(
    "LayerFailureTypeDef",
    {
        "layerDigest": str,
        "failureCode": Literal["InvalidLayerDigest", "MissingLayerDigest"],
        "failureReason": str,
    },
    total=False,
)

LayerTypeDef = TypedDict(
    "LayerTypeDef",
    {
        "layerDigest": str,
        "layerAvailability": Literal["AVAILABLE", "UNAVAILABLE"],
        "layerSize": int,
        "mediaType": str,
    },
    total=False,
)

BatchCheckLayerAvailabilityResponseTypeDef = TypedDict(
    "BatchCheckLayerAvailabilityResponseTypeDef",
    {"layers": List[LayerTypeDef], "failures": List[LayerFailureTypeDef]},
    total=False,
)

ImageIdentifierTypeDef = TypedDict(
    "ImageIdentifierTypeDef", {"imageDigest": str, "imageTag": str}, total=False
)

ImageFailureTypeDef = TypedDict(
    "ImageFailureTypeDef",
    {
        "imageId": ImageIdentifierTypeDef,
        "failureCode": Literal[
            "InvalidImageDigest",
            "InvalidImageTag",
            "ImageTagDoesNotMatchDigest",
            "ImageNotFound",
            "MissingDigestAndTag",
        ],
        "failureReason": str,
    },
    total=False,
)

BatchDeleteImageResponseTypeDef = TypedDict(
    "BatchDeleteImageResponseTypeDef",
    {"imageIds": List[ImageIdentifierTypeDef], "failures": List[ImageFailureTypeDef]},
    total=False,
)

ImageTypeDef = TypedDict(
    "ImageTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageManifest": str,
    },
    total=False,
)

BatchGetImageResponseTypeDef = TypedDict(
    "BatchGetImageResponseTypeDef",
    {"images": List[ImageTypeDef], "failures": List[ImageFailureTypeDef]},
    total=False,
)

CompleteLayerUploadResponseTypeDef = TypedDict(
    "CompleteLayerUploadResponseTypeDef",
    {"registryId": str, "repositoryName": str, "uploadId": str, "layerDigest": str},
    total=False,
)

ImageScanningConfigurationTypeDef = TypedDict(
    "ImageScanningConfigurationTypeDef", {"scanOnPush": bool}, total=False
)

RepositoryTypeDef = TypedDict(
    "RepositoryTypeDef",
    {
        "repositoryArn": str,
        "registryId": str,
        "repositoryName": str,
        "repositoryUri": str,
        "createdAt": datetime,
        "imageTagMutability": Literal["MUTABLE", "IMMUTABLE"],
        "imageScanningConfiguration": ImageScanningConfigurationTypeDef,
    },
    total=False,
)

CreateRepositoryResponseTypeDef = TypedDict(
    "CreateRepositoryResponseTypeDef", {"repository": RepositoryTypeDef}, total=False
)

DeleteLifecyclePolicyResponseTypeDef = TypedDict(
    "DeleteLifecyclePolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "lastEvaluatedAt": datetime,
    },
    total=False,
)

DeleteRepositoryPolicyResponseTypeDef = TypedDict(
    "DeleteRepositoryPolicyResponseTypeDef",
    {"registryId": str, "repositoryName": str, "policyText": str},
    total=False,
)

DeleteRepositoryResponseTypeDef = TypedDict(
    "DeleteRepositoryResponseTypeDef", {"repository": RepositoryTypeDef}, total=False
)

_RequiredAttributeTypeDef = TypedDict("_RequiredAttributeTypeDef", {"key": str})
_OptionalAttributeTypeDef = TypedDict("_OptionalAttributeTypeDef", {"value": str}, total=False)


class AttributeTypeDef(_RequiredAttributeTypeDef, _OptionalAttributeTypeDef):
    pass


ImageScanFindingTypeDef = TypedDict(
    "ImageScanFindingTypeDef",
    {
        "name": str,
        "description": str,
        "uri": str,
        "severity": Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL", "UNDEFINED"],
        "attributes": List[AttributeTypeDef],
    },
    total=False,
)

ImageScanFindingsTypeDef = TypedDict(
    "ImageScanFindingsTypeDef",
    {
        "imageScanCompletedAt": datetime,
        "vulnerabilitySourceUpdatedAt": datetime,
        "findings": List[ImageScanFindingTypeDef],
        "findingSeverityCounts": Dict[
            Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL", "UNDEFINED"], int
        ],
    },
    total=False,
)

ImageScanStatusTypeDef = TypedDict(
    "ImageScanStatusTypeDef",
    {"status": Literal["IN_PROGRESS", "COMPLETE", "FAILED"], "description": str},
    total=False,
)

DescribeImageScanFindingsResponseTypeDef = TypedDict(
    "DescribeImageScanFindingsResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageScanStatus": ImageScanStatusTypeDef,
        "imageScanFindings": ImageScanFindingsTypeDef,
        "nextToken": str,
    },
    total=False,
)

DescribeImagesFilterTypeDef = TypedDict(
    "DescribeImagesFilterTypeDef", {"tagStatus": Literal["TAGGED", "UNTAGGED", "ANY"]}, total=False
)

ImageScanFindingsSummaryTypeDef = TypedDict(
    "ImageScanFindingsSummaryTypeDef",
    {
        "imageScanCompletedAt": datetime,
        "vulnerabilitySourceUpdatedAt": datetime,
        "findingSeverityCounts": Dict[
            Literal["INFORMATIONAL", "LOW", "MEDIUM", "HIGH", "CRITICAL", "UNDEFINED"], int
        ],
    },
    total=False,
)

ImageDetailTypeDef = TypedDict(
    "ImageDetailTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageDigest": str,
        "imageTags": List[str],
        "imageSizeInBytes": int,
        "imagePushedAt": datetime,
        "imageScanStatus": ImageScanStatusTypeDef,
        "imageScanFindingsSummary": ImageScanFindingsSummaryTypeDef,
    },
    total=False,
)

DescribeImagesResponseTypeDef = TypedDict(
    "DescribeImagesResponseTypeDef",
    {"imageDetails": List[ImageDetailTypeDef], "nextToken": str},
    total=False,
)

DescribeRepositoriesResponseTypeDef = TypedDict(
    "DescribeRepositoriesResponseTypeDef",
    {"repositories": List[RepositoryTypeDef], "nextToken": str},
    total=False,
)

AuthorizationDataTypeDef = TypedDict(
    "AuthorizationDataTypeDef",
    {"authorizationToken": str, "expiresAt": datetime, "proxyEndpoint": str},
    total=False,
)

GetAuthorizationTokenResponseTypeDef = TypedDict(
    "GetAuthorizationTokenResponseTypeDef",
    {"authorizationData": List[AuthorizationDataTypeDef]},
    total=False,
)

GetDownloadUrlForLayerResponseTypeDef = TypedDict(
    "GetDownloadUrlForLayerResponseTypeDef", {"downloadUrl": str, "layerDigest": str}, total=False
)

LifecyclePolicyRuleActionTypeDef = TypedDict(
    "LifecyclePolicyRuleActionTypeDef", {"type": Literal["EXPIRE"]}, total=False
)

LifecyclePolicyPreviewResultTypeDef = TypedDict(
    "LifecyclePolicyPreviewResultTypeDef",
    {
        "imageTags": List[str],
        "imageDigest": str,
        "imagePushedAt": datetime,
        "action": LifecyclePolicyRuleActionTypeDef,
        "appliedRulePriority": int,
    },
    total=False,
)

LifecyclePolicyPreviewSummaryTypeDef = TypedDict(
    "LifecyclePolicyPreviewSummaryTypeDef", {"expiringImageTotalCount": int}, total=False
)

GetLifecyclePolicyPreviewResponseTypeDef = TypedDict(
    "GetLifecyclePolicyPreviewResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "status": Literal["IN_PROGRESS", "COMPLETE", "EXPIRED", "FAILED"],
        "nextToken": str,
        "previewResults": List[LifecyclePolicyPreviewResultTypeDef],
        "summary": LifecyclePolicyPreviewSummaryTypeDef,
    },
    total=False,
)

GetLifecyclePolicyResponseTypeDef = TypedDict(
    "GetLifecyclePolicyResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "lastEvaluatedAt": datetime,
    },
    total=False,
)

GetRepositoryPolicyResponseTypeDef = TypedDict(
    "GetRepositoryPolicyResponseTypeDef",
    {"registryId": str, "repositoryName": str, "policyText": str},
    total=False,
)

InitiateLayerUploadResponseTypeDef = TypedDict(
    "InitiateLayerUploadResponseTypeDef", {"uploadId": str, "partSize": int}, total=False
)

LifecyclePolicyPreviewFilterTypeDef = TypedDict(
    "LifecyclePolicyPreviewFilterTypeDef",
    {"tagStatus": Literal["TAGGED", "UNTAGGED", "ANY"]},
    total=False,
)

ListImagesFilterTypeDef = TypedDict(
    "ListImagesFilterTypeDef", {"tagStatus": Literal["TAGGED", "UNTAGGED", "ANY"]}, total=False
)

ListImagesResponseTypeDef = TypedDict(
    "ListImagesResponseTypeDef",
    {"imageIds": List[ImageIdentifierTypeDef], "nextToken": str},
    total=False,
)

TagTypeDef = TypedDict("TagTypeDef", {"Key": str, "Value": str}, total=False)

ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef", {"tags": List[TagTypeDef]}, total=False
)

PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef", {"MaxItems": int, "PageSize": int, "StartingToken": str}, total=False
)

PutImageResponseTypeDef = TypedDict("PutImageResponseTypeDef", {"image": ImageTypeDef}, total=False)

PutImageScanningConfigurationResponseTypeDef = TypedDict(
    "PutImageScanningConfigurationResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageScanningConfiguration": ImageScanningConfigurationTypeDef,
    },
    total=False,
)

PutImageTagMutabilityResponseTypeDef = TypedDict(
    "PutImageTagMutabilityResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageTagMutability": Literal["MUTABLE", "IMMUTABLE"],
    },
    total=False,
)

PutLifecyclePolicyResponseTypeDef = TypedDict(
    "PutLifecyclePolicyResponseTypeDef",
    {"registryId": str, "repositoryName": str, "lifecyclePolicyText": str},
    total=False,
)

SetRepositoryPolicyResponseTypeDef = TypedDict(
    "SetRepositoryPolicyResponseTypeDef",
    {"registryId": str, "repositoryName": str, "policyText": str},
    total=False,
)

StartImageScanResponseTypeDef = TypedDict(
    "StartImageScanResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "imageId": ImageIdentifierTypeDef,
        "imageScanStatus": ImageScanStatusTypeDef,
    },
    total=False,
)

StartLifecyclePolicyPreviewResponseTypeDef = TypedDict(
    "StartLifecyclePolicyPreviewResponseTypeDef",
    {
        "registryId": str,
        "repositoryName": str,
        "lifecyclePolicyText": str,
        "status": Literal["IN_PROGRESS", "COMPLETE", "EXPIRED", "FAILED"],
    },
    total=False,
)

UploadLayerPartResponseTypeDef = TypedDict(
    "UploadLayerPartResponseTypeDef",
    {"registryId": str, "repositoryName": str, "uploadId": str, "lastByteReceived": int},
    total=False,
)

WaiterConfigTypeDef = TypedDict(
    "WaiterConfigTypeDef", {"Delay": int, "MaxAttempts": int}, total=False
)
