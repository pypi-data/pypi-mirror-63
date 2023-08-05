"""
Main interface for codedeploy service client waiters.

Usage::

    import boto3
    from mypy_boto3.codedeploy import (
        DeploymentSuccessfulWaiter,
    )

    client: CodeDeployClient = boto3.client("codedeploy")

    deployment_successful_waiter: DeploymentSuccessfulWaiter = client.get_waiter("deployment_successful")
"""
# pylint: disable=arguments-differ,redefined-outer-name,redefined-builtin
from typing import TYPE_CHECKING
from botocore.waiter import Waiter as Boto3Waiter
from mypy_boto3_codedeploy.type_defs import WaiterConfigTypeDef


__all__ = ("DeploymentSuccessfulWaiter",)


class DeploymentSuccessfulWaiter(Boto3Waiter):
    """
    [Waiter.DeploymentSuccessful documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/codedeploy.html#CodeDeploy.Waiter.DeploymentSuccessful)
    """

    def wait(self, deploymentId: str, WaiterConfig: WaiterConfigTypeDef = None) -> None:
        """
        [DeploymentSuccessful.wait documentation](https://boto3.amazonaws.com/v1/documentation/api/1.12.16/reference/services/codedeploy.html#CodeDeploy.Waiter.DeploymentSuccessful.wait)
        """
