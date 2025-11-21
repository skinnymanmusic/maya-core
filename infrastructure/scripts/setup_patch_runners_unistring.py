# setup_patch_runners_final.py
# -----------------------------------------------------------
# OMEGA 4.0 — Patch Runner Installer (Unistring, Tested)
# -----------------------------------------------------------

from pathlib import Path
from datetime import datetime

ROOT = Path(__file__).resolve().parent
SCRIPTS = ROOT / "scripts"
SCRIPTS.mkdir(exist_ok=True)

# ONE big string that contains all 3 patch scripts
UNISTRING = """
===FILE:run_backend_patch.py===
# OMEGA Backend Patch Runner
import os, subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "backend"
SCRIPTS = ROOT / "scripts"

def run(cmd, cwd=None):
    print(f"\\n>>> {cmd}")
    return subprocess.run(cmd, shell=True, cwd=cwd, text=True)

print("\\n=== BACKEND PATCH RUNNER ===")

# 1) Run email_hash migration if present
if (SCRIPTS / "apply_email_hash_migration.py").exists():
    run("python apply_email_hash_migration.py", cwd=SCRIPTS)

# 2) Run schema drift checker if present
if (SCRIPTS / "startup_schema_check.py").exists():
    run("python startup_schema_check.py", cwd=SCRIPTS)

# 3) Run backend tests (Phase 1 Day 2) if present
tests = BACKEND / "scripts" / "dev" / "test_phase1_day2.py"
if tests.exists():
    run("python test_phase1_day2.py", cwd=tests.parent)

# 4) Run pip-audit (dependency vulnerabilities)
run("pip install pip-audit")
run("pip-audit", cwd=BACKEND)

# 5) Run Trivy filesystem scan (HIGH/CRITICAL)
run("trivy fs . --exit-code 0 --severity HIGH,CRITICAL", cwd=BACKEND)

print("\\n=== BACKEND PATCH COMPLETE ===")

===FILE:run_frontend_patch.py===
# OMEGA Frontend Patch Runner
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONTEND = ROOT / "omega-frontend"

def run(cmd, cwd=None):
    print(f"\\n>>> {cmd}")
    return subprocess.run(cmd, shell=True, cwd=cwd, text=True)

print("\\n=== FRONTEND PATCH RUNNER ===")

# 1) Ensure dependencies are installed
run("npm install", cwd=FRONTEND)

# 2) Run frontend tests (if test script exists)
run("npm test --if-present", cwd=FRONTEND)

# 3) Run npm audit (high severity and above)
run("npm audit --audit-level=high", cwd=FRONTEND)

# 4) Run Trivy filesystem scan (HIGH/CRITICAL)
run("trivy fs . --exit-code 0 --severity HIGH,CRITICAL", cwd=FRONTEND)

print("\\n=== FRONTEND PATCH COMPLETE ===")

===FILE:run_all_patches.py===
# OMEGA Solin Master Patch Runner
from pathlib import Path
import subprocess
from datetime import datetime

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"
LOG = ROOT / "CLAUDE_CODE_LOG.md"

def run(cmd, cwd=None):
    print(f"\\n>>> {cmd}")
    p = subprocess.run(cmd, shell=True, cwd=cwd, text=True, capture_output=True)
    return p.returncode, p.stdout + p.stderr

print("\\n=== RUNNING FULL OMEGA PATCH SUITE ===")

results = {}

# Backend patch
results["backend"], out_backend = run("python run_backend_patch.py", cwd=SCRIPTS)

# Frontend patch
results["frontend"], out_frontend = run("python run_frontend_patch.py", cwd=SCRIPTS)

# Schema drift checker (if available)
drift_script = SCRIPTS / "startup_schema_check.py"
if drift_script.exists():
    results["schema"], out_schema = run("python startup_schema_check.py", cwd=SCRIPTS)
else:
    out_schema = "Schema drift script missing."

# Build log entry (no triple quotes to avoid parser issues)
timestamp = datetime.utcnow().isoformat() + "Z"

lines = []
lines.append('---')
lines.append('## ' + timestamp + ' — Solin Patch Runner')
lines.append('Backend Patch: ' + str(results.get("backend")))
lines.append('Frontend Patch: ' + str(results.get("frontend")))
lines.append('Schema Drift: ' + str(results.get("schema", "n/a")))
lines.append('')
lines.append('### Backend Output')
lines.append(out_backend[-800:])
lines.append('')
lines.append('### Frontend Output')
lines.append(out_frontend[-800:])
lines.append('')
lines.append('### Schema Drift Output')
lines.append(out_schema[-800:])
entry = "\\n".join(lines)

with open(LOG, "a", encoding="utf-8") as f:
    f.write(entry + "\\n")

print("\\n=== FULL PATCH SUITE COMPLETE ===")
print("Logged to CLAUDE_CODE_LOG.md")
"""

# ===== Write files out from the unistring =====

print("\n=== Installing OMEGA Patch Runners (final) ===")

blocks = UNISTRING.split("===FILE:")
for block in blocks:
    block = block.strip()
    if not block:
        continue
    name, content = block.split("===", 1)
    name = name.strip()
    content = content.strip()
    target = SCRIPTS / name
    target.write_text(content, encoding="utf-8")
    print(f"[OK] wrote {target}")

print("\n=== Done ===")
print("Run any of:")
print("  python scripts/run_backend_patch.py")
print("  python scripts/run_frontend_patch.py")
print("  python scripts/run_all_patches.py   # Solin master runner")
print("Timestamp:", datetime.utcnow().isoformat() + "Z")
