# Design Tokens - Kraft & Kitchen

These tokens can be pasted directly into a style guide or CSS variables file.

---

## Brand Identity

**Brand feel:** Maker-grade utility + clean product proof + tactile warmth

**Design approach:**
- Functional, not decorative
- Proof-driven, not claim-driven
- Warm and approachable, not clinical
- Professional, not cute

---

## Color Palette

### CSS Variables

```css
:root {
  /* Backgrounds */
  --color-bg-primary: #FAF8F5;        /* Warm off-white */
  --color-bg-secondary: #FFFFFF;       /* Pure white */
  --color-bg-kraft: #E8DFD4;          /* Light kraft */
  --color-bg-kraft-dark: #C4B6A4;     /* Kraft accent */

  /* Text */
  --color-text-primary: #2D2D2D;      /* Charcoal (not pure black) */
  --color-text-secondary: #6B6B6B;    /* Warm gray */
  --color-text-muted: #9A9A9A;        /* Light gray */
  --color-text-inverse: #FFFFFF;      /* White on dark */

  /* Accent (choose ONE) */
  /* Option A: Deep Teal */
  --color-accent: #1A7F7F;
  --color-accent-hover: #156666;
  --color-accent-light: #E6F3F3;

  /* Option B: Muted Coral */
  /* --color-accent: #D97565;
  --color-accent-hover: #C4604F;
  --color-accent-light: #FDF2F0; */

  /* Option C: Indigo */
  /* --color-accent: #4F46E5;
  --color-accent-hover: #4338CA;
  --color-accent-light: #EEF2FF; */

  /* UI States */
  --color-border: #E5E5E5;
  --color-border-focus: var(--color-accent);
  --color-success: #059669;
  --color-error: #DC2626;
  --color-warning: #D97706;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.07);
  --shadow-lg: 0 10px 15px rgba(0, 0, 0, 0.1);
}
```

### Color Usage Rules

| Element | Token |
|---------|-------|
| Page background | `--color-bg-primary` |
| Cards, modals | `--color-bg-secondary` |
| Section dividers | `--color-bg-kraft` |
| Primary buttons | `--color-accent` |
| Primary text | `--color-text-primary` |
| Secondary text | `--color-text-secondary` |
| Links | `--color-accent` |
| Borders | `--color-border` |

**Rules:**
- Use accent color ONLY for CTAs, links, badges, and focus states
- Kraft tones appear in backgrounds and props, NOT in UI controls
- Maximum 1 accent color throughout the site

---

## Typography

### Font Stack

```css
:root {
  /* Headings: Editorial serif or friendly geometric */
  --font-heading: 'Fraunces', 'Libre Baskerville', Georgia, serif;

  /* Body: Clean modern sans */
  --font-body: 'Inter', 'DM Sans', 'Manrope', -apple-system, BlinkMacSystemFont, sans-serif;

  /* Mono (code, specs) */
  --font-mono: 'JetBrains Mono', 'Fira Code', monospace;
}
```

### Type Scale

```css
:root {
  /* Desktop */
  --text-h1: 44px;
  --text-h1-line: 52px;

  --text-h2: 32px;
  --text-h2-line: 40px;

  --text-h3: 24px;
  --text-h3-line: 30px;

  --text-body: 16px;
  --text-body-line: 24px;

  --text-small: 14px;
  --text-small-line: 20px;

  --text-micro: 12px;
  --text-micro-line: 16px;

  /* Font weights */
  --weight-normal: 400;
  --weight-medium: 500;
  --weight-semibold: 600;
  --weight-bold: 700;
}

/* Mobile overrides */
@media (max-width: 768px) {
  :root {
    --text-h1: 34px;
    --text-h1-line: 42px;

    --text-h2: 28px;
    --text-h2-line: 34px;
  }
}
```

### Typography Classes

```css
.heading-1 {
  font-family: var(--font-heading);
  font-size: var(--text-h1);
  line-height: var(--text-h1-line);
  font-weight: var(--weight-bold);
  color: var(--color-text-primary);
}

.heading-2 {
  font-family: var(--font-heading);
  font-size: var(--text-h2);
  line-height: var(--text-h2-line);
  font-weight: var(--weight-semibold);
  color: var(--color-text-primary);
}

.heading-3 {
  font-family: var(--font-body);
  font-size: var(--text-h3);
  line-height: var(--text-h3-line);
  font-weight: var(--weight-semibold);
  color: var(--color-text-primary);
}

.body-text {
  font-family: var(--font-body);
  font-size: var(--text-body);
  line-height: var(--text-body-line);
  font-weight: var(--weight-normal);
  color: var(--color-text-primary);
}

.small-text {
  font-family: var(--font-body);
  font-size: var(--text-small);
  line-height: var(--text-small-line);
  color: var(--color-text-secondary);
}
```

---

## Spacing

### Spacing Scale (8px base)

```css
:root {
  --space-1: 4px;
  --space-2: 8px;
  --space-3: 12px;
  --space-4: 16px;
  --space-5: 20px;
  --space-6: 24px;
  --space-8: 32px;
  --space-10: 40px;
  --space-12: 48px;
  --space-16: 64px;
  --space-18: 72px;
  --space-24: 96px;
}
```

### Section Spacing

```css
:root {
  /* Desktop */
  --section-padding-desktop: 72px;
  --section-gap-desktop: 64px;

  /* Mobile */
  --section-padding-mobile: 48px;
  --section-gap-mobile: 40px;
}

.section {
  padding-top: var(--section-padding-desktop);
  padding-bottom: var(--section-padding-desktop);
}

@media (max-width: 768px) {
  .section {
    padding-top: var(--section-padding-mobile);
    padding-bottom: var(--section-padding-mobile);
  }
}
```

---

## Components

### Border Radius

