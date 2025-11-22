"""
Create handoff folder structure
"""
from pathlib import Path

repo_root = Path(r"C:\Users\delin\maya-ai")
handoff_base = repo_root / "handoff"

# AI assistants
ais = ["solin", "claude", "code", "cursor", "copilot"]

# Create all subdirectories
for ai in ais:
    ai_dir = handoff_base / ai
    
    # Create fromskinny folder
    (ai_dir / "fromskinny").mkdir(parents=True, exist_ok=True)
    
    # Create to[other_ai] folders
    for other_ai in ais:
        if other_ai != ai:
            (ai_dir / f"to{other_ai}").mkdir(parents=True, exist_ok=True)

print("✅ All handoff directories created!")

# Print structure
print("\n📂 Created structure:")
for ai in ais:
    print(f"\nhandoff/{ai}/")
    print(f"  ├── fromskinny/")
    for other_ai in ais:
        if other_ai != ai:
            print(f"  └── to{other_ai}/")
