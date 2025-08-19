using './main.bicep'

param environmentName = readEnvironmentVariable('AZURE_ENV_NAME', 'development')
param location = readEnvironmentVariable('AZURE_LOCATION', 'westus')
param deploymentUserPrincipalId = readEnvironmentVariable('AZURE_PRINCIPAL_ID', '')
param webContainerExists = readEnvironmentVariable('SERVICE_WEB_CONTAINER_EXISTS', 'false') == 'true'
