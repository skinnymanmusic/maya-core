# Azure CLI Installation Guide

## Option 1: MSI Installer (Recommended - Easiest)

1. Download the MSI installer:
   https://aka.ms/installazurecliwindowsx64

2. Double-click the downloaded file to install

3. Restart your terminal after installation

4. Verify installation:
   ```bash
   az --version
   ```

---

## Option 2: PowerShell (Admin)

1. Open PowerShell as Administrator

2. Run this command:
   ```powershell
   $ProgressPreference = 'SilentlyContinue'; Invoke-WebRequest -Uri https://aka.ms/installazurecliwindowsx64 -OutFile .\AzureCLI.msi; Start-Process msiexec.exe -Wait -ArgumentList '/I AzureCLI.msi /quiet'; Remove-Item .\AzureCLI.msi
   ```

3. Restart your terminal

4. Verify installation:
   ```bash
   az --version
   ```

---

## Option 3: Chocolatey (Admin)

1. Open Command Prompt as Administrator

2. Run:
   ```bash
   choco install azure-cli -y
   ```

3. Restart your terminal

4. Verify installation:
   ```bash
   az --version
   ```

---

## After Installation

### Login to Azure
```bash
az login
```
This will open a browser window for authentication.

### Verify Login
```bash
az account show
```

### List Your Subscriptions
```bash
az account list --output table
```

### Set Default Subscription (if needed)
```bash
az account set --subscription "YOUR_SUBSCRIPTION_ID"
```

---

## Common Azure CLI Commands

### Resource Groups
```bash
# List resource groups
az group list --output table

# Create resource group
az group create --name myResourceGroup --location eastus
```

### Web Apps
```bash
# List web apps
az webapp list --output table

# Create web app
az webapp create --resource-group myResourceGroup --plan myAppServicePlan --name myUniqueAppName
```

### Storage
```bash
# List storage accounts
az storage account list --output table
```

### Container Apps
```bash
# List container apps
az containerapp list --output table
```

---

## Troubleshooting

### Command not found after installation
- Restart your terminal completely
- Check PATH: Azure CLI should be in `C:\Program Files\Microsoft SDKs\Azure\CLI2\wbin`

### Login issues
- Make sure you have a Microsoft/Azure account
- Try `az login --use-device-code` if browser doesn't open

---

**Next Steps After Installation:**
1. Run `az login` to authenticate
2. Run `az account show` to verify your subscription
3. You're ready to deploy to Azure!
