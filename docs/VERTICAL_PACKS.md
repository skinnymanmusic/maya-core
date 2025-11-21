# VERTICAL_PACKS.md  
## MayAssistant Vertical Pack Framework (v1.2)

Last Updated: 2025-01-27

---

# 1. PURPOSE
Vertical Packs = how MayAssistant scales horizontally across industries.

Each pack adjusts:
- terminology  
- default services  
- booking durations  
- pricing logic  
- workflows  
- UI accents  
- templates  
without changing core architecture.

---

# 2. PACKS (CURRENT + FUTURE)

### 🔴 BEAUTY PACK — Priority 1
For:
- nail techs  
- lash artists  
- estheticians  
- makeup artists  
- stylists  

Includes:
- fixed durations  
- service catalog  
- SMS-first booking  
- simple schedules  
- no-show minimization  

---

### 🔴 EVENTS PACK — Priority 2 (70–85% complete)
For DJs, AV techs.

Includes:
- venue intelligence  
- event duration logic  
- equipment lists  
- payment deposit system  
- proposal basics  

---

### 🟡 WELLNESS PACK — Future
For:
- massage therapists  
- acupuncturists  
- bodywork specialists  

Defaults:
- longer durations  
- intake notes  

---

### 🟢 FITNESS PACK — Future
For personal trainers.

Defaults:
- repeating schedules  
- membership logic  

---

# 3. PACK STRUCTURE

Each pack has:
- Config file  
- Default services  
- Default durations  
- Default pricing  
- Appearance theme  
- Tips + onboarding variations  

Stored in:
```
/packs/<vertical>/config.json
```

---

# 4. PACK CREATION RULES

1. No pack may duplicate core logic.  
2. Packs must be purely config-driven.  
3. Packs may override:
   - text  
   - durations  
   - service names  
   - icons  
   - layout accents  

4. Packs may NOT override:
   - encryption  
   - database schema  
   - safety  
   - legal compliance  
   - payment core logic  

---

# 5. TEMPLATE FOR PACKS

```
{
  "id": "beauty",
  "name": "Beauty Professionals",
  "defaultServices": [...],
  "durations": {...},
  "colors": {...},
  "reminderStyle": "gentle",
  "bookingFlow": "sms-first",
  "requiresCalendarSync": true
}
```

---

END OF VERTICAL_PACKS.md