```css
:root {
  --radius-sm: 4px;
  --radius-md: 8px;
  --radius-lg: 12px;
  --radius-xl: 16px;
  --radius-full: 9999px;
}
```

### Buttons

```css
:root {
  --button-height: 48px;
  --button-height-sm: 40px;
  --button-padding-x: 24px;
  --button-radius: var(--radius-md);
}

.btn {
  height: var(--button-height);
  padding: 0 var(--button-padding-x);
  border-radius: var(--button-radius);
  font-family: var(--font-body);
  font-size: var(--text-body);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: all 0.2s ease;
}

.btn-primary {
  background: var(--color-accent);
  color: var(--color-text-inverse);
  border: none;
}

.btn-primary:hover {
  background: var(--color-accent-hover);
}

.btn-secondary {
  background: transparent;
  color: var(--color-accent);
  border: 2px solid var(--color-accent);
}

.btn-secondary:hover {
  background: var(--color-accent-light);
}

.btn-tertiary {
  background: transparent;
  color: var(--color-text-primary);
  border: 2px solid var(--color-border);
}

.btn-tertiary:hover {
  border-color: var(--color-text-secondary);
}
```

### Cards

```css
.card {
  background: var(--color-bg-secondary);
  border-radius: var(--radius-lg);
  border: 1px solid var(--color-border);
  overflow: hidden;
}

.card-elevated {
  box-shadow: var(--shadow-md);
  border: none;
}

.card-interactive {
  cursor: pointer;
  transition: transform 0.2s ease, box-shadow 0.2s ease;
}

.card-interactive:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg);
}
```

### Form Inputs

```css
.input {
  height: var(--button-height);
  padding: 0 var(--space-4);
  border: 2px solid var(--color-border);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: var(--text-body);
  background: var(--color-bg-secondary);
  transition: border-color 0.2s ease;
}

.input:focus {
  outline: none;
  border-color: var(--color-border-focus);
}

.input::placeholder {
  color: var(--color-text-muted);
}
```

---

## Image Specifications

### Aspect Ratios

```css
:root {
  --aspect-product-tile: 4 / 5;     /* Product cards */
  --aspect-collection-hero: 21 / 9; /* Collection headers */
  --aspect-homepage-hero: 16 / 9;   /* Homepage hero */
  --aspect-square: 1 / 1;           /* Icons, thumbnails */
}

.img-product-tile {
  aspect-ratio: var(--aspect-product-tile);
  object-fit: cover;
}

.img-collection-hero {
  aspect-ratio: var(--aspect-collection-hero);
  object-fit: cover;
}

.img-hero {
  aspect-ratio: var(--aspect-homepage-hero);
  object-fit: cover;
}
```

### Photography Style Rules

| Attribute | Specification |
|-----------|---------------|
| Lighting | Soft daylight, clean shadows |
| Background | Off-white, light gray, or kraft texture |
| Props | Functional tools only, no clutter |
| Clarity | High clarity, sharp focus on product |
| Color | True to life, not over-saturated |
| Minimum size | 2000px shortest side |

---

## Grid System

```css
:root {
  --container-max: 1200px;
  --container-padding: 20px;
  --grid-gap: 24px;
}

.container {
  max-width: var(--container-max);
  margin: 0 auto;
  padding-left: var(--container-padding);
  padding-right: var(--container-padding);
}

.grid {
  display: grid;
  gap: var(--grid-gap);
}

.grid-2 { grid-template-columns: repeat(2, 1fr); }
.grid-3 { grid-template-columns: repeat(3, 1fr); }
.grid-4 { grid-template-columns: repeat(4, 1fr); }
.grid-6 { grid-template-columns: repeat(6, 1fr); }

@media (max-width: 768px) {
  .grid-2 { grid-template-columns: 1fr; }
  .grid-3 { grid-template-columns: repeat(2, 1fr); }
  .grid-4 { grid-template-columns: repeat(2, 1fr); }
  .grid-6 { grid-template-columns: repeat(3, 1fr); }
}
```

---

## Breakpoints

```css
:root {
  --breakpoint-sm: 640px;
  --breakpoint-md: 768px;
  --breakpoint-lg: 1024px;
  --breakpoint-xl: 1280px;
}

/* Mobile first approach */
@media (min-width: 640px) { /* sm */ }
@media (min-width: 768px) { /* md */ }
@media (min-width: 1024px) { /* lg */ }
@media (min-width: 1280px) { /* xl */ }
```

---

## Animation

```css
:root {
  --transition-fast: 0.15s ease;
  --transition-normal: 0.2s ease;
  --transition-slow: 0.3s ease;
}

/* Hover states */
.hover-lift {
  transition: transform var(--transition-normal);
}
.hover-lift:hover {
  transform: translateY(-4px);
}

/* Focus states */
.focus-ring:focus {
  outline: none;
  box-shadow: 0 0 0 3px var(--color-accent-light);
}
```

---

## Z-Index Scale

```css
:root {
  --z-dropdown: 100;
  --z-sticky: 200;
  --z-fixed: 300;
  --z-modal-backdrop: 400;
  --z-modal: 500;
  --z-popover: 600;
  --z-tooltip: 700;
}
```

---

## Badges

```css
.badge {
  display: inline-flex;
  align-items: center;
  padding: var(--space-1) var(--space-3);
  border-radius: var(--radius-full);
  font-size: var(--text-micro);
  font-weight: var(--weight-semibold);
}

.badge-accent {
  background: var(--color-accent);
  color: var(--color-text-inverse);
}

.badge-success {
  background: #D1FAE5;
  color: #065F46;
}

.badge-warning {
  background: #FEF3C7;
  color: #92400E;
}

.badge-kraft {
  background: var(--color-bg-kraft);
  color: var(--color-text-primary);
}
```
