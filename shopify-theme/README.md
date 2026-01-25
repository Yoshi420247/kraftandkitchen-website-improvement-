# Kraft & Kitchen Shopify Theme Files

Ready-to-use Liquid templates for the Kraft & Kitchen craft supply store.

## Installation

Copy these files into your Shopify theme:

1. **Sections** - Copy to `sections/` folder
2. **Snippets** - Copy to `snippets/` folder
3. **Templates** - Copy to `templates/` folder

## Sections

### Homepage
- `homepage-hero.liquid` - Full-width hero with background image and CTAs
- `shop-by-project.liquid` - 6 project tiles (Stickers, Transfers, Heat Press, etc.)
- `best-sellers.liquid` - Product grid from a collection
- `trust-strip.liquid` - Trust badges (shipping, reviews, security)
- `craft-hub.liquid` - Complete landing page for craft shoppers

### Product Pages
- `product-buy-box.liquid` - Above-the-fold buy box with variant buttons
- `product-specs-table.liquid` - Specifications table from metafields
- `product-faqs.liquid` - Accordion FAQs with schema.org markup
- `product-how-to-use.liquid` - 3-step visual instructions

### Collection Pages
- `collection-hero.liquid` - Collection title, description, Size Finder link
- `collection-product-grid.liquid` - Product grid with filters and sorting

## Snippets

- `mega-menu.liquid` - Navigation mega menu with 4 columns

## Templates

- `page.size-finder.liquid` - Interactive product recommendation quiz

## Metafields

These templates use custom metafields in the `kk` namespace. See `/config/shopify-metafields.md` for the full schema.

### Required Metafields
- `kk.best_for` - List of use cases
- `kk.size` - Product size
- `kk.pack_count` - Pack quantity
- `kk.material` - Product material
- `kk.temp_max_f` - Max temperature (for PTFE)
- `kk.reusable` - Boolean for reusable products

## CSS Custom Properties

Sections use these CSS variables (customize in theme settings):

```css
:root {
  --color-primary: #1A7F7F;      /* Teal */
  --color-primary-dark: #156666;
  --color-text: #2D2D2D;
  --color-text-muted: #6B6B6B;
  --color-background: #FAF8F5;   /* Warm cream */
  --color-border: #E5E5E5;
  --color-accent: #F59E0B;       /* Gold for stars/badges */
  --font-heading: 'Fraunces', Georgia, serif;
  --font-body: 'Inter', -apple-system, sans-serif;
}
```

## Product Import

See `/data/products-import.csv` for product data with all metafields populated.

## Customization

All sections include schema settings for theme editor customization:
- Headings and text
- Colors and backgrounds
- Block content (bullets, FAQs, steps)
- Collection references
- Link URLs

## Mobile Responsive

All templates are mobile-first with breakpoints at:
- 768px (tablet)
- 991px (desktop)
- 600px (small mobile)
