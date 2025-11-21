# 🎨 UX GUIDELINES

**MAYA/OMEGA Design System**  
**Version:** 1.0  
**Last Updated:** 2025-01-27

---

## 📋 Overview

This document defines the user experience guidelines, design system, and UI/UX standards for the MAYA/OMEGA frontend application.

---

## 🎯 Design Principles

### 1. Mobile First
- Design for mobile devices first, then scale up
- Minimum touch target: **48px × 48px**
- Ensure all interactions work on touch screens
- Test on real devices, not just emulators

### 2. Accessibility
- WCAG 2.1 AA compliance minimum
- Keyboard navigation for all features
- Screen reader support
- High contrast mode support
- Focus indicators visible

### 3. Performance
- First Contentful Paint < 1.5s
- Time to Interactive < 3.5s
- Optimize images and assets
- Lazy load non-critical content
- Use skeleton loaders, not spinners

### 4. Clarity
- Clear, concise language
- Consistent terminology
- Visual hierarchy
- Error messages are helpful
- Success states are clear

---

## 🎨 Design System

### Color Palette

**Primary Colors:**
```css
--primary-black: #000000;      /* Main background, text */
--primary-yellow: #FCD34D;     /* Accent, highlights */
--primary-gray-800: #1F2937;   /* Sidebar, cards */
--primary-gray-400: #9CA3AF;   /* Secondary text */
```

**Status Colors:**
```css
--success: #10B981;    /* Green - success states */
--warning: #F59E0B;    /* Amber - warnings */
--error: #EF4444;      /* Red - errors */
--info: #3B82F6;       /* Blue - information */
```

**Usage:**
- **Black:** Primary background, main text
- **Yellow:** Active states, highlights, CTAs
- **Gray-800:** Sidebar, card backgrounds
- **Gray-400:** Secondary text, disabled states

### Typography

**Font Family:**
- Primary: `Inter` (sans-serif)
- Fallback: `system-ui, -apple-system, sans-serif`

**Font Sizes:**
```css
--text-xs: 0.75rem;    /* 12px - Captions */
--text-sm: 0.875rem;   /* 14px - Body small */
--text-base: 1rem;     /* 16px - Body */
--text-lg: 1.125rem;   /* 18px - Body large */
--text-xl: 1.25rem;    /* 20px - Headings */
--text-2xl: 1.5rem;    /* 24px - Section titles */
--text-3xl: 2rem;      /* 32px - Page titles */
```

**Font Weights:**
- `400` - Regular (body text)
- `500` - Medium (emphasis)
- `600` - Semibold (headings)
- `700` - Bold (strong emphasis)

### Spacing

**Grid System:**
- Base unit: **4px**
- Use multiples of 4px for all spacing

**Spacing Scale:**
```css
--space-1: 0.25rem;   /* 4px */
--space-2: 0.5rem;    /* 8px */
--space-3: 0.75rem;   /* 12px */
--space-4: 1rem;      /* 16px */
--space-6: 1.5rem;    /* 24px */
--space-8: 2rem;      /* 32px */
--space-12: 3rem;     /* 48px */
```

### Components

#### Buttons

**Primary Button:**
```tsx
<button className="bg-yellow-400 text-black font-semibold px-6 py-3 rounded-lg hover:bg-yellow-500 transition-colors min-h-[48px] min-w-[48px]">
  Primary Action
</button>
```

**Secondary Button:**
```tsx
<button className="bg-gray-800 text-white font-medium px-6 py-3 rounded-lg hover:bg-gray-700 transition-colors min-h-[48px] min-w-[48px]">
  Secondary Action
</button>
```

**Button States:**
- Default: Full opacity
- Hover: Slightly darker/lighter
- Active: Pressed state
- Disabled: 50% opacity, no interaction

#### Cards

```tsx
<div className="bg-gray-800 rounded-lg p-6 border border-gray-700">
  {/* Card content */}
</div>
```

#### Input Fields

```tsx
<input
  type="text"
  className="w-full bg-gray-800 text-white border border-gray-700 rounded-lg px-4 py-3 focus:outline-none focus:ring-2 focus:ring-yellow-400 min-h-[48px]"
  placeholder="Enter text..."
/>
```

**Input States:**
- Default: Gray border
- Focus: Yellow ring (2px)
- Error: Red border
- Disabled: 50% opacity

---

## 📱 Mobile Guidelines

### Touch Targets
- **Minimum:** 48px × 48px
- **Recommended:** 56px × 56px for primary actions
- **Spacing:** 8px minimum between touch targets

