#!/bin/bash

GH="/c/Program Files/GitHub CLI/gh.exe"

echo "=== STEP 1: VERIFY GITHUB AUTH ==="
"$GH" auth status || "$GH" auth login

echo "=== STEP 2: VERIFY AZURE LOGIN ==="
az account show || az login

echo "=== STEP 3: COLLECT REQUIRED IDs FROM AZURE ==="
TENANT_ID=$(az account show --query tenantId -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Fetch your App Registration created earlier
APP_ID=$(az ad app list --display-name "maya-github-deploy" --query "[0].appId" -o tsv)

echo "Using:"
echo " Tenant ID: $TENANT_ID"
echo " Subscription ID: $SUBSCRIPTION_ID"
echo " Client ID (App Registration): $APP_ID"

echo "=== STEP 4: RESET GITHUB SECRETS IN maya-core repo ==="
"$GH" secret set AZURE_CLIENT_ID -R skinnymanmusic/maya-core -b "$APP_ID"
"$GH" secret set AZURE_TENANT_ID -R skinnymanmusic/maya-core -b "$TENANT_ID"
"$GH" secret set AZURE_SUBSCRIPTION_ID -R skinnymanmusic/maya-core -b "$SUBSCRIPTION_ID"

echo "=== STEP 5: VERIFY THE SECRETS EXIST ==="
echo "If these appear below, secrets are successfully set:"
"$GH" secret list -R skinnymanmusic/maya-core

echo "=== STEP 6: TRIGGER A NEW DEPLOYMENT ==="
"$GH" workflow run deploy.yml -R skinnymanmusic/maya-core

echo "=== ALL DONE. WATCH THE WORKFLOW RUN ON GITHUB. ==="
