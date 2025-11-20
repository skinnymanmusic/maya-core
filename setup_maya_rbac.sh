#!/usr/bin/env bash
set -euo pipefail

SUBSCRIPTION_ID="8195bf9f-e930-4f0d-8236-9526882d6f32"
TENANT_ID="7f41cfaa-7c09-424e-b7dd-aec5d8d400d9"

RESOURCE_GROUP="maya-core"
APP_DISPLAY_NAME="maya-github-deploy"
GITHUB_OWNER="skinnymanmusic"
GITHUB_REPO="maya-core"
GITHUB_BRANCH="main"
FED_CRED_NAME="github-oidc"
ROLE_NAME="Contributor"

echo "Setting Azure subscription..."
az account set --subscription "$SUBSCRIPTION_ID"

echo "Creating or finding app registration..."
APP_ID=$(az ad app list --display-name "$APP_DISPLAY_NAME" --query '[0].appId' -o tsv)
if [[ -z "$APP_ID" ]]; then
  APP_ID=$(az ad app create --display-name "$APP_DISPLAY_NAME" --sign-in-audience AzureADMyOrg --query appId -o tsv)
fi

echo "Creating or finding Service Principal..."
SP_ID=$(az ad sp list --filter "appId eq '$APP_ID'" --query '[0].id' -o tsv)
if [[ -z "$SP_ID" ]]; then
  SP_ID=$(az ad sp create --id "$APP_ID" --query id -o tsv)
fi

echo "Checking federated credential..."
CRED_COUNT=$(az ad app federated-credential list --id "$APP_ID" --query "length([?subject=='repo:${GITHUB_OWNER}/${GITHUB_REPO}:ref:refs/heads/${GITHUB_BRANCH}'])" -o tsv)
if [[ "$CRED_COUNT" == "0" ]]; then
  echo "  Creating new federated credential..."
  az ad app federated-credential create \
    --id "$APP_ID" \
    --parameters "{
      \"name\": \"${FED_CRED_NAME}\",
      \"issuer\": \"https://token.actions.githubusercontent.com\",
      \"subject\": \"repo:${GITHUB_OWNER}/${GITHUB_REPO}:ref:refs/heads/${GITHUB_BRANCH}\",
      \"audiences\": [\"api://AzureADTokenExchange\"]
    }" || echo "  Credential may already exist, continuing..."
else
  echo "  Federated credential already exists for this subject."
fi

echo "Assigning Contributor role on resource group..."
SCOPE="/subscriptions/${SUBSCRIPTION_ID}/resourceGroups/${RESOURCE_GROUP}"
az role assignment create \
  --assignee-object-id "$SP_ID" \
  --assignee-principal-type ServicePrincipal \
  --role "$ROLE_NAME" \
  --scope "$SCOPE" 2>/dev/null || echo "  Role assignment may already exist or requires portal assignment."

echo ""
echo "============================================"
echo "RBAC setup complete."
echo "============================================"
echo "CLIENT_ID=$APP_ID"
echo "TENANT_ID=$TENANT_ID"
echo "SUBSCRIPTION_ID=$SUBSCRIPTION_ID"
echo "============================================"
