"""
Main interface for autoscaling-plans service client

Usage::

    import boto3
    from mypy_boto3.autoscaling_plans import AutoScalingPlansClient

    session = boto3.Session()

    client: AutoScalingPlansClient = boto3.client("autoscaling-plans")
    session_client: AutoScalingPlansClient = session.client("autoscaling-plans")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from datetime import datetime
import sys
from typing import Any, Dict, List, TYPE_CHECKING, overload
from botocore.exceptions import ClientError as Boto3ClientError
from mypy_boto3_autoscaling_plans.paginator import (
    DescribeScalingPlanResourcesPaginator,
    DescribeScalingPlansPaginator,
)
from mypy_boto3_autoscaling_plans.type_defs import (
    ApplicationSourceTypeDef,
    CreateScalingPlanResponseTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansResponseTypeDef,
    GetScalingPlanResourceForecastDataResponseTypeDef,
    ScalingInstructionTypeDef,
)

if sys.version_info >= (3, 8):
    from typing import Literal
else:
    from typing_extensions import Literal


__all__ = ("AutoScalingPlansClient",)


class Exceptions:
    ClientError: Boto3ClientError
    ConcurrentUpdateException: Boto3ClientError
    InternalServiceException: Boto3ClientError
    InvalidNextTokenException: Boto3ClientError
    LimitExceededException: Boto3ClientError
    ObjectNotFoundException: Boto3ClientError
    ValidationException: Boto3ClientError


class AutoScalingPlansClient:
    """
    [AutoScalingPlans.Client documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client)
    """

    exceptions: Exceptions

    def can_paginate(self, operation_name: str) -> bool:
        """
        [Client.can_paginate documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.can_paginate)
        """

    def create_scaling_plan(
        self,
        ScalingPlanName: str,
        ApplicationSource: ApplicationSourceTypeDef,
        ScalingInstructions: List[ScalingInstructionTypeDef],
    ) -> CreateScalingPlanResponseTypeDef:
        """
        [Client.create_scaling_plan documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.create_scaling_plan)
        """

    def delete_scaling_plan(self, ScalingPlanName: str, ScalingPlanVersion: int) -> Dict[str, Any]:
        """
        [Client.delete_scaling_plan documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.delete_scaling_plan)
        """

    def describe_scaling_plan_resources(
        self,
        ScalingPlanName: str,
        ScalingPlanVersion: int,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> DescribeScalingPlanResourcesResponseTypeDef:
        """
        [Client.describe_scaling_plan_resources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.describe_scaling_plan_resources)
        """

    def describe_scaling_plans(
        self,
        ScalingPlanNames: List[str] = None,
        ScalingPlanVersion: int = None,
        ApplicationSources: List[ApplicationSourceTypeDef] = None,
        MaxResults: int = None,
        NextToken: str = None,
    ) -> DescribeScalingPlansResponseTypeDef:
        """
        [Client.describe_scaling_plans documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.describe_scaling_plans)
        """

    def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Dict[str, Any] = None,
        ExpiresIn: int = 3600,
        HttpMethod: str = None,
    ) -> str:
        """
        [Client.generate_presigned_url documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.generate_presigned_url)
        """

    def get_scaling_plan_resource_forecast_data(
        self,
        ScalingPlanName: str,
        ScalingPlanVersion: int,
        ServiceNamespace: Literal["autoscaling", "ecs", "ec2", "rds", "dynamodb"],
        ResourceId: str,
        ScalableDimension: Literal[
            "autoscaling:autoScalingGroup:DesiredCapacity",
            "ecs:service:DesiredCount",
            "ec2:spot-fleet-request:TargetCapacity",
            "rds:cluster:ReadReplicaCount",
            "dynamodb:table:ReadCapacityUnits",
            "dynamodb:table:WriteCapacityUnits",
            "dynamodb:index:ReadCapacityUnits",
            "dynamodb:index:WriteCapacityUnits",
        ],
        ForecastDataType: Literal[
            "CapacityForecast",
            "LoadForecast",
            "ScheduledActionMinCapacity",
            "ScheduledActionMaxCapacity",
        ],
        StartTime: datetime,
        EndTime: datetime,
    ) -> GetScalingPlanResourceForecastDataResponseTypeDef:
        """
        [Client.get_scaling_plan_resource_forecast_data documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_scaling_plan_resource_forecast_data)
        """

    def update_scaling_plan(
        self,
        ScalingPlanName: str,
        ScalingPlanVersion: int,
        ApplicationSource: ApplicationSourceTypeDef = None,
        ScalingInstructions: List[ScalingInstructionTypeDef] = None,
    ) -> Dict[str, Any]:
        """
        [Client.update_scaling_plan documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.update_scaling_plan)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_plan_resources"]
    ) -> DescribeScalingPlanResourcesPaginator:
        """
        [Paginator.DescribeScalingPlanResources documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Paginator.DescribeScalingPlanResources)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_plans"]
    ) -> DescribeScalingPlansPaginator:
        """
        [Paginator.DescribeScalingPlans documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/autoscaling-plans.html#AutoScalingPlans.Paginator.DescribeScalingPlans)
        """
