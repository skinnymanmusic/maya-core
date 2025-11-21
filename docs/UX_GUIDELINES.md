# UX_GUIDELINES.md  
## MayAssistant UX & Accessibility Standards (v1.2)
### The user experience must always feel: optional, empowering, modern, ethical, and stress-reducing.

Last Updated: 2025-01-27

---

# 1. PURPOSE

This document defines how MayAssistant **looks, feels, flows, and behaves**.

It merges:
- The OurBooks accessibility mandate  
- The Gilman Accords  
- The MayAssistant dual-vertical UX strategy  
- Your adaptive complexity philosophy (“UX is up to the user”)  
- Cursor-safe, future-proof UI principles  

Every screen, component, interaction, and training flow MUST align with this file.

---

# 2. USER-CONTROLLED COMPLEXITY (THE 3-LAYER PHILOSOPHY)

MayAssistant is the **first AI booking platform that adapts its UI complexity to each user**.

Users can switch modes ANYTIME from the accessibility panel.

### 🟧 **Layer 1 — Ultra-Simple Mode**
For beauty pros + barbers + stylists who want ZERO clutter.
- Only essential actions visible
- Giant buttons
- Big text default
- No analytics
- No advanced settings
- Booking → Pay → Remind, that’s it

### 🟦 **Layer 2 — Standard Mode** (Default)
For most users.
- Clean dashboard  
- Bookings, clients, payments  
- Minimal charts  
- Friendly onboarding tips  

### 🟩 **Layer 3 — Power User Mode**
For DJs, agencies, tech-savvy pros.
- Advanced automations  
- Developer tab  
- Integrations center  
- Multi-location controls  
- Revenue analytics  
- Timeline logs  
- Vertical-specific controls (Events Pack, etc.)

**The UI adapts to the user — not the other way around.**

---

# 3. ACCESSIBILITY STANDARDS (MANDATORY)

These are inherited from OurBooks’ accessibility philosophy and expanded for MayAssistant.

All modes MUST support:

### ✔ Text Size Scaling  
- Small  
- Medium  
- Large  
- XL (high visibility)

### ✔ Dyslexia-Friendly Font  
- Switchable globally  
- Applies to all components instantly

### ✔ Color-Blind Palettes  
- Protanopia  
- Deuteranopia  
- Tritanopia  
- High-contrast “Accessibility Gold” theme

### ✔ Quiet Mode  
For neurodivergent or overwhelmed users:
- No animations  
- No pop-up tooltips  
- Minimal notifications  
- Slower transitions  

### ✔ Predictable Navigation  
- No changing button positions  
- No surprise modals  
- No hidden menus  
- No moving targets  

### ✔ Keyboard Navigation & Screen Reader Support  
- Every interactive element accessible via TAB  
- ARIA labels mandatory  
- Focus rings visible  

---

# 4. DESIGN PRINCIPLES

### ⭐ **Clarity Over Cleverness**  
Simple language always beats jargon.

### ⭐ **45-Second Rule**  
A new user should:
- understand the dashboard  
- see their next appointment  
- understand how to add a client  
- send a test reminder  

**in 45 seconds or less.**

### ⭐ **Zero Cognitive Overload**  
No walls of text.  
No complex forms.  
No 7-step wizards.  
Chunk EVERYTHING.

### ⭐ **Predictable Flow**  
Every action should follow:
1. Intent  
2. Confirmation  
3. Result  
4. Undo  

### ⭐ **Mobile First**  
Most beauty pros + stylists + barbers run their businesses from phones.

### ⭐ **Everything Optional**  
No forced onboarding.  
No forced setup.  
No forced automation.  
Ever.

---

# 5. DESIGN SYSTEM COMPONENTS

A unified base component library lives in `/components/ui/`.

### Buttons:
- Primary
- Secondary
- Ghost
- Destructive
- Icon-only
- Loading state

### Inputs:
- Text  
- Email  
- Phone  
- Search  
- Date/time  
- Select  
- Autocomplete  
- Textarea  

### Cards:
- Standard Card  
- Highlight Card  
- Success/Warning/Error Cards  

### Data Display:
- Tables  
- Lists  
- Badges  
- Charts (simple, minimal)

### Navigation:
- Sidebar (collapsible)  
- Top bar  
- Workspace switcher  
- User settings menu  

### Notifications:
- Toast (non-blocking)  
- Inline success/error banners  
- Subtle progress bars  

---

# 6. PLATFORM-WIDE LAYOUT STRUCTURE

### 🗂 Dashboard Layout
- Left sidebar (navigation)
- Top bar (profile, theme, accessibility)
- Main content area (cards + tables)

### 🏷 Page Layout
Each page should have:
- Title  
- Short description  
- Main section  
- Secondary sidebar (if power user)  

### 📱 Mobile Layout
- Sticky bottom navigation bar  
- Floating “+” button for quick add  
- Collapsible sections  
- Large touch targets (48px minimum)  

---

# 7. CONTENT TONE & LANGUAGE

MayAssistant’s tone = **clear + friendly + respectful**.

### Do:
- “Let’s confirm this appointment.”
- “Here are your next steps.”
- “You can change this anytime.”

### Do NOT:
- “Are you sure?”
- “You must finish this first.”
- Shame/pressure wording

---

# 8. COMPONENT BEHAVIOR RULES (NON-NEGOTIABLES)

- Buttons must show loading state  
- Inputs must have error + success states  
- Tooltips must be ignorable  
- Forms must auto-save drafts  
- No scroll-jacking  
- No full-screen modals unless absolutely needed  
- No infinite spinners — use skeleton loaders instead  
- Animations must be < 200ms  

---

# 9. SCREEN-BY-SCREEN GUIDELINES

### Dashboard:
- Show today’s appointments  
- Show "Money Owed Today"  
- Alerts module (if enabled)  
- No more than 3 metrics  

### Bookings:
- Table + filters  
- Quick-add button  
- Inline reschedule  
- Status badges  

### Clients:
- Masked PII by default (per Gilman Accords)  
- Search uses hashed fields  
- Quick-add client modal  

### Payments:
- Full Stripe integration  
- Clear deposit status  
- Buttons:
  - “Send Payment Link”
  - “Send Reminder”

### Automations:
- Toggle-based  
- No scripts or code  
- Default suggestions for beginners  

### Messages:
- Timeline view  
- Email + SMS threads unified  

---

# 10. VERTICAL DIFFERENTIATION (APPLIED AT RUNTIME)

### Beauty:
- Pastel/light themes  
- Icons: nail, hair, spa  
- 30–90 min blocks  
- Simple repeating schedules  

### Events (DJ):
- Dark mode default  
- Equipment icons  
- Long-duration blocks (4–8 hours)  
- Event detail fields  

---

# 11. QUALITY STANDARDS (ABSOLUTE)

- FCP < 1.5s  
- LCP < 2.5s  
- Lazy-load images  
- Bundles < 250 KB gzipped  
- All content mobile-optimized  
- No layout shift during load  

---

# 12. UX MANDATE SUMMARY

MayAssistant MUST feel:

- **Beautiful**  
- **Fast**  
- **Flexible**  
- **Optional**  
- **Accessible**  
- **Calming**  
- **Intuitive**  
- **Non-judgmental**  
- **Professional without being cold**  

If a UX choice increases anxiety?  
It is automatically wrong.

**END OF UX_GUIDELINES.md**
