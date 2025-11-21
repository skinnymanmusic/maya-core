# VERSION SELECTOR RULE (AUTO-LOADED)
This rule ensures Cursor always uses the correct MayAssistant documentation version.

## RULE 1 — Detect versions
When this repository is opened:
- Read `/docs/VERSION.md`
- Identify the value of `CURRENT_VERSION: x.x`
- Treat that version as the canonical documentation suite

## RULE 2 — Load correct docs
After detecting the version `x.x`, Cursor must:
- Read all documentation files in `/docs`
- Cross-check that their internal version tags match `x.x`
- Build internal working memory based ONLY on version `x.x`

## RULE 3 — If multiple versions are found
If any files inside `/docs` contain version tags that do NOT match `CURRENT_VERSION`, Cursor must:
- Pause immediately
- Ask the user:  
  “Multiple documentation versions detected. Which one should I load?”
- Options must match the folders or tags found
- Do NOT auto-choose

## RULE 4 — Ignore legacy versions
Documentation sections or files tagged as:
- `v1.0`, `v1.1`, `v1.2`, etc.  
that do NOT match `CURRENT_VERSION` must be treated as:
- deprecated  
- historical  
- non-canonical  

They should NOT be used for:
- architecture reasoning  
- builds  
- code generation  
- planning  

## RULE 5 — Safety
Cursor must NOT:
- Modify `/docs/VERSION.md`
- Modify `/docs` files unless explicitly instructed
- Use hallucinated, deprecated, or conflicting documentation

## RULE 6 — Logs vs Canon
If the master historical log contains references to old versions:
- Cursor must respect them AS HISTORY ONLY
- Never treat them as current truth
- Use `CURRENT_VERSION` docs as the only authoritative source
