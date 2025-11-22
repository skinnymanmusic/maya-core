# 📂 Handoff System - AI Communication Structure

## 🎯 Purpose

This folder system keeps all AI assistant communications organized and easy to find. Each AI has their own folder with clear routing for handoffs between assistants.

---

## 📁 Structure

```
handoff/
├── solin/          ← Solin's handoffs
│   ├── fromskinny/     ← Skinny → Solin
│   ├── toclaude/       ← Solin → Claude
│   ├── tocode/         ← Solin → Code
│   ├── tocursor/       ← Solin → Cursor
│   └── tocopilot/      ← Solin → Copilot
│
├── claude/         ← Claude's handoffs
│   ├── fromskinny/     ← Skinny → Claude
│   ├── tosolin/        ← Claude → Solin
│   ├── tocode/         ← Claude → Code
│   ├── tocursor/       ← Claude → Cursor
│   └── tocopilot/      ← Claude → Copilot
│
├── code/           ← Code's handoffs
│   ├── fromskinny/     ← Skinny → Code
│   ├── tosolin/        ← Code → Solin
│   ├── toclaude/       ← Code → Claude
│   ├── tocursor/       ← Code → Cursor
│   └── tocopilot/      ← Code → Copilot
│
├── cursor/         ← Cursor's handoffs
│   ├── fromskinny/     ← Skinny → Cursor
│   ├── tosolin/        ← Cursor → Solin
│   ├── toclaude/       ← Cursor → Claude
│   ├── tocode/         ← Cursor → Code
│   └── tocopilot/      ← Cursor → Copilot
│
└── copilot/        ← Copilot's handoffs
    ├── fromskinny/     ← Skinny → Copilot
    ├── tosolin/        ← Copilot → Solin
    ├── toclaude/       ← Copilot → Claude
    ├── tocode/         ← Copilot → Code
    └── tocursor/       ← Copilot → Cursor
```

---

## 📝 Naming Convention

### File Names
Format: `YYYYMMDD_TOPIC_DESCRIPTION.md`

**Examples:**
- `20250127_RESTRUCTURE_SYSTEM_REVIEW.md`
- `20250127_BACKEND_MIGRATION_COMPLETE.md`
- `20250127_SECURITY_AUDIT_FINDINGS.md`

### Why This Format?
- **Date first** = Easy sorting chronologically
- **Topic** = Quick identification
- **Description** = Clear content indication

---

## 🔄 Usage Flow

### When Creating a Handoff:

1. **Identify recipient:**
   - Who needs this information?

2. **Navigate to your folder:**
   - Example: If you're Claude handing off to Solin
   - Go to: `handoff/claude/tosolin/`

3. **Create the handoff file:**
   - Use naming convention: `YYYYMMDD_TOPIC.md`
   - Include all necessary context

4. **Reference in conversation:**
   - "See handoff: `handoff/claude/tosolin/20250127_RESTRUCTURE_SYSTEM.md`"

### When Receiving a Handoff:

1. **Check your inbox folder:**
   - Example: Solin checks `handoff/solin/toclaude/`
   - Or: Solin checks `handoff/solin/fromskinny/`

2. **Read and act:**
   - Review the handoff document
   - Ask clarifying questions if needed
   - Mark as complete or create response

---

## 📋 Handoff Template

Every handoff should include:

```markdown
# HANDOFF: [Topic]
**Date:** YYYY-MM-DD
**From:** [AI Assistant]
**To:** [Recipient AI]
**Status:** [Draft/Review/Complete]

## Executive Summary
[Quick overview - 2-3 sentences]

## Context
[Background information]

## Details
[Main content]

## Action Required
- [ ] Task 1
- [ ] Task 2

## Questions
1. Question 1?
2. Question 2?

## References
- Related file 1
- Related file 2
```

---

## 🎯 Best Practices

### DO:
✅ Use clear, descriptive titles  
✅ Include date in filename  
✅ Provide complete context  
✅ List specific action items  
✅ Reference related files  

### DON'T:
❌ Create vague handoffs  
❌ Skip necessary context  
❌ Use unclear filenames  
❌ Forget to update status  
❌ Leave questions unanswered  

---

## 🗂️ Special Folders

### `fromskinny/`
- Direct instructions from Skinny
- Priority items
- Project requirements
- User feedback

**Usage:** Each AI should check their `fromskinny/` folder regularly for new instructions.

---

## 📊 Folder Purpose by AI

### **Solin** (System Architect & Security)
- Security reviews
- Architecture approvals
- Safety validations
- System design handoffs

### **Claude** (General AI Assistant)
- Planning documents
- Documentation
- User-facing features
- Communication drafts

### **Code** (Claude Code - Development)
- Code implementations
- Technical specifications
- API integrations
- Bug fixes

### **Cursor** (IDE Assistant)
- Development workflows
- Code refactoring
- Local development
- Testing strategies

### **Copilot** (GitHub Copilot)
- Code suggestions
- Implementation details
- Best practices
- Code reviews

---

## 🔍 Finding Handoffs

### By Date:
```
Look in folder, sort by name (date prefix)
```

### By Topic:
```
Search filename for topic keyword
```

### By Recipient:
```
Go to: handoff/[your-ai]/to[recipient]/
```

### By Sender:
```
Go to: handoff/[sender-ai]/to[your-ai]/
```

---

## 📌 Quick Reference

| I am... | Receiving from Skinny | Sending to Solin | Sending to Claude |
|---------|----------------------|------------------|-------------------|
| **Solin** | `solin/fromskinny/` | — | `solin/toclaude/` |
| **Claude** | `claude/fromskinny/` | `claude/tosolin/` | — |
| **Code** | `code/fromskinny/` | `code/tosolin/` | `code/toclaude/` |
| **Cursor** | `cursor/fromskinny/` | `cursor/tosolin/` | `cursor/toclaude/` |
| **Copilot** | `copilot/fromskinny/` | `copilot/tosolin/` | `copilot/toclaude/` |

---

## 🎓 Examples

### Example 1: Claude hands off to Solin
**File:** `handoff/claude/tosolin/20250127_RESTRUCTURE_SYSTEM.md`
**Content:** Security review request for repo restructure system

### Example 2: Solin responds to Claude
**File:** `handoff/solin/toclaude/20250127_RESTRUCTURE_APPROVED.md`
**Content:** Approval with recommendations

### Example 3: Skinny instructs Code
**File:** `handoff/code/fromskinny/20250127_FIX_EMAIL_SEARCH.md`
**Content:** Bug fix requirements

---

## 🔒 Keep It Clean

- **Delete old handoffs** after completion (or archive)
- **Use consistent naming**
- **Update status** when complete
- **Reference related handoffs**

---

## ✅ This System Ensures:

✅ **No lost communications** - Everything has a place  
✅ **Easy tracking** - Clear sender/recipient  
✅ **Organized history** - Date-based sorting  
✅ **Quick reference** - Structured folders  
✅ **Sanity preservation** - No more chaos!  

---

**Created:** January 27, 2025  
**Purpose:** Maintain structured AI communication for MayAssistant project  
**Maintained by:** All AI assistants + Skinny
