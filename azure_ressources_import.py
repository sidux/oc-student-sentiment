import json

# Load your JSON data
resources_json = '''
[
  {
    "changedTime": "2025-01-11T17:55:31.519079+00:00",
    "createdTime": "2025-01-11T17:45:31.294592+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/microsoft.insights/components/oc-student-sentiment",
    "identity": null,
    "kind": "web",
    "location": "westeurope",
    "managedBy": null,
    "name": "oc-student-sentiment",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": null,
    "tags": {},
    "type": "microsoft.insights/components"
  },
  {
    "changedTime": "2025-01-11T18:05:35.614224+00:00",
    "createdTime": "2025-01-11T17:55:34.964888+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/microsoft.insights/actiongroups/Application Insights Smart Detection",
    "identity": null,
    "kind": null,
    "location": "global",
    "managedBy": null,
    "name": "Application Insights Smart Detection",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": null,
    "tags": null,
    "type": "microsoft.insights/actiongroups"
  },
  {
    "changedTime": "2025-01-12T11:51:52.235997+00:00",
    "createdTime": "2025-01-12T11:41:51.656413+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/microsoft.insights/scheduledqueryrules/negative feedback",
    "identity": null,
    "kind": null,
    "location": "westeurope",
    "managedBy": null,
    "name": "negative feedback",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": null,
    "systemData": {
      "createdAt": "2025-01-12T11:41:51.6842094Z",
      "createdBy": "b.amel.braiek@gmail.com",
      "createdByType": "User",
      "lastModifiedAt": "2025-01-12T11:46:40.6999925Z",
      "lastModifiedBy": "b.amel.braiek@gmail.com",
      "lastModifiedByType": "User"
    },
    "tags": {},
    "type": "microsoft.insights/scheduledqueryrules"
  },
  {
    "changedTime": "2025-01-18T22:01:10.642069+00:00",
    "createdTime": "2025-01-18T20:13:11.939940+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/Microsoft.ContainerRegistry/registries/alocpath",
    "identity": null,
    "kind": null,
    "location": "westeurope",
    "managedBy": null,
    "name": "alocpath",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": {
      "capacity": null,
      "family": null,
      "model": null,
      "name": "Basic",
      "size": null,
      "tier": "Basic"
    },
    "systemData": {
      "createdAt": "2025-01-18T20:13:11.9666144Z",
      "createdBy": "b.amel.braiek@gmail.com",
      "createdByType": "User",
      "lastModifiedAt": "2025-01-18T21:51:09.7376246Z",
      "lastModifiedBy": "b.amel.braiek@gmail.com",
      "lastModifiedByType": "User"
    },
    "tags": {},
    "type": "Microsoft.ContainerRegistry/registries"
  },
  {
    "changedTime": "2025-01-18T21:57:51.477439+00:00",
    "createdTime": "2025-01-18T21:47:51.243931+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/Microsoft.OperationalInsights/workspaces/oc-student-sentiment-law",
    "identity": null,
    "kind": null,
    "location": "westeurope",
    "managedBy": null,
    "name": "oc-student-sentiment-law",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": null,
    "tags": {},
    "type": "Microsoft.OperationalInsights/workspaces"
  },
  {
    "changedTime": "2025-01-18T21:57:52.182131+00:00",
    "createdTime": "2025-01-18T21:47:52.759715+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/Microsoft.Web/serverFarms/oc-student-sentiment-plan",
    "identity": null,
    "kind": "linux",
    "location": "westeurope",
    "managedBy": null,
    "name": "oc-student-sentiment-plan",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": {
      "capacity": 1,
      "family": "B",
      "model": null,
      "name": "B1",
      "size": "B1",
      "tier": "Basic"
    },
    "tags": null,
    "type": "Microsoft.Web/serverFarms"
  },
  {
    "changedTime": "2025-01-18T22:07:52.375602+00:00",
    "createdTime": "2025-01-18T21:57:27.891394+00:00",
    "extendedLocation": null,
    "id": "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/OC-Student/providers/Microsoft.Web/sites/oc-student-sentiment-app",
    "identity": null,
    "kind": "app,linux,container",
    "location": "westeurope",
    "managedBy": null,
    "name": "oc-student-sentiment-app",
    "plan": null,
    "properties": null,
    "provisioningState": "Succeeded",
    "resourceGroup": "OC-Student",
    "sku": null,
    "tags": {},
    "type": "Microsoft.Web/sites"
  }
]

'''

resources = json.loads(resources_json)

# Map Azure resource types to Terraform resource types
resource_type_mapping = {
    "microsoft.insights/components": "azurerm_application_insights",
    "microsoft.insights/actiongroups": "azurerm_monitor_action_group",
    "microsoft.insights/scheduledqueryrules": "azurerm_monitor_scheduled_query_rules_alert",
    "Microsoft.ContainerRegistry/registries": "azurerm_container_registry",
    "Microsoft.OperationalInsights/workspaces": "azurerm_log_analytics_workspace",
    "Microsoft.Web/serverFarms": "azurerm_service_plan",
    "Microsoft.Web/sites": "azurerm_app_service",
}

# Generate Terraform import commands
for resource in resources:
    resource_type = resource["type"]
    resource_id = resource["id"]
    resource_name = resource["name"]

    terraform_resource_type = resource_type_mapping.get(resource_type, None)
    if terraform_resource_type:
        print(f"terraform import {terraform_resource_type}.{resource_name} {resource_id}")
    else:
        print(f"# Unsupported resource type: {resource_type} (ID: {resource_id})")
