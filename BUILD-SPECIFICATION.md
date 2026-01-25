# Kraft & Kitchen Complete Build Specification

## Executive Summary

**Primary Goal:** Make the craft buyer feel like they landed on a purpose-built craft supply store (not a mixed industrial catalog) within 3 seconds, then guide them to the correct product size in 2 clicks.

**Operating Principle:** Lead with the project, then reveal the material.

**Current State:** Navigation leads with materials (PTFE/FEP, nonstick paper) and jars, with "Crafts/Kitchen" as secondary.

**Target State:** Craft path becomes primary; materials become filters, specs, and education.

---

## Table of Contents

1. [Brand System](#1-brand-system)
2. [Site Architecture](#2-site-architecture)
3. [Navigation System](#3-navigation-system)
4. [Homepage Design](#4-homepage-design)
5. [Collection Pages](#5-collection-pages)
6. [Product Pages (PDP)](#6-product-pages)
7. [Size Finder](#7-size-finder)
8. [Custom Printing](#8-custom-printing)
9. [Photography System](#9-photography-system)
10. [Copy System](#10-copy-system)
11. [Merchandising](#11-merchandising)
12. [Trust & Conversion](#12-trust-and-conversion)
13. [Build Plan](#13-build-plan)

---

## 1. Brand System

### Brand Identity

**Brand anchor:** "Kraft" = tactile, grounded, workshop | "Kitchen" = practical, functional, clean

**Target feel:** Maker-grade utility + clean product proof + tactile warmth

### Visual Design Tokens

#### Color Palette

| Token | Use |
|-------|-----|
| Background | Warm off-white (not pure white) |
| Surface | White |
| Text Primary | Charcoal (not pure black) |
| Text Secondary | Warm gray |
| Kraft Accent | Light kraft tan, deeper kraft brown |
| Action Accent | Single hue only (deep teal, muted coral, or indigo) |

**Rules:**
- Maximum 1 accent color
- Kraft tones for backgrounds/separators/packaging props only—not UI controls
- Buttons: 1 primary, 1 secondary, 1 tertiary only

#### Typography

| Element | Font Options | Scale Desktop | Scale Mobile |
|---------|--------------|---------------|--------------|
| Headings | Fraunces or Libre Baskerville | — | — |
| Body | Inter, DM Sans, or Manrope | — | — |
| H1 | — | 44/52 | 34/42 |
| H2 | — | 32/40 | 28/34 |
| H3 | — | 24/30 | 24/30 |
| Body | — | 16/24 | 16/24 |
| Small | — | 14/20 | 14/20 |
| Micro | — | 12/16 | 12/16 |

#### Spacing & Components

- Base unit: 8px
- Section padding: 72px desktop, 48px mobile
- Card radius: 12px
- Button height: 48px minimum

#### Image Specifications

| Type | Aspect Ratio |
|------|--------------|
| Product tiles | 4:5 |
| Collection hero | 21:9 |
| Homepage hero | 16:9 |
| Icons | Square SVG |

**Photography style:**
- Lighting: soft daylight, clean shadows, high clarity
- Background: off-white, light gray, or kraft texture (subtle)
- Props: only functional tools, no clutter

---

## 2. Site Architecture

### Three Storefront Lanes

1. **Craft** (primary)
2. **Kitchen** (secondary)
3. **Packaging** (separate lane)

**Rule:** Craft collections contain only craft-relevant products. Packaging stays in its own lane.

### URL Structure

#### Core Pages
```
/                           → Craft-first homepage
/pages/craft
/pages/heat-press
/pages/stickers-transfers
/pages/diamond-painting
/pages/work-surfaces
/pages/bulk-wholesale
/pages/custom-printing
/pages/learn              → Hub
/pages/about
/pages/contact
/pages/shipping-returns   → Single consolidated page
```

#### Craft Collections
```
/collections/release-paper
/collections/release-paper-stickers
/collections/release-paper-diamond-painting
/collections/release-paper-transfers
/collections/ptfe-sheets
/collections/ptfe-rolls-bulk
/collections/silicone-mats
/collections/bundles
```

#### Packaging Collections (Separate Lane)
```
/collections/packaging
/collections/glass-jars
/collections/child-resistant
/collections/easy-open
```

---

## 3. Navigation System

### Header Structure

**Announcement Bar (rotating, 5s interval):**
1. "Fast shipping from Washington"
2. "Bulk discounts for studios and small businesses"
3. "Need help picking a size? Use the Size Finder"
4. "New: Release paper for sticker books and diamond painting"

**Header Row:**
- Left: Logo
- Center: Primary nav
- Right: Search icon + Account + Cart
- Secondary: "Call/Help" link

### Primary Nav Labels (Desktop)

```
Craft | Heat Press | Stickers + Transfers | Diamond Painting | Work Surfaces | Bulk + Wholesale | Custom Printing | Learn
```

### Mega Menu Specifications

#### Craft Mega Menu

| Column 1: Shop by Project | Column 2: Shop by Product | Column 3: Quick Links | Column 4: Proof |
|---------------------------|---------------------------|----------------------|-----------------|
| Sticker storage + sticker books | Release paper sheets | Best sellers | Image tile |
| Transfers + UV DTF | Release paper squares | New arrivals | "Why makers switch" |
| Heat press + sublimation | PTFE cover sheets | Size Finder | 3 bullet proofs |
| Diamond painting sectioning | PTFE rolls (bulk) | Starter packs | |
| Resin + glue projects | Silicone mats and pads | Bulk pricing | |
| Craft clean-up + work surfaces | Bundles | | |

#### Heat Press Mega Menu
- PTFE cover sheets (sizes)
- Platen protection
- Pressing accessories
- "Which size do I need?" link

#### Stickers + Transfers Mega Menu
- Release paper for sticker books (letter size)
- Release paper for transfers (letter/legal)
- "Laser printer safe" products
- Storage formats

#### Diamond Painting Mega Menu
- 4x4 release paper squares
- Decorative squares (future)
- "How to section a canvas" guide

#### Work Surfaces Mega Menu
- Silicone mats (table size)
- Silicone pads (small)
- Trivets

#### Bulk + Wholesale Mega Menu
- Bulk PTFE rolls
- Case packs release paper
- Master cases
- "Request bulk pricing" form

#### Custom Printing Mega Menu
- "Request a quote"
- "MOQ + lead times"
- "Examples gallery"
- "Upload artwork"

### Mobile Navigation

**Top quick buttons (horizontal):**
Shop | Size Finder | Best Sellers | Bulk

**Menu sections:**
Craft → Heat Press → Stickers + Transfers → Diamond Painting → Work Surfaces → Bulk + Wholesale → Learn → Contact

---

## 4. Homepage Design

### Section 1: Hero (16:9)

**Headline options:**
- "Nonstick essentials for makers."
- "Cleaner transfers. Cleaner worktables."
- "Release paper and PTFE that actually releases."

**Subhead:** "Release paper for stickers and diamond painting, plus PTFE cover sheets for heat press."

**CTAs:**
- Primary: Shop Release Paper
- Secondary: Shop PTFE Sheets
- Tertiary: Size Finder (text link)

### Section 2: Shop by Project (6 tiles, 1:1)

1. Stickers + Sticker Books
2. Transfers + UV DTF
3. Heat Press + Sublimation
4. Diamond Painting
5. Resin + Glue
6. Work Surfaces

### Section 3: Best Sellers (8 products)

Requirements:
- Star rating and review count
- Size as first attribute
- Quick add with variant support

### Section 4: "Pick Your Size" Module

Interactive tabs:
- Sticker book pages → recommended products
- Diamond painting → recommended products
- Heat press → recommended products
- Transfers → recommended products

### Section 5: Proof Strip (5 icons)

1. Clean release (less waste)
2. Reusable options
3. Craft-friendly sizes
4. Bulk pricing
5. Real support (phone/chat)

### Section 6: "How It Works" (3 steps)

*Release paper example:*
1. Place sticker/transfer on release paper
2. Peel and re-place without damage
3. Store flat or in binder

*Diamond painting example:*
1. Remove original plastic sheet
2. Place 4x4 squares in sections
3. Work one section, re-cover

### Section 7: UGC Gallery (12 tiles)

Real project photos:
- Sticker storage pages
- Diamond painting sectioning
- PTFE cover sheet usage
- Resin on silicone mats

### Section 8: Learn Cards (3)

- "Release paper vs parchment for stickers"
- "Heat press cover sheets: when to use them"
- "Diamond painting sectioning in 5 minutes"

---

## 5. Collection Pages

### Collection Hero (21:9)

Components:
- Title
- 1-sentence job statement
- 3 quick filter pills (size, pack size, best for)
- "Size Finder" link

### Filters

#### Release Paper Filters
- Size: 8.5x11, 8.5x14, 4x4, 4.5x4.5
- Coating: single-sided, double-sided
- Pack size: Starter (<100), Refill (100-500), Studio (500+), Cases
- Best for: stickers, diamond painting, heat press, transfers
- Printer safe: laser

#### PTFE Filters
- Format: cover sheet, roll
- Size: 8x12, 16x20, 18x20, etc
- Thickness (mil/mm)
- Best for: heat press, craft table, glue/resin
- Temperature rating

### Default Sort Order

| Collection | Default Sort |
|------------|--------------|
| Release paper for stickers | Best sellers |
| Diamond painting squares | Best sellers |
| PTFE cover sheets | Size popularity (16x20, 18x20 first) |
| PTFE rolls bulk | Price per square foot |

### Product Card (PLP)

Components in order:
1. Image (4:5)
2. Badge (Best seller, New, Bulk)
3. Title (short, craft-first)
4. 2 attributes (size, pack count)
5. Price
6. Rating
7. Quick add (variant-aware)

---

## 6. Product Pages (PDP)

### Universal PDP Layout

#### Above the Fold

**Left:** Media gallery
**Right:** Buy box

**Buy box order:**
1. Product title (craft language first)
2. Star rating + review count
3. 3 bullet proofs (with icons)
4. Variant selection (buttons)
5. Quantity selector
6. Add to cart button
7. Shipping note (1 line)
8. "Need help choosing?" link → Size Finder

#### Below the Fold Modules

1. "Best for" (4 icons)
2. "What you get" (pack count, dimensions, contents)
3. "How to use" (3 steps)
4. Specs table
5. Comparison block (optional)
6. FAQs
7. Reviews + customer photos
8. Related items (relevant only)

### PDP Template A: PTFE Cover Sheets

**Title format:** `PTFE Heat Press Cover Sheet {Size}`
- Example: "PTFE Heat Press Cover Sheet 16" x 20""

**Variant structure:**
- Variant 1: Size (pill buttons)
- Variant 2: Pack (1, 2-pack, 5-pack)
- Optional: Thickness

**Icon bullets:**
- Protects platen from residue
- Reusable, wipes clean
- Smooth finish support (test first)

**How-to (3 steps):**
1. Place design on garment
2. Cover with PTFE sheet
3. Press with your normal settings (test for timing)

**Comparison block:**
PTFE cover sheet vs parchment vs kraft paper (finish, reuse, durability)

**Cross-sells:**
- Heat press magnets
- Release paper (disposable barrier)

### PDP Template B: Silicone Release Paper Sheets

**Title format:** `Silicone Release Paper Sheets {Size}`
- Example: "Silicone Release Paper Sheets 8.5" x 11" (Sticker Book Pages)"

**Variant structure:**
- Variant 1: Size (8.5x11, 8.5x14)
- Variant 2: Pack size (25, 50, 100, 250)
- Bulk options visually separated

**Above-fold "Start here" selector:**
- "Sticker book pages" → 8.5x11, 50-pack
- "Transfers" → 8.5x11 or 8.5x14
- "Small business" → 250-pack or case

**FAQs:**
- Can I run this through a printer?
- Is it double-sided?
- Will it damage sticker adhesive?
- Can I cut it down?

**Related items:**
- Release paper squares
- Silicone mat

**REMOVE:** $7,500 custom products from related items

### PDP Template C: Diamond Painting Squares

**Title format:** `Diamond Painting Release Paper Squares 4" x 4" (Double-Sided)`

**Variant structure:**
- Pack size: 100, 200
- Optional: seasonal/printed (future)

**How-to (3 steps):**
1. Remove plastic cover
2. Place squares in sections
3. Work section by section, re-cover when you stop

**Proof module:**
- Rating display
- Customer photos grid

### PDP Template D: PTFE Rolls (Bulk)

**Title:** `PTFE Roll (Bulk) Cut-to-Size`

**Top callout:** "Want a finished-size heat press cover sheet? Shop cover sheets here."

**Variant structure:**
- Width (buttons)
- Length (buttons)
- Thickness (buttons)

NOT a single long dropdown.

**Yield calculator block:**
"How many 16x20 sheets can I cut from this roll?"

---

## 7. Size Finder

### Placement

- Header nav item
- Homepage Section 4
- PDP "Need help choosing?" link
- Collection hero

### Logic

**Inputs:**
- Project type: Stickers / Transfers / Heat Press / Diamond Painting
- Machine size (if heat press): 9x9, 12x10, 15x15, 16x20
- Preference: reusable vs disposable
- Typical volume: personal, side hustle, studio

**Outputs:**
- Recommended SKU(s) and pack sizes
- "Why" sentence
- Add to cart button

### Required Metafields

```
kk.best_for          (list)
kk.size              (string)
kk.format            (sheet, square, roll)
kk.coating_sides     (single, double)
kk.heat_press_compatible  (true/false)
kk.printer_compatible     (laser/inkjet/tested/unknown)
kk.pack_count        (number)
kk.bulk_tier         (starter/refill/studio/case)
```

---

## 8. Custom Printing

### Dedicated Page: `/pages/custom-printing`

**Sections:**
1. Hero: "Custom printed release paper, made for brands and studios"
2. What you can print (sheets, squares, wraps)
3. MOQ and lead time
4. Proofing process
5. Upload artwork + quote form
6. Gallery
7. FAQs

**Rule:** Custom products hidden from standard browsing; accessible only via quote links.

---

## 9. Photography System

### Global Rules

Every product requires:
1. White background pack shot
2. Macro texture shot
3. Scale shot (in-hand or with ruler)
4. In-use shot
5. 3-step how-to images
6. 6-10 second loop video

### File Specifications

- Minimum: 2000px shortest side
- Color profile: sRGB
- Format: JPG for photos, PNG for graphics
- Naming: `kk_{category}_{sku}_{shot-type}_v01.jpg`

### Shot Lists by Product

See `/creative/photography-prompts.md` for detailed prompts.

---

## 10. Copy System

### Voice Rules

- Use plain craft language first, then material in parentheses
- Be specific, avoid hype
- If something varies by setup, say "test first"

### Universal PDP Copy Skeleton

```
TITLE: {Primary craft name} ({Material}) {Size}

ONE-LINE VALUE: A {reusable/disposable} nonstick {sheet/square} that {main job}.

3 BULLETS:
• Best for: {top use cases}
• Size: {dimensions} | Pack: {count}
• Care: {wipe clean / store flat / etc}

HOW TO USE:
1. {step}
2. {step}
3. {step}

SPECS TABLE:
- Size
- Pack count
- Material
- Coating (sides)
- Thickness / basis weight
- Heat notes
- Storage instructions

FAQs (5-8):
Focus on objections
```

See `/copy/templates/` for detailed templates.

---

## 11. Merchandising

### Bundle Products

**Sticker Maker Bundle:**
- Release paper 8.5x11 (50-pack)
- Silicone mat (small)

**Diamond Painting Bundle:**
- 4x4 squares (200)
- Silicone mat (small)

**Heat Press Protection Bundle:**
- PTFE cover sheet 16x20
- Release paper sheets (disposable backup)

### Cross-Sell Rules

**Never include:**
- Sold-out items
- High-priced custom products in retail flow
- Products from different lanes (packaging in craft)

### Bulk Tiering

**Visible tiers:**
- Retail packs: 25, 50, 100
- Studio packs: 250, 500
- Cases: Behind "Bulk + Wholesale" tab

---

## 12. Trust and Conversion

### Reviews and UGC

- Add reviews to all craft products
- Allow photo uploads
- Display summary above fold
- Add "Customer photos" grid

### Urgency (Light Touch)

Use:
- "Popular this week"
- "Backed by maker reviews"
- "Ships fast from WA"

Avoid: Aggressive countdown timers

### Critical Fix

**REMOVE** subscription-style "recurring or deferred purchase" language unless offering subscriptions.

---

## 13. Build Plan

### Phase 1: Structure (1 Sprint)

**Deliverables:**
- New nav + mega menus
- Craft lane pages
- Updated collections (split by project)
- Remove packaging from craft collections
- Size Finder v1

**Acceptance Criteria:**
- Craft shopper reaches correct release paper format in 2 clicks
- No craft collection contains jars/packaging
- No retail PDP shows $7,500 items as related

### Phase 2: PDP System + Proof (1 Sprint)

**Deliverables:**
- PDP templates A-D
- Variants as button selectors
- Specs table via metafields
- Reviews above fold
- Related items logic rewritten

**Acceptance Criteria:**
- PTFE PDP: protection, finish note, reuse, how-to, specs, FAQs
- Release paper PDP: "start here" selector, use-case tabs
- Diamond painting PDP: sectioning how-to, photo proof

### Phase 3: Photography + Content (Ongoing)

**Deliverables:**
- Full shot list for best sellers
- UGC collection system
- Learn hub with 6 core guides

**Acceptance Criteria:**
- Every best seller has 6+ images and 1 video
- Learn pages link to products

### Priority Order

1. Craft-first nav + packaging separation
2. Release paper retail variants + remove subscription warning
3. Add 8.5x11 sticker packs and 4x4 squares
4. PTFE cover sheets as finished sizes
5. Reviews + UGC modules
6. Size Finder

---

## Reference Sources

- [Heat Press Nation](https://www.heatpressnation.com/products/pro-grade-non-stick-sheet) - Size-first variants, heavy reviews
- [STAHLS'](https://www.stahls.com/heat-press-cover-sheet) - Protect platen, semi-gloss finish, reusable
- [Diamond Art Club](https://www.diamondartclub.com/products/double-sides-release-paper) - 2,382 reviews, scarcity cues
- [Etsy Sticker Books](https://www.etsy.com/au/listing/1375701848/sticker-book-release-paper-extra-large) - Double-sided silicone, letter size, small packs
- [Expressions Vinyl](https://expressionsvinyl.com/heat-transfer-cover-sheet-18x20/) - Reusable, replace if creased
- [143 Vinyl](https://www.143vinyl.com/Heat-resistant-sheets-16-x-20.html) - Plain language, practical add-ons
