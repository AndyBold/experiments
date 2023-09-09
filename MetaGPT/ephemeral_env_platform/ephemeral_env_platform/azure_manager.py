from azure.mgmt.resource import ResourceManagementClient
from azure.identity import DefaultAzureCredential
from .models import Environment
import os

class AzureManager:

    def __init__(self):
        self.credential = DefaultAzureCredential()
        self.subscription_id = os.getenv('AZURE_SUBSCRIPTION_ID')
        if not self.subscription_id:
            raise ValueError("AZURE_SUBSCRIPTION_ID is not set in environment variables")
        self.client = ResourceManagementClient(self.credential, self.subscription_id)

    def setup_environment(self, environment: Environment):
        """
        Sets up resources for the given environment on Azure.
        """
        try:
            resource_group_name = f"{environment.project.name}-{environment.name}"
            resource_group = self.client.resource_groups.create_or_update(
                resource_group_name,
                {
                    "location": "westus"
                }
            )
            environment.status = "setup"
            return resource_group
        except Exception as e:
            print(f"Failed to setup environment: {e}")
            return None

    def destroy_environment(self, environment: Environment):
        """
        Destroys resources associated with the given environment on Azure.
        """
        try:
            resource_group_name = f"{environment.project.name}-{environment.name}"
            async_delete = self.client.resource_groups.begin_delete(resource_group_name)
            async_delete.result()
            environment.status = "destroyed"
            return async_delete.status()
        except Exception as e:
            print(f"Failed to destroy environment: {e}")
            return None

    def check_environment_status(self, environment: Environment):
        """
        Checks the status of the given environment on Azure.
        """
        try:
            resource_group_name = f"{environment.project.name}-{environment.name}"
            resource_group = self.client.resource_groups.get(resource_group_name)
            return resource_group.properties.provisioning_state
        except Exception as e:
            print(f"Failed to check environment status: {e}")
            return None
