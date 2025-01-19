output "app_service_url" {
  value = azurerm_linux_web_app.main.default_hostname
}

output "log_analytics_workspace_id" {
  value = azurerm_log_analytics_workspace.main.id
}

output "docker_registry_password" {
  value       = azurerm_container_registry.main.admin_password
  sensitive   = true
  description = "Sensitive password for Docker registry."
}

output "application_insights_id" {
  value = azurerm_application_insights.main.id
}