### Navigation
- Bottom navigation for mobile
- Hamburger menu for desktop
- Breadcrumbs for deep navigation
- Back button always available

### Forms
- Full-width inputs on mobile
- Large, easy-to-tap buttons
- Inline validation
- Clear error messages
- Auto-focus first field

### Lists
- Minimum row height: 56px
- Clear visual separation
- Swipe actions (optional)
- Pull-to-refresh
- Infinite scroll for long lists

---

## ♿ Accessibility Guidelines

### Keyboard Navigation
- All interactive elements keyboard accessible
- Tab order is logical
- Focus indicators visible (yellow ring)
- Skip links for main content

### Screen Readers
- Semantic HTML elements
- ARIA labels where needed
- Alt text for images
- Descriptive link text
- Form labels associated with inputs

### Color Contrast
- Text: Minimum 4.5:1 contrast ratio
- Large text: Minimum 3:1 contrast ratio
- Don't rely on color alone for information

### Focus Management
- Focus trap in modals
- Return focus after modal closes
- Focus visible on all interactive elements
- No focus traps in normal flow

---

## 🎭 Component Patterns

### Loading States

**Skeleton Loader:**
```tsx
<div className="animate-pulse">
  <div className="h-4 bg-gray-700 rounded w-3/4 mb-2"></div>
  <div className="h-4 bg-gray-700 rounded w-1/2"></div>
</div>
```

**Spinner:**
```tsx
<div className="flex items-center justify-center">
  <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-yellow-400"></div>
</div>
```

### Error States

**Error Message:**
```tsx
<div className="bg-red-900/20 border border-red-500 rounded-lg p-4 text-red-400">
  <p className="font-semibold">Error</p>
  <p className="text-sm mt-1">{errorMessage}</p>
  <button className="mt-4 text-red-400 underline">Retry</button>
</div>
```

### Empty States

```tsx
<div className="text-center py-12">
  <p className="text-gray-400 text-lg">No items found</p>
  <button className="mt-4 text-yellow-400 underline">Add Item</button>
</div>
```

### Success States

```tsx
<div className="bg-green-900/20 border border-green-500 rounded-lg p-4 text-green-400">
  <p>✓ Success! {message}</p>
</div>
```

---

## 📊 Data Display

### Tables
- Responsive (scroll on mobile)
- Sortable columns
- Clear headers
- Alternating row colors
- Action buttons in rows

### Cards
- Consistent padding (24px)
- Clear hierarchy
- Action buttons at bottom
- Hover states for interactivity

### Lists
- Clear visual separation
- Consistent spacing
- Action buttons accessible
- Loading states
- Empty states

---

## 🔔 Notifications

### Toast Notifications
- Position: Top-right (desktop), Bottom (mobile)
- Auto-dismiss: 5 seconds
- Manual dismiss: X button
- Types: Success, Error, Warning, Info

### Inline Notifications
- Contextual to content
- Clear and actionable
- Dismissible
- Persistent for critical info

---

## 🎯 User Flows

### Booking Flow
1. User receives email/SMS
2. Clicks payment link
3. Completes payment
4. Receives confirmation
5. Booking appears in dashboard

### Error Recovery
1. Error message displayed
2. Retry button available
3. Clear error description
4. Support contact if needed

### Onboarding
1. Welcome screen
2. Feature highlights
3. Quick setup
4. First action guidance

---

## 📱 Responsive Breakpoints

```css
/* Mobile First */
sm: 640px   /* Small tablets */
md: 768px   /* Tablets */
lg: 1024px  /* Laptops */
xl: 1280px  /* Desktops */
2xl: 1536px /* Large desktops */
```

**Usage:**
- Mobile: Default styles
- Tablet: `md:` prefix
- Desktop: `lg:` prefix

---

## 🎨 Animation Guidelines

### Transitions
- Duration: 200-300ms
- Easing: `ease-in-out`
- Use for: Hover, focus, state changes

### Loading
- Skeleton loaders preferred
- Spinners for quick actions
- Progress bars for long operations

### Micro-interactions
- Button press feedback
- Form validation feedback
- Success confirmations
- Error shake (optional)

---

## ✅ Checklist

Before shipping UI changes:

- [ ] Mobile responsive
- [ ] Touch targets ≥ 48px
- [ ] Keyboard accessible
- [ ] Screen reader tested
- [ ] Color contrast verified
- [ ] Loading states implemented
- [ ] Error states implemented
- [ ] Empty states implemented
- [ ] Performance optimized
- [ ] Cross-browser tested

---

**Version:** 1.0  
**Status:** Active  
**Maintained By:** Frontend Team

