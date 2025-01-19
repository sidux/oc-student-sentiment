resource "azurerm_resource_group" "main" {
  name     = "OC-Student"
  location = "westeurope"
}

# App Service Plan
resource "azurerm_service_plan" "main" {
  name                = "oc-student-sentiment-plan"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  sku_name            = "B1"
  os_type             = "Linux"
}

# Azure Container Registry (ACR)
resource "azurerm_container_registry" "main" {
  admin_enabled       = true
  location            = "westeurope"
  name                = "alocpath"
  resource_group_name = "OC-Student"
  sku                 = "Basic"
  depends_on = [
    azurerm_resource_group.main,
  ]
}

# Log Analytics Workspace
resource "azurerm_log_analytics_workspace" "main" {
  name                = "oc-student-sentiment-law"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  depends_on = [
    azurerm_resource_group.main,
  ]
}

# Linux Web App (Updated from azurerm_app_service)
resource "azurerm_linux_web_app" "main" {
  name                = "oc-student-sentiment-app"
  location            = azurerm_resource_group.main.location
  resource_group_name = azurerm_resource_group.main.name
  service_plan_id     = azurerm_service_plan.main.id

  site_config {
    always_on = true
    application_stack {
      docker_image     = "alocpath.azurecr.io/oc-student-sentiment"
      docker_image_tag = "latest"
    }
  }

  app_settings = {
    "WEBSITES_ENABLE_APP_SERVICE_STORAGE"   = "true"
    "DOCKER_REGISTRY_SERVER_URL"            = "https://alocpath.azurecr.io"
    "DOCKER_REGISTRY_SERVER_USERNAME"       = azurerm_container_registry.main.admin_username
    "DOCKER_REGISTRY_SERVER_PASSWORD"       = azurerm_container_registry.main.admin_password
    "APPINSIGHTS_INSTRUMENTATIONKEY"        = azurerm_application_insights.main.instrumentation_key
    "APPLICATIONINSIGHTS_CONNECTION_STRING" = azurerm_application_insights.main.connection_string
  }
}

resource "azurerm_application_insights" "main" {
  application_type    = "web"
  location            = azurerm_resource_group.main.location
  name                = "oc-student-sentiment"
  resource_group_name = azurerm_resource_group.main.name
  sampling_percentage = 0
  workspace_id        = "/subscriptions/61585847-8d6c-4085-ac31-453a9f6b8938/resourceGroups/DefaultResourceGroup-WEU/providers/Microsoft.OperationalInsights/workspaces/DefaultWorkspace-61585847-8d6c-4085-ac31-453a9f6b8938-WEU"
  depends_on = [
    azurerm_resource_group.main,
  ]
}

resource "azurerm_monitor_scheduled_query_rules_alert_v2" "main" {
  display_name         = "negative feedback"
  evaluation_frequency = "PT5M"
  location             = "westeurope"
  name                 = "negative feedback"
  resource_group_name  = "OC-Student"
  scopes = [
    azurerm_application_insights.main.id,
  ]
  severity              = 3
  target_resource_types = ["microsoft.insights/components"]
  window_duration       = "PT5M"
  criteria {
    operator                = "GreaterThan"
    query                   = "traces\n| where customDimensions.correct == \"False\"\n"
    threshold               = 3
    time_aggregation_method = "Count"
    failing_periods {
      minimum_failing_periods_to_trigger_alert = 1
      number_of_evaluation_periods             = 1
    }
  }
  depends_on = [
    azurerm_application_insights.main,
  ]
}