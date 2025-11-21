# SAFETY RULES — Gilman Accords Enforcement

Cursor MUST enforce:

- No hallucinated code.  
- No destructive DB migrations.  
- No writing secrets to files.  
- No auto-deployment unless triggered in the workflow.  
- No modifying environment variables.  
- No writing to `.env` files.  
- No auto-execution of shell commands unless user-approved.  
- No attempts to run Node/Python commands without permission.

Cursor MUST label any irreversible action with:

⚠️ “This is a destructive action”  
and pause until user approval.
