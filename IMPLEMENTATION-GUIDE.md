# Kraft & Kitchen Craft Website Improvement - Implementation Guide

This guide provides a complete roadmap for implementing the craft buyer-focused improvements to your Shopify store.

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Priority Actions](#priority-actions)
3. [New Products to Create](#new-products-to-create)
4. [Product Page Changes](#product-page-changes)
5. [Navigation Changes](#navigation-changes)
6. [New Pages to Create](#new-pages-to-create)
7. [Collection Setup](#collection-setup)
8. [Content Implementation](#content-implementation)
9. [Technical Fixes](#technical-fixes)
10. [Photography Needs](#photography-needs)
11. [Implementation Timeline](#implementation-timeline)
12. [File Reference](#file-reference)

---

## Executive Summary

### The Core Problem
Your site sells quality products but presents them in a bulk/industrial way that doesn't match how craft shoppers think and shop.

### The Solution
Reposition for craft buyers with:
- Task-forward navigation (not material-forward)
- Craft-friendly pack sizes (not bulk-first)
- Educational content that matches search intent
- Clear product pages with specs that matter to crafters

### Expected Outcomes
- Improved conversion from craft traffic
- Better SEO for craft-intent searches
- Reduced bounce from first-time buyers
- Clear differentiation from industrial suppliers

---

## Priority Actions

### Immediate (Do First)

1. **Remove recurring purchase language** from all product pages
   - Unless you're offering subscriptions, this confuses/scares buyers
   - In Shopify Admin: Edit products → Remove selling plans

2. **Create Craft Hub landing page** at `/pages/craft-supplies`
   - Use content from: `pages/craft-hub-landing-page.html`
   - This becomes the "front door" for craft shoppers

3. **Add letter size (8.5x11) release paper option**
   - Your current 8.5x14 is fine, but letter size is what sticker makers expect
   - Add smaller pack sizes (25, 50, 100) as entry points

4. **Add 4x4 diamond painting squares product**
   - Use content from: `products/diamond-painting-release-paper-4x4.html`
   - This matches market expectations (Diamond Art Club, Hobby Lobby format)

### High Priority

5. **Create PTFE Cover Sheets as primary craft product**
   - Pre-cut sheets, not rolls, should be the craft entry point
   - Use content from: `products/ptfe-cover-sheet-heat-press.html`

6. **Update navigation** to task-forward structure
   - See: `config/navigation-collections.md`

7. **Create "Shop by Craft" collections**
   - Heat Press + Sublimation + DTF
   - Stickers + Decals + Transfer
   - Diamond Painting
   - Resin + Glue + Messy Crafts

### Important

8. **Add SEO landing pages** for craft intent keywords
   - See: `pages/seo-content/` folder
   - Start with top 3-4 pages

9. **Update product photography**
   - See: `creative/photography-shot-list.md`
   - Prioritize use-case shots over product-only shots

10. **Add reviews with photo uploads**
    - Craft shoppers rely on social proof
    - Consider Shopify Product Reviews or similar app

---

## New Products to Create

### 1. Double-Sided Silicone Release Paper (Letter Size)
**SKU Pattern:** `RELEASE-LETTER-[count]`
**Sizes:** 8.5" x 11"
**Pack Counts:** 25, 50, 100, 250, 500
**Collections:** Stickers + Decals, Silicone Release Paper
**Content:** `products/release-paper-sticker-letter-size.html`

### 2. Diamond Painting Release Paper Squares
**SKU Pattern:** `RELEASE-DP-4X4-[count]`
**Size:** 4" x 4"
**Pack Counts:** 100, 200, 400
**Collections:** Diamond Painting, Silicone Release Paper
**Content:** `products/diamond-painting-release-paper-4x4.html`

### 3. PTFE Cover Sheets (Pre-Cut)
**SKU Pattern:** `PTFE-SHEET-[size]-[thickness]-[count]`
**Sizes:** 16x20, 18x20, 15x15, 12x15
**Thickness:** 3 mil, 4 mil
**Pack Counts:** 1, 2, 5, 10
**Collections:** PTFE Cover Sheets, Heat Press + Sublimation
**Content:** `products/ptfe-cover-sheet-heat-press.html`

### 4. Starter Bundles (Optional)
Consider creating bundles:
- Heat Press Starter: 2x PTFE sheets + release paper
- Sticker Maker Starter: 100x release paper + tips card
- Diamond Painting Starter: 200x 4x4 squares

---

## Product Page Changes

### All Products

1. **Remove recurring purchase language**
   - Go to Shopify Admin → Products → [Product] → Edit
   - Remove any selling plan associations
   - Or if keeping subscriptions, add clear "Subscribe & Save" UI with cancellation policy

2. **Add spec panels** (use tables from content files)

3. **Add FAQ sections** with schema markup

4. **Add "use case" buttons/selector** above the fold

### PTFE Rolls Page
- Rename to: "Bulk PTFE Rolls (For Shops and High-Volume Use)"
- Add link at top: "Looking for pre-cut sheets? Shop PTFE Cover Sheets →"
- Add cutting guide showing how many sheets per roll:
  - 16"x4' → 2 sheets at 16x20
  - 16"x50' → ~30 sheets at 16x20
  - 16"x300' → ~180 sheets at 16x20
  - 24"x50' → ~30 sheets at 24x20

### Release Paper Page (Existing)
- Add 8.5x11 option
- Add smaller pack sizes (50, 100)
- Clarify: single-sided or double-sided
- Add related link to diamond painting squares
- Content reference: `products/release-paper-bulk-legal-size.html`

---

## Navigation Changes

### Current (Material-Forward)
```
PTFE and FEP Nonstick
Nonstick Paper
```

### Recommended (Task-Forward)
```
Craft Supplies
├── Shop by Craft
│   ├── Heat Press + Sublimation + DTF
│   ├── Stickers + Decals + Transfer
│   ├── Diamond Painting
│   └── Resin + Glue + Messy Crafts
├── Shop by Product
│   ├── PTFE Cover Sheets
│   ├── Silicone Release Paper
│   └── Silicone Work Mats
Kitchen
Bulk & Business
Learn
```

Full navigation structure: `config/navigation-collections.md`

---

## New Pages to Create

### Landing Pages

| Page | URL | Content File |
|------|-----|--------------|
| Craft Hub | /pages/craft-supplies | `pages/craft-hub-landing-page.html` |

### SEO Content Pages

| Page | URL | Content File |
|------|-----|--------------|
| PTFE Heat Press Guide | /pages/ptfe-sheet-for-heat-press | `pages/seo-content/ptfe-sheet-for-heat-press.html` |
| Sticker Storage Guide | /pages/release-paper-for-stickers | `pages/seo-content/release-paper-for-stickers.html` |
| Diamond Painting Guide | /pages/diamond-painting-release-paper | `pages/seo-content/diamond-painting-release-paper.html` |
| Release vs Parchment | /pages/release-paper-vs-parchment | `pages/seo-content/release-paper-vs-parchment.html` |
| Dust Protection Tips | /pages/diamond-painting-dust-protection | `pages/seo-content/diamond-painting-dust-protection.html` |

---

## Collection Setup

### New Collections to Create

1. **heat-press-sublimation**
   - Title: Heat Press + Sublimation + DTF
   - Products: PTFE sheets, PTFE rolls, silicone pads

2. **stickers-decals-transfer**
   - Title: Stickers + Decals + Transfer
   - Products: Release paper letter, release paper legal, bulk paper

3. **diamond-painting**
   - Title: Diamond Painting
   - Products: 4x4 squares, 4.5x4.5 squares, letter release paper

4. **resin-glue-messy-crafts**
   - Title: Resin + Glue + Messy Crafts
   - Products: Silicone mats, release paper

5. **ptfe-cover-sheets**
   - Title: PTFE Cover Sheets
   - Products: All pre-cut PTFE sizes

6. **silicone-release-paper**
   - Title: Silicone Release Paper
   - Products: All release paper sizes/formats

7. **craft-best-sellers**
   - Title: Craft Best Sellers
   - Products: Manually curated top products

8. **bulk-business**
   - Title: Bulk & Business
   - Products: Rolls, large packs, case quantities

Full details: `config/navigation-collections.md`

---

## Content Implementation

### Product Description Copy

For each product, update descriptions to include:

1. **Key benefits list** (bullet points at top)
2. **Use case explanations** (who uses this and why)
3. **Specifications table** (size, coating, weight, etc.)
4. **FAQ section** with schema markup
5. **Related products** links

Content templates are in the `products/` folder.

### Copy Direction (What to Emphasize)

**For PTFE Cover Sheets:**
- Protects upper platen from ink/vinyl residue
- Reusable—replace only if creased or wrinkled
- Rated to 500°F/260°C
- May impart semi-gloss finish (test first)

**For Release Paper:**
- Double-sided silicone coating (for letter size)
- Stickers peel clean, retain adhesive
- Standard letter size fits binders
- Reusable until creased or soiled

**For Diamond Painting Squares:**
- 4x4 is the market standard size
- Protects poured glue adhesive
- Move squares as you work sections
- Double-sided—use either face

---

## Technical Fixes

### 1. Remove Recurring Purchase Authorization
**Location:** Product pages (via selling plans)
**Action:** Remove selling plan from products unless offering subscriptions
**Why:** This language scares normal buyers

### 2. Add FAQ Schema Markup
**Location:** Product pages and SEO pages
**Action:** Implement FAQPage schema on FAQ sections
**Why:** Can trigger rich snippets in search results

### 3. Add Article Schema
**Location:** SEO content pages
**Action:** Implement Article schema
**Why:** Helps search engines understand content type

### 4. Verify Mobile Navigation
**Action:** Test "Shop by Craft" is accessible without scrolling on mobile
**Why:** Mobile is likely majority of craft traffic

---

## Photography Needs

### Priority Shots (Phase 1)

1. PTFE cover sheet on heat press platen (hero)
2. Release paper with sticker being peeled
3. Diamond painting canvas with 4x4 squares covering sections
4. Pack/quantity shots for all products

### Full Shot List

See: `creative/photography-shot-list.md`

Estimated total: 50-75 product images for complete refresh

---

## Implementation Timeline

### Week 1: Foundation
- [ ] Remove recurring purchase language
- [ ] Create letter size release paper variant
- [ ] Create 4x4 diamond painting squares product
- [ ] Create PTFE cover sheets product

### Week 2: Structure
- [ ] Create new collections
- [ ] Update navigation
- [ ] Create Craft Hub landing page
- [ ] Link collections from Craft Hub

### Week 3: Content
- [ ] Update product descriptions (priority products first)
- [ ] Add spec tables and FAQ sections
- [ ] Create first 2-3 SEO pages

### Week 4: Polish
- [ ] Remaining SEO pages
- [ ] Photography updates (as available)
- [ ] Internal linking
- [ ] Test and verify all links work

### Ongoing
- Add reviews and photo uploads
- Monitor search performance
- Adjust based on customer feedback

---

## File Reference

### Product Content
```
products/
├── release-paper-sticker-letter-size.html    # Letter size for stickers
├── diamond-painting-release-paper-4x4.html   # 4x4 squares
├── release-paper-bulk-legal-size.html        # Bulk/legal (existing reformatted)
├── ptfe-cover-sheet-heat-press.html          # Pre-cut PTFE sheets
└── ptfe-rolls-bulk.html                      # Bulk rolls (repositioned)
```

### Pages
```
pages/
├── craft-hub-landing-page.html               # Craft entry point
└── seo-content/
    ├── README.md                             # SEO page index
    ├── ptfe-sheet-for-heat-press.html
    ├── release-paper-for-stickers.html
    ├── diamond-painting-release-paper.html
    ├── release-paper-vs-parchment.html
    └── diamond-painting-dust-protection.html
```

### Configuration
```
config/
└── navigation-collections.md                  # Nav structure and collection definitions
```

### Creative
```
creative/
└── photography-shot-list.md                   # Photo requirements
```

---

## Success Metrics

Track these to measure impact:

1. **Conversion rate** on craft collection pages
2. **Bounce rate** on product pages
3. **Add-to-cart rate** on new products (letter size, 4x4 squares)
4. **Organic search traffic** to SEO pages
5. **Search rankings** for target keywords:
   - "teflon sheet for heat press"
   - "sticker storage paper"
   - "diamond painting release paper"
   - "silicone release paper"

---

## Questions to Decide

Before implementation, clarify:

1. **Subscription offering:** Are you keeping subscriptions? If yes, need proper UI. If no, remove selling plans.

2. **4.5" vs 4" squares:** Keep both or standardize? Market norm is 4".

3. **Coating clarity:** Is your release paper single-sided or double-sided? Be explicit.

4. **Pricing strategy:** How to price smaller pack sizes relative to bulk?

5. **Photography budget:** Doing in-house or hiring? Affects timeline.

---

*This guide was created based on comprehensive craft buyer research. Implementation should be done in phases, starting with highest-impact changes.*
