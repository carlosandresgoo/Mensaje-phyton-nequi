provider "azurerm" {
  features {}
}

resource "azurerm_resource_group" "nequi_rg" {
  name     = "rg-nequi-microservices"
  location = "East US"
}

resource "azurerm_container_registry" "nequi_acr" {
  name                = "nequicontainerregistry"
  resource_group_name = azurerm_resource_group.nequi_rg.name
  location            = azurerm_resource_group.nequi_rg.location
  sku                 = "Basic"
  admin_enabled       = true
}

resource "azurerm_linux_web_app" "nequi_api" {
  name                = "nequi-messaging-api"
  resource_group_name = azurerm_resource_group.nequi_rg.name
  location            = azurerm_resource_group.nequi_rg.location
  service_plan_id     = azurerm_service_plan.nequi_plan.id

  site_config {
    application_stack {
      docker_image     = "nequicontainerregistry.azurecr.io/nequi-api"
      docker_image_tag = "latest"
    }
  }
}

resource "azurerm_service_plan" "nequi_plan" {
  name                = "nequi-service-plan"
  resource_group_name = azurerm_resource_group.nequi_rg.name
  location            = azurerm_resource_group.nequi_rg.location
  os_type             = "Linux"
  sku_name            = "B1"
}
