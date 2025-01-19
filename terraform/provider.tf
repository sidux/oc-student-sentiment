terraform {
  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 3.0.0, < 4.0.0"
    }
  }
}

provider "azurerm" {
  features {}
  # Use the environment variables for authentication
  client_id       = var.client_id       # Maps to "clientId" in the AZURE_CREDENTIALS secret
  client_secret   = var.client_secret   # Maps to "clientSecret" in the AZURE_CREDENTIALS secret
  subscription_id = var.subscription_id # Maps to "subscriptionId" in the AZURE_CREDENTIALS secret
  tenant_id       = var.tenant_id       # Maps to "tenantId" in the AZURE_CREDENTIALS secret
}
