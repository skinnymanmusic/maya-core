#!/bin/bash

# ======================================================
# MayAssistant — Railway Environment Setup Script
# AUTOMATED ENV VARIABLE INITIALIZATION (SOLIN v2)
# ======================================================
# SAFE • IDEMPOTENT • RE-RUNNABLE
# This script will set ALL required Railway environment
# variables for the MayAssistant backend.
#
# Only ANTHROPIC_API_KEY and GMAIL fields require manual
# input once generated.
# ======================================================

echo "=== MayAssistant: Railway Environment Setup ==="

# --- Required Variables ---

echo ""
echo "[1/8] Setting DEFAULT_TENANT_ID..."
railway variables set DEFAULT_TENANT_ID="default"

echo ""
echo "[2/8] Setting DATABASE_URL (placeholder — update manually)..."
railway variables set DATABASE_URL="postgresql://UPDATE_ME:UPDATE_ME@UPDATE_ME:5432/postgres"

echo ""
echo "[3/8] Generating JWT_SECRET_KEY..."
JWT_SECRET_KEY=$(openssl rand -hex 32)
railway variables set JWT_SECRET_KEY="$JWT_SECRET_KEY"
echo "Generated JWT_SECRET_KEY: $JWT_SECRET_KEY"

echo ""
echo "[4/8] Generating ENCRYPTION_KEY (32-byte base64)..."
ENCRYPTION_KEY=$(openssl rand -base64 32)
railway variables set ENCRYPTION_KEY="$ENCRYPTION_KEY"
echo "Generated ENCRYPTION_KEY: $ENCRYPTION_KEY"

echo ""
echo "[5/8] Setting ANTHROPIC_API_KEY (placeholder — update manually)..."
railway variables set ANTHROPIC_API_KEY="UPDATE_ME"

echo ""
echo "[6/8] Setting GMAIL_WEBHOOK_URL (placeholder — update after Railway deploy exposes domain)..."
railway variables set GMAIL_WEBHOOK_URL="https://UPDATE_ME.railway.app/api/gmail/webhook"

echo ""
echo "[7/8] Setting GMAIL_PUBSUB_TOPIC (optional)..."
railway variables set GMAIL_PUBSUB_TOPIC=""

echo ""
echo "[8/8] Setting GMAIL_PUBSUB_SERVICE_ACCOUNT (optional)..."
railway variables set GMAIL_PUBSUB_SERVICE_ACCOUNT=""

echo ""
echo "======================================================="
echo " DONE! Environment variables initialized."
echo " IMPORTANT:"
echo " - Update DATABASE_URL after copying from Supabase."
echo " - Update ANTHROPIC_API_KEY after copying from Claude."
echo " - Update GMAIL_WEBHOOK_URL after Railway deploy."
echo "======================================================="

# END OF FILE

