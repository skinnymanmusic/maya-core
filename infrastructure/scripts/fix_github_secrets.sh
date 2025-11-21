#!/bin/bash

# STEP 0 — SAFETY
# Exit if any command fails
set -e

GH="/c/Program Files/GitHub CLI/gh.exe"

echo "=== FIXING GITHUB → AZURE OIDC SECRETS & WORKFLOW ==="

# STEP 1 — VERIFY GITHUB CLI LOGIN
echo "Checking GitHub CLI login..."
"$GH" auth status || "$GH" auth login

# STEP 2 — VERIFY AZURE CLI LOGIN
echo "Checking Azure CLI login..."
az account show || az login

# STEP 3 — COLLECT REQUIRED AZURE VALUES
echo "Collecting Azure values..."
TENANT_ID=$(az account show --query tenantId -o tsv)
SUBSCRIPTION_ID=$(az account show --query id -o tsv)

# Find the service principal created for GitHub deploy
APP_NAME="maya-github-deploy"
echo "Retrieving App Registration Client ID..."
CLIENT_ID=$(az ad app list --display-name $APP_NAME --query "[0].appId" -o tsv)

if [ -z "$CLIENT_ID" ]; then
  echo "ERROR: Could not find App Registration '$APP_NAME'."
  exit 1
fi

echo "  ✓ CLIENT_ID = $CLIENT_ID"
echo "  ✓ TENANT_ID = $TENANT_ID"
echo "  ✓ SUBSCRIPTION_ID = $SUBSCRIPTION_ID"

# STEP 4 — WRITE GITHUB SECRETS (Repository Scope)
echo "Updating GitHub repository secrets..."
REPO="skinnymanmusic/maya-core"

"$GH" secret set AZURE_CLIENT_ID          --repo $REPO <<< "$CLIENT_ID"
"$GH" secret set AZURE_TENANT_ID          --repo $REPO <<< "$TENANT_ID"
"$GH" secret set AZURE_SUBSCRIPTION_ID    --repo $REPO <<< "$SUBSCRIPTION_ID"

echo "✓ Secrets updated!"

# STEP 5 — FIX WORKFLOW IF NEEDED
echo "Checking workflow files..."
mkdir -p .github/workflows

cat > .github/workflows/deploy.yml << 'EOF'
name: Deploy Maya Core Function App

on:
  push:
    branches: [ main ]

jobs:
  build-and-deploy:
    runs-on: ubuntu-latest
    permissions:
      id-token: write
      contents: read

    steps:
      - name: Azure Login (OIDC)
        uses: azure/login@v2
        with:
          client-id: ${{ secrets.AZURE_CLIENT_ID }}
          tenant-id: ${{ secrets.AZURE_TENANT_ID }}
          subscription-id: ${{ secrets.AZURE_SUBSCRIPTION_ID }}

      - name: Checkout repository
        uses: actions/checkout@v3

      - name: Set up Node.js
        uses: actions/setup-node@v3
        with:
          node-version: 20

      - name: Install dependencies
        run: npm install
        working-directory: api

      - name: Deploy to Azure Function App
        uses: azure/functions-action@v1
        with:
          app-name: maya-core-func
          package: api
EOF

echo "✓ Workflow file repaired"

# STEP 6 — COMMIT & PUSH FIX
git add .github/workflows/deploy.yml
git commit -m "Auto-fix OIDC secrets + workflow"
git push

echo "=== FIX COMPLETE — GitHub Actions will run automatically ==="
