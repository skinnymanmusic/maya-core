# Python 3.11 Runtime Fix for Railway Deployment

## Problem Summary
Railway recently updated their default Python runtime to 3.13. However, `asyncpg==0.29.0` (our PostgreSQL driver) does NOT support Python 3.13 yet because its C extensions haven't been updated. This causes the build to fail with:

```
error: command '/usr/bin/cc' failed with exit code 1
```

## Solution
Force Railway to use Python 3.11.9 explicitly through multiple enforcement mechanisms.

## Files Changed

### 1. `nixpacks.toml` (PRIMARY ENFORCEMENT)
**Changes:**
- Removed ambiguous `[python]` section that Railway was ignoring
- Explicitly use `python311` in nixPkgs
- All commands now explicitly call `python3.11` instead of generic `python3`
- Added required C extension libraries: zlib, libffi, openssl

**Why this matters:**
Railway's Nixpacks builder respects explicit python3.11 commands over generic python3.

### 2. `railway.json` (SECONDARY ENFORCEMENT)
**Changes:**
- Removed invalid `"pythonVersion"` field (not part of Railway schema)
- Added proper `nixpacksPlan` with explicit python311 package
- Start command now uses `python3.11 -m uvicorn` explicitly

**Why this matters:**
The nixpacksPlan inline configuration ensures Railway can't fall back to Python 3.13.

### 3. `.python-version` (ALREADY EXISTS - VERIFIED)
**Content:**
```
3.11.9
```

**Why this matters:**
Many Python tools respect this file for version pinning.

### 4. `runtime.txt` (NEW - ADDITIONAL ENFORCEMENT)
**Content:**
```
python-3.11.9
```

**Why this matters:**
Some PaaS platforms (including Railway in certain modes) respect runtime.txt.

### 5. `verify_python.sh` (NEW - DEBUGGING TOOL)
Verification script to check which Python version Railway actually uses during build.

## Deployment Instructions

### Step 1: Commit and Push
```bash
cd C:\Users\delin\maya-ai
git add backend/nixpacks.toml backend/railway.json backend/runtime.txt backend/verify_python.sh
git commit -m "Fix: Force Python 3.11 for asyncpg compatibility (Railway 3.13 breaks build)"
git push -u origin main
```

### Step 2: Monitor Railway Build
Watch for these success indicators:
```
✓ Using Python 3.11.9
✓ Successfully installed asyncpg-0.29.0
✓ Starting server...
```

### Step 3: If Build Still Fails
Check Railway build logs for:
- What Python version is actually being used
- Look for "Python 3.13" - if present, config was ignored
- Look for asyncpg compilation errors

## Why asyncpg Requires Python 3.11

`asyncpg` is a PostgreSQL driver with **C extensions** for performance. These C extensions:
- Are compiled during `pip install asyncpg`
- Must be built against Python's C API
- Python 3.13 changed the C API in ways asyncpg 0.29.0 doesn't support yet
- **asyncpg 0.30.0+ will support Python 3.13** (not released yet as of Nov 2024)

## Verification After Deployment

Once deployed, check Railway logs for:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Application startup complete.
```

If you see those lines, Python 3.11 is working and asyncpg compiled successfully.

## DO NOT Do These Things

❌ **DO NOT upgrade asyncpg** - newer versions aren't released yet
❌ **DO NOT remove asyncpg** - it's required for PostgreSQL async operations
❌ **DO NOT try to fix asyncpg code** - the issue is in C extensions, not Python code
❌ **DO NOT modify backend source code** - this is purely a runtime environment issue

## What to Do If This Still Fails

If Railway still uses Python 3.13 after this fix:
1. Check Railway dashboard → Settings → Environment
2. Look for any environment variables overriding Python version
3. Consider opening a Railway support ticket showing the explicit config being ignored

## Technical Deep Dive

Railway's build process hierarchy:
1. Checks for `nixpacks.toml` (highest priority)
2. Falls back to auto-detection if config is incomplete
3. Auto-detection now defaults to Python 3.13

Our fix ensures `nixpacks.toml` is **complete and authoritative** so Railway never falls back to auto-detection.

---

**Fix prepared by:** Claude (Solin/Vita collaboration)
**Date:** November 22, 2024
**Affects:** Railway deployment only (not local development)
