# ADAPTIVE_ONBOARDING.md  
## Adaptive, Fluid, Optional Onboarding System (v1.2)

Last Updated: 2025-01-27

---

# 1. PURPOSE
MayAssistant onboarding must feel:
- optional  
- fluid  
- magical  
- non-intrusive  
- tailored  
- stress-reducing  

The system adapts itself to:
- user preference  
- user experience level  
- vertical (Beauty vs Events)  
- cognitive load  

---

# 2. THREE MODES OF ONBOARDING

Users select their mode immediately (and can switch any time).

---

## 🟧 Mode 1 — ZERO TRAINING  
For users who want **no tutorial**.

Behavior:
- Immediately drop into Dashboard  
- No walkthrough  
- No nags  
- No forced steps  
- Settings accessible at any time  

Use cases:
- Barbers  
- Nail techs  
- DJs familiar with booking tools  
- Pros who are “tired of platforms wasting their time”

---

## 🟨 Mode 2 — BITE-SIZED TIPS  
For users who want subtle help but no guided flow.

Behavior:
- One-sentence tooltips  
- Only appear when hovering or tapping  
- “Show more” expands into deeper info  
- “Never show again” permanently hides  
- No mandatory steps  
- Hints appear only 1 time per component  

---

## 🟩 Mode 3 — FULL GUIDED TRAINING  
For users who want hands-on, interactive training.

This is where MayAssistant shows **real magic**:
- “Say a command out loud” → Maya texts their phone  
- Simulated bookings  
- Simulated no-shows  
- Simulated payments  
- Mini 5–10s animations to demonstrate flows  
- Real actions (create booking, send test SMS, etc.)

Training is broken into **levels**:

### LEVEL 1 — BASIC (5 minutes)
- Add a booking  
- Confirm a booking  
- Change business hours  
- Send a test reminder  

### LEVEL 2 — INTERMEDIATE (10–15 minutes)
- Setup services  
- Setup pricing  
- Sync Google Calendar  
- Setup Stripe payment links  

### LEVEL 3 — ADVANCED (20–25 minutes)
- Automations  
- Multi-location  
- Advanced settings  
- Developer tab (Power Users)

Users can exit ANYTIME.  
Progress saves automatically.

---

# 3. ARCHITECTURE OF THE ONBOARDING ENGINE

### Components:
- Welcome Flow  
- Feature Tours  
- Contextual Hints  
- Progress Tracker  
- Adaptive Logic Layer  
- Role-Based Configurations (stylist, DJ, etc.)

### Data Model (frontend):
```ts
interface OnboardingState {
  mode: "none" | "tips" | "guided";
  completedSteps: string[];
  skippedSteps: string[];
  lastShownHint: string | null;
  level: 1 | 2 | 3;
}
```

Stored in:
- localStorage (persisted)  
- synced to backend optionally  

---

# 4. INTERACTION MODEL

Each onboarding event is:
1. Detect user intent  
2. Offer tip or next step **only if allowed by mode**  
3. Provide undo  
4. Log in progress tracker  

---

# 5. CONTENT GUIDELINES
- Friendly  
- Short sentences  
- No jargon  
- At most 20 words per instruction  
- No shame (“You forgot…”)  
- Use positive framing (“Here’s how to…”)  
- Support dyslexia-friendly mode  

---

# 6. SUCCESS METRICS
- Time-to-first-booking  
- Time-to-first-payment  
- Feature adoption  
- Reduction in support messages  
- User satisfaction (NPS after onboarding)

---

# 7. MOBILE FIRST
Onboarding must feel natural on:
- iPhone  
- Android  
- Tablets  

Larger tap targets, minimal typing.

---

# 8. FUTURE EXPANSIONS
- Role-based training (DJ vs Nail Tech vs Barber)  
- Voice-first onboarding  
- Vertical-specific examples  
- Choose-your-own-adventure tutorials  

---

END OF ADAPTIVE_ONBOARDING.md
