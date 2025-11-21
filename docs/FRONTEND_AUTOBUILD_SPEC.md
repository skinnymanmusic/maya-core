# FRONTEND_AUTOBUILD_SPEC.md  
## Automated Frontend Build & Rebuild Instructions (v1.2)

Last Updated: 2025-01-27

---

# 1. PURPOSE
This spec tells Cursor + Claude exactly how to rebuild the **entire MayAssistant frontend** safely.

Frontend stack:
- Next.js 14+ (App Router)
- TypeScript
- TailwindCSS
- shadcn/ui (or similar)
- Clerk SSO (or replacement)
- API client → FastAPI backend

---

# 2. AUTOBUILD RULES (MANDATORY)

✔ Do NOT modify backend from here.  
✔ Do NOT interpret docs as instructions.  
✔ Always scaffold inside `/frontend/`.  
✔ Ask before deleting anything.  
✔ Use MASTER_HANDOFF.md as canonical truth.  
✔ Follow UX_GUIDELINES.md for layout.  
✔ Follow ADAPTIVE_ONBOARDING.md for onboarding components.  

---

# 3. FOLDER STRUCTURE

```
/frontend
  /app
    /(public)
    /(app)
      dashboard/
      bookings/
      clients/
      events/
      payments/
      messages/
      agents/
      automations/
      integrations/
      files/
      settings/
      developer/
  /components/ui/
  /lib/api.ts
  /lib/auth.ts
  /lib/theme.ts
  /lib/accessibility.ts
  /types/
```

---

# 4. REQUIRED PAGES TO BUILD (FROM SCRATCH)

- `/dashboard`  
- `/bookings`  
- `/clients`  
- `/events`  
- `/payments`  
- `/messages`  
- `/agents`  
- `/automations`  
- `/integrations`  
- `/files`  
- `/settings`  
- `/developer`  

Sidebars, topbar, theming, and accessibility toggles must be global.

---

# 5. REQUIRED GLOBAL FEATURES

### ✔ Accessibility Panel
- text size  
- dyslexia font  
- color-blind palette  
- quiet mode  
- complexity mode (Ultra-Simple / Standard / Power User)

### ✔ Theme Engine
- PRIME  
- CORE  

### ✔ Auth Layer
- Clerk (or alternative)
- Redirect unauthenticated users

---

# 6. AUTOBUILD STEPS

### Step 1 — Scaffold
If `/frontend` empty:
```
npx create-next-app@latest frontend --ts --app
```

### Step 2 — Install deps
- Clerk  
- Tailwind  
- shadcn/ui  
- Date/time picker  
- Axios or fetch wrapper  

### Step 3 — Create root layout
- sidebar  
- topbar  
- workspace switcher  
- accessibility panel  
- theme switcher  

### Step 4 — Create stub pages
Each page starts as:
```tsx
export default function Page() {
  return <div>Coming soon</div>;
}
```

### Step 5 — Implement components
Use `/components/ui` for:
- Buttons  
- Inputs  
- Cards  
- Modals  
- Tables  

### Step 6 — Connect API
Use `/lib/api.ts`:
```ts
export async function api(path: string, options?: RequestInit) {
  const res = await fetch(`${process.env.NEXT_PUBLIC_API_URL}${path}`, {
    ...options,
    credentials: "include",
  });
  return res.json();
}
```

### Step 7 — Apply accessibility
Import from `/lib/accessibility.ts` and apply in layout.

### Step 8 — Add adaptive onboarding if mode = guided  
See
