# Maya Repository Restructure - Safety System

## 🎯 QUICK START (Just 3 Clicks!)

### Step 1: Preview Changes (No Risk)
```
Double-click: restructure_preview.bat
```
This shows what will change WITHOUT touching anything.

### Step 2: Execute Restructure (Safe - Has Undo)
```
Double-click: restructure_execute.bat
```
This does the actual restructure with full safety backups.

### Step 3: If You Need to Undo
```
Double-click: restructure_undo.bat
```
This restores everything exactly as it was before.

---

## 🛡️ SAFETY FEATURES

### ✅ What Protects You:

1. **Complete Backup** - Everything saved before ANY changes
2. **Pre-flight Checks** - Validates repository is ready
3. **Transaction-Based** - All changes succeed or all fail
4. **Auto-Updates** - Import paths automatically fixed
5. **Post-Validation** - Ensures nothing broke
6. **One-Command Undo** - Complete rollback anytime

### 📦 Backup System:
- Backups stored in: `.restructure_backups/`
- Timestamped: `backup_YYYYMMDD_HHMMSS/`
- Includes checksums for integrity verification
- Never deleted automatically

---

## 📁 WHAT GETS REORGANIZED

### Legacy Code → `_archive/`
Moves these to archive:
- `api/` - Legacy Azure Functions API
- `dashboard/` - Legacy dashboard frontend  
- `dev-portal/` - Legacy dev portal
- `deploy_tmp/` - Temporary deployment files
- `functions/` - Legacy Azure Functions
- `legacy_v3_functions/` - Legacy v3 functions
- `shared/` - Legacy shared code

### Reports & Docs → `_reports/`
Moves these to reports:
- All PHASE_*.md files
- All handoff documents
- All analysis reports
- All deployment guides
- Archive directories (PHASE_1_SUPABASE, etc.)
- Zip files

### Scripts → `scripts/`
Organizes into subdirectories:
- `scripts/setup/` - Setup scripts
- `scripts/deployment/` - Deployment scripts
- `scripts/diagnostics/` - Diagnostic tools
- `scripts/maintenance/` - Cleanup and maintenance

### Services → `services/`
Renames microservices:
- `backend/` → `services/backend/`
- `nova-backend/` → `services/nova/`
- `eli-backend/` → `services/eli/`

---

## 🔧 ADVANCED USAGE (Command Line)

### Preview Changes
```bash
python scripts/maintenance/restructure_repo.py --dry-run
```

### Execute Restructure
```bash
python scripts/maintenance/restructure_repo.py --execute
```

### Undo Restructure
```bash
python scripts/maintenance/undo_restructure.py
```

### Check Structure Integrity
```bash
python scripts/maintenance/structure_integrity_checker.py
```

### List Available Backups
```bash
python scripts/maintenance/undo_restructure.py --list
```

### Restore Specific Backup
```bash
python scripts/maintenance/undo_restructure.py backup_20250127_143022
```

---

## 📊 WHAT HAPPENS DURING RESTRUCTURE

### Phase 1: Pre-Flight Validation
- ✓ Checks git repository status
- ✓ Verifies required directories exist
- ✓ Validates Python syntax
- ✓ Checks disk space
- ✓ Ensures backend tests are present

### Phase 2: Backup Creation
- ✓ Creates timestamped backup
- ✓ Copies all files and directories
- ✓ Calculates checksums
- ✓ Saves metadata

### Phase 3: Reference Scanning
- ✓ Scans Python imports
- ✓ Scans config files
- ✓ Scans documentation
- ✓ Scans scripts

### Phase 4: Execute Moves
- ✓ Creates new directories
- ✓ Moves legacy code to archive
- ✓ Moves reports to _reports
- ✓ Organizes scripts by type
- ✓ Renames service directories

### Phase 5: Update References
- ✓ Updates Python imports
- ✓ Updates config paths
- ✓ Updates documentation links

### Phase 6: Post-Validation
- ✓ Verifies new structure
- ✓ Checks imports still work
- ✓ Validates no broken paths
- ✓ Ensures essential files present

### Phase 7: Cleanup
- ✓ Removes empty directories
- ✓ Cleans temporary files

---

## 🆘 TROUBLESHOOTING

### If Preview Shows Unexpected Changes:
1. Don't execute! Review the dry-run output
2. Report what looks wrong
3. We can adjust the plan before executing

### If Execute Fails:
1. Don't panic! Everything is backed up
2. Run: `restructure_undo.bat`
3. Everything will be restored

### If You're Unsure:
1. Run: `check_structure.bat` to see current state
2. Run: `restructure_preview.bat` to see what would change
3. Ask questions before executing!

---

## 🔒 INTEGRITY MODE (Automatic Enforcement)

After restructure completes, these prevent future disorganization:

### Pre-Commit Hook (Future)
Will automatically check structure before allowing commits.

### CI/CD Workflow (Future)
GitHub Action that validates structure on every PR.

### Structure Checker (Available Now)
```
check_structure.bat
```
Run anytime to validate organization.

---

## 📋 FILES CREATED

### Batch Files (Windows - Double-Click These!)
- `restructure_preview.bat` - Preview changes
- `restructure_execute.bat` - Execute restructure
- `restructure_undo.bat` - Undo/rollback
- `check_structure.bat` - Check current structure

### Python Scripts (Under scripts/maintenance/)
- `restructure_repo.py` - Main orchestrator
- `undo_restructure.py` - Rollback system
- `backup_manager.py` - Backup creation/verification
- `reference_scanner.py` - Finds all references
- `validator.py` - Pre/post validation
- `structure_integrity_checker.py` - Structure validation

---

## 💡 BEST PRACTICES

### Before Restructuring:
1. ✓ Commit or stash any work in progress
2. ✓ Run `restructure_preview.bat` first
3. ✓ Review what will change
4. ✓ Make sure you have disk space

### After Restructuring:
1. ✓ Test your backend still works
2. ✓ Check imports resolve correctly
3. ✓ Run your test suite
4. ✓ Keep backup until you're confident

### Maintaining Organization:
1. ✓ Run `check_structure.bat` periodically
2. ✓ Put new reports in `_reports/`
3. ✓ Put new scripts in `scripts/`
4. ✓ Archive old code in `_archive/`

---

## 🎓 UNDERSTANDING THE SYSTEM

### Why This Approach?
- **Safety First** - Can't break what's backed up
- **Automation** - Humans make mistakes, scripts don't
- **Validation** - Checks before AND after
- **Reversible** - One command undoes everything

### What Makes It Safe?
1. **Immutable Backups** - Original files never touched until move
2. **Checksums** - Verify backup integrity
3. **Transaction-Based** - All or nothing approach
4. **Multiple Validations** - Catches issues early

### When to Undo?
- Tests fail after restructure
- Imports break
- Something doesn't work right
- You change your mind
- Anything feels wrong

---

## 📞 NEED HELP?

If anything goes wrong or you're unsure:

1. **Don't Panic** - Everything is backed up
2. **Don't Continue** - Stop if errors appear
3. **Run Undo** - `restructure_undo.bat` restores everything
4. **Ask Questions** - Better safe than sorry

---

## ✨ FINAL NOTES

This system was built with the "git reset disaster" in mind. It's designed to be:
- **Foolproof** - Hard to accidentally break things
- **Reversible** - Easy to undo if needed
- **Automated** - Minimal manual work
- **Safe** - Multiple layers of protection

**Remember:** It's always safer to run `restructure_preview.bat` first!

---

**Created:** 2025-01-27
**Version:** 1.0
**For:** MayAssistant (Maya) by Skinny
