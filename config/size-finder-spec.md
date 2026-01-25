# Size Finder System Specification

The Size Finder is a core conversion feature that helps craft shoppers choose the correct product, size, and pack.

---

## Placement

The Size Finder should appear in these locations:

1. **Header navigation** - Visible link: "Size Finder"
2. **Homepage** - Section 4: "Pick Your Size" interactive module
3. **Product pages** - "Need help choosing?" link in buy box
4. **Collection pages** - Link in hero area

---

## User Interface

### Step 1: Project Type Selection

**Question:** "What are you making?"

**Options (tabs or large buttons):**

| Option | Icon | Description |
|--------|------|-------------|
| Sticker book pages | 📒 | Storing and organizing stickers |
| Transfers (UV DTF, HTV) | 🔄 | Transfer paper backing |
| Heat press protection | 🔥 | Cover sheets for heat press |
| Diamond painting | 💎 | Protecting adhesive canvas |
| Resin / glue cleanup | 🧪 | Work surface protection |

### Step 2: Context Questions (varies by project)

#### For Sticker Book Pages
- "How many stickers do you have?"
  - Just starting (< 100 stickers)
  - Growing collection (100-500)
  - Serious collector (500+)

#### For Heat Press Protection
- "What size is your heat press?"
  - 9x12 or smaller
  - 15x15
  - 16x20
  - 18x20 or larger
- "How often do you press?"
  - Occasionally (1-2x/week)
  - Regularly (several times/week)
  - Daily production

#### For Diamond Painting
- "How many canvases do you work on?"
  - 1 at a time
  - 2-3 active projects
  - Many projects / gifting

#### For Transfers
- "What size transfers?"
  - Letter size (8.5x11)
  - Legal size or larger

#### For Resin / Glue
- "What size workspace?"
  - Small (desk area)
  - Medium (craft table section)
  - Large (full table coverage)

### Step 3: Preference

- "Do you prefer reusable or disposable?"
  - Reusable (PTFE sheets, silicone mats)
  - Disposable (release paper)
  - Not sure / show me both

### Step 4: Results

Display 1-3 recommended products with:
- Product image
- Product name
- Size
- Recommended pack size
- "Why this?" explanation (1 sentence)
- Price
- Add to Cart button

---

## Recommendation Logic

### Sticker Book Pages

| Collection Size | Recommendation |
|-----------------|----------------|
| Just starting | Release Paper 8.5x11 - 25 pack |
| Growing | Release Paper 8.5x11 - 50 pack |
| Serious | Release Paper 8.5x11 - 100 pack |

**Why text:** "Letter size fits standard binders. Double-sided coating means stickers peel clean from both sides."

### Heat Press Protection

| Press Size | Frequency | Recommendation |
|------------|-----------|----------------|
| 9x12 | Any | PTFE Cover Sheet 12x15 |
| 15x15 | Occasional | PTFE Cover Sheet 16x20 - 1 pack |
| 15x15 | Regular | PTFE Cover Sheet 16x20 - 2 pack |
| 16x20 | Occasional | PTFE Cover Sheet 16x20 - 2 pack |
| 16x20 | Regular/Daily | PTFE Cover Sheet 16x20 - 5 pack |
| 18x20+ | Any | PTFE Cover Sheet 18x20 |

**Why text:** "Protects your platen from residue and provides consistent results. Replace when creased."

### Diamond Painting

| Projects | Recommendation |
|----------|----------------|
| 1 at a time | 4x4 Squares - 100 pack |
| 2-3 active | 4x4 Squares - 200 pack |
| Many / gifting | 4x4 Squares - 200 pack (x2) |

**Why text:** "4x4 squares are the standard size. Cover sections to keep adhesive clean while you work."

### Transfers

| Size | Recommendation |
|------|----------------|
| Letter | Release Paper 8.5x11 - 50 or 100 pack |
| Legal+ | Release Paper 8.5x14 - 100 pack |

**Why text:** "Silicone coating provides clean release for transfer applications."

### Resin / Glue

| Workspace | Recommendation |
|-----------|----------------|
| Small | Silicone Mat - Small |
| Medium | Silicone Mat - Medium |
| Large | Silicone Mat - Large |

**Why text:** "Cured resin and glue peel right off. Reusable work surface protection."

---

## Technical Implementation

### Option 1: Shopify Native (Simple)

Create as a page with JavaScript:
- `/pages/size-finder`
- Questions as clickable buttons
- Results populated from product JSON

### Option 2: Shopify App

Use a quiz/recommendation app:
- Octane AI
- ReConvert
- Custom build

### Option 3: Theme Section

Build as a reusable Shopify section:
- Include in homepage
- Include in product pages
- Include on dedicated page

---

## Data Requirements

### Product Metafields Needed

For the Size Finder to work, products must have these metafields:

```
kk.best_for          (list)     - ["stickers", "heat-press", "diamond-painting"]
kk.size              (string)   - "16x20", "8.5x11", "4x4"
kk.format            (string)   - "sheet", "square", "roll", "mat"
kk.reusable          (boolean)  - true/false
kk.pack_count        (number)   - 50, 100, 200
kk.bulk_tier         (string)   - "starter", "refill", "studio", "case"
kk.heat_press_size   (string)   - Size this fits: "15x15", "16x20", etc.
```

### Recommendation Engine Data

Store recommendations as JSON:

```json
{
  "sticker-starter": {
    "product_handle": "silicone-release-paper-letter-25",
    "why": "Letter size fits standard binders. Double-sided coating means stickers peel clean from both sides."
  },
  "heat-press-16x20-regular": {
    "product_handle": "ptfe-cover-sheet-16x20-2pack",
    "why": "Protects your platen from residue. 2-pack lets you rotate while one cools."
  }
}
```

---

## Mobile UX

On mobile:
- Each step is full-screen
- Large touch targets (48px minimum)
- Progress indicator at top
- "Back" button always visible
- Results show 1 product at a time with swipe

---

## Analytics Events

Track these events:
- `size_finder_started` - User opens Size Finder
- `size_finder_step_completed` - Each step completion with answer
- `size_finder_result_viewed` - Results displayed
- `size_finder_add_to_cart` - Product added from Size Finder
- `size_finder_abandoned` - User exits before results (with last step)

---

## A/B Testing Ideas

Test variations:
- Question order
- Number of steps (fewer vs more specific)
- Result display (1 product vs 3 products)
- "Why" text variations
- Button vs tab selection UI

---

## Copy for Size Finder

### Header
**Headline:** "Find Your Perfect Size"
**Subhead:** "Answer a few quick questions and we'll recommend the right product and pack size for your project."

### Progress Labels
- Step 1: "Your Project"
- Step 2: "Details"
- Step 3: "Preferences"
- Step 4: "Your Recommendation"

### Result CTA
**Button:** "Add to Cart"
**Secondary:** "See All Options" (links to collection)

### Empty State (if no match)
"We couldn't find a perfect match, but here are some options that might work:"
[Show related products]
