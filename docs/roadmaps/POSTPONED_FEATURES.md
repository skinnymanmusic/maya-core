# POSTPONED FEATURES — MAYASSISTANT (v1.2)

This document records the features intentionally postponed from the v1.2 launch.  
These features are NOT cancelled. They are deferred for stability, safety, and product clarity.

All postponed items will return in future versions (see REINTRODUCTION_PLAN.md).

---

# 🚫 POSTPONED FEATURES (NOT REMOVED)

## 1. Zero-Click Workflows Engine
**Reason for Postponement:**  
Requires unified scheduler, safety audits, conflict resolution, and concurrency guarantees.

**Risks if added prematurely:**  
Could duplicate bookings, send incorrect reminders, or trigger unintended user actions.

**Will return in:** v2.3

---

## 2. Unified Scheduler Service
**Reason:**  
Full task orchestration requires monitoring, logging, rollback logic, and distributed locks.

**Risk:**  
Race conditions in SMS reminders or payment chasing.

**Will return:** v3.0

---

## 3. Auto-Approval Rules Engine
**Reason:**  
Needs compliance + business logic validation.

**Risk:**  
Approving the wrong event or client could cause financial or legal issues.

**Will return:** v2.4

---

## 4. Hands-Off Operational Mode
**Reason:**  
Depends on zero-click + auto-approval + robust exception detection.

**Will return:** v2.5

---

## 5. Proactive Messaging Service (Maya-reaches-out)
**Reason:**  
Risk of spam, over-messaging, or incorrect timing.

**Will return:** v3.0

---

## 6. Multi-Level Adaptive Onboarding (Tier 2/3)
**Reason:**  
Tier 1 onboarding is enough for MVP. Tier 2/3 require analytics and user studies.

**Will return:** v2.1

---

## 7. Automation Editor (UI for designing automations)
**Reason:**  
Requires schema, runtime engine, and a full visual builder.

**Will return:** v2.2

---

## 8. Contract Builder 2.0
**Reason:**  
Not necessary for MVP; high complexity.

**Will return:** v2.5 or later

---

# 💾 ARCHIVAL NOTE
This file ensures no feature is lost due to reprioritization.  
Whenever a new version begins, product leads must consult:

- POSTPONED_FEATURES.md  
- REINTRODUCTION_PLAN.md  
- ROADMAP_OVERVIEW.md  

to determine feature readiness.

