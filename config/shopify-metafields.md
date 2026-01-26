# Shopify Metafield Schema

This document defines all custom metafields needed for the Kraft & Kitchen craft store implementation.

---

## Namespace: `kk` (Kraft & Kitchen)

All custom metafields use the `kk` namespace to avoid conflicts.

---

## Product Metafields

### Core Product Data

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.best_for` | list.single_line_text_field | Use cases this product is best for | `["stickers", "diamond-painting", "heat-press"]` |
| `kk.size` | single_line_text_field | Product dimensions | `"16x20"`, `"8.5x11"`, `"4x4"` |
| `kk.size_inches` | single_line_text_field | Full size with units | `"16\" x 20\""`, `"8.5\" x 11\""` |
| `kk.size_cm` | single_line_text_field | Metric size | `"40.6cm x 50.8cm"` |
| `kk.format` | single_line_text_field | Product format | `"sheet"`, `"square"`, `"roll"`, `"mat"` |
| `kk.pack_count` | number_integer | Number of items in pack | `50`, `100`, `200` |
| `kk.bulk_tier` | single_line_text_field | Bulk category | `"starter"`, `"refill"`, `"studio"`, `"case"` |

### Material Specifications

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.material` | single_line_text_field | Primary material | `"PTFE-coated fiberglass"`, `"Silicone-coated paper"` |
| `kk.coating_sides` | single_line_text_field | Coating coverage | `"single"`, `"double"` |
| `kk.thickness_mil` | number_decimal | Thickness in mils | `3.0`, `4.0` |
| `kk.thickness_mm` | number_decimal | Thickness in mm | `0.076`, `0.102` |
| `kk.basis_weight` | single_line_text_field | Paper weight | `"40 lb"`, `"60 gsm"` |
| `kk.color` | single_line_text_field | Product color | `"White"`, `"Beige/Tan"`, `"Gray"` |

### Heat/Temperature Data

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.temp_max_f` | number_integer | Max temperature Fahrenheit | `500` |
| `kk.temp_max_c` | number_integer | Max temperature Celsius | `260` |
| `kk.heat_press_compatible` | boolean | Safe for heat press | `true`, `false` |
| `kk.heat_press_sizes` | list.single_line_text_field | Compatible press sizes | `["15x15", "16x20"]` |

### Compatibility

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.printer_compatible` | single_line_text_field | Printer compatibility | `"laser"`, `"inkjet"`, `"both"`, `"none"` |
| `kk.printer_notes` | multi_line_text_field | Printer usage notes | `"Print on uncoated side only. Test before production."` |
| `kk.reusable` | boolean | Is product reusable | `true`, `false` |
| `kk.reuse_notes` | single_line_text_field | Reuse guidance | `"Replace when creased or damaged"` |

### Care & Storage

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.care_instructions` | multi_line_text_field | Care instructions | `"Wipe clean with damp cloth. Store flat."` |
| `kk.storage_instructions` | single_line_text_field | Storage guidance | `"Store flat - do not fold"` |

### Marketing

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.one_liner` | single_line_text_field | Short value prop | `"Protects your heat press platen from residue"` |
| `kk.bullet_1` | single_line_text_field | Benefit bullet 1 | `"Reusable hundreds of times"` |
| `kk.bullet_2` | single_line_text_field | Benefit bullet 2 | `"Rated to 500°F"` |
| `kk.bullet_3` | single_line_text_field | Benefit bullet 3 | `"Wipes clean easily"` |

---

## Collection Metafields

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.collection_intro` | multi_line_text_field | Collection description | `"PTFE cover sheets protect your heat press..."` |
| `kk.default_sort` | single_line_text_field | Default sort order | `"best-selling"`, `"price-ascending"` |
| `kk.filter_groups` | json | Available filters | See JSON below |

### Filter Groups JSON Example

```json
{
  "filters": [
    {
      "label": "Size",
      "key": "size",
      "values": ["16x20", "18x20", "15x15", "12x15"]
    },
    {
      "label": "Pack Size",
      "key": "bulk_tier",
      "values": ["starter", "refill", "studio", "case"]
    },
    {
      "label": "Best For",
      "key": "best_for",
      "values": ["stickers", "heat-press", "diamond-painting"]
    }
  ]
}
```

---

## Page Metafields

| Key | Type | Description | Example Values |
|-----|------|-------------|----------------|
| `kk.page_type` | single_line_text_field | Page category | `"landing"`, `"guide"`, `"comparison"` |
| `kk.related_collection` | single_line_text_field | Related collection handle | `"ptfe-sheets"` |
| `kk.related_products` | list.product_reference | Featured products | Product references |

---

## Metafield Definitions (Shopify Admin)

### Creating Metafields in Shopify Admin

1. Go to **Settings → Custom data → Products**
2. Click **Add definition**
3. Use these settings:

#### Example: `kk.best_for`

```
Name: Best For
Namespace and key: kk.best_for
Description: Use cases this product is best for (stickers, heat-press, diamond-painting, etc.)
Type: List of single line text
Validation: None
```

#### Example: `kk.temp_max_f`

```
Name: Max Temperature (°F)
Namespace and key: kk.temp_max_f
Description: Maximum safe operating temperature in Fahrenheit
Type: Integer
Validation: Min 0, Max 1000
```

#### Example: `kk.coating_sides`

```
Name: Coating Sides
Namespace and key: kk.coating_sides
Description: Whether silicone coating is single-sided or double-sided
Type: Single line text
Validation: One of: single, double
```

---

## Liquid Access Examples

### In Product Template

```liquid
{% comment %} Display temperature rating {% endcomment %}
{% if product.metafields.kk.temp_max_f %}
  <p>Rated to {{ product.metafields.kk.temp_max_f }}°F
     ({{ product.metafields.kk.temp_max_c }}°C)</p>
{% endif %}

{% comment %} Display best-for badges {% endcomment %}
{% if product.metafields.kk.best_for %}
  <div class="best-for-badges">
    {% for use in product.metafields.kk.best_for.value %}
      <span class="badge">{{ use | capitalize }}</span>
    {% endfor %}
  </div>
{% endif %}

{% comment %} Display care instructions {% endcomment %}
{% if product.metafields.kk.care_instructions %}
  <div class="care-instructions">
    {{ product.metafields.kk.care_instructions | newline_to_br }}
  </div>
{% endif %}
```

### In Collection Template (Filtering)

```liquid
{% comment %} Filter by best_for metafield {% endcomment %}
{% assign filter_value = "stickers" %}
{% for product in collection.products %}
  {% if product.metafields.kk.best_for contains filter_value %}
    {% include 'product-card' %}
  {% endif %}
{% endfor %}
```

---

## Bulk Import Format

For importing metafields via CSV or app:

### CSV Headers

```
Handle,kk.best_for,kk.size,kk.format,kk.pack_count,kk.coating_sides,kk.temp_max_f,kk.reusable
```

### CSV Example Rows

```
ptfe-cover-sheet-16x20,"[""heat-press"",""sublimation""]",16x20,sheet,2,single,500,true
release-paper-letter-50,"[""stickers"",""transfers""]",8.5x11,sheet,50,double,,false
diamond-painting-squares-200,"[""diamond-painting""]",4x4,square,200,double,,false
```

---

## GraphQL Mutations

### Update Product Metafield

```graphql
mutation updateProductMetafield($input: ProductInput!) {
  productUpdate(input: $input) {
    product {
      metafields(first: 10) {
        edges {
          node {
            namespace
            key
            value
          }
        }
      }
    }
    userErrors {
      field
      message
    }
  }
}

# Variables
{
  "input": {
    "id": "gid://shopify/Product/123456789",
    "metafields": [
      {
        "namespace": "kk",
        "key": "best_for",
        "value": "[\"stickers\", \"transfers\"]",
        "type": "list.single_line_text_field"
      },
      {
        "namespace": "kk",
        "key": "temp_max_f",
        "value": "500",
        "type": "number_integer"
      }
    ]
  }
}
```

---

## Implementation Checklist

### Phase 1: Core Metafields
- [ ] `kk.best_for`
- [ ] `kk.size`
- [ ] `kk.format`
- [ ] `kk.pack_count`
- [ ] `kk.bulk_tier`

### Phase 2: Specifications
- [ ] `kk.material`
- [ ] `kk.coating_sides`
- [ ] `kk.thickness_mil`
- [ ] `kk.temp_max_f` / `kk.temp_max_c`
- [ ] `kk.heat_press_compatible`

### Phase 3: Marketing
- [ ] `kk.one_liner`
- [ ] `kk.bullet_1` / `kk.bullet_2` / `kk.bullet_3`
- [ ] `kk.care_instructions`
- [ ] `kk.reusable`

### Phase 4: Collection Metafields
- [ ] `kk.collection_intro`
- [ ] `kk.filter_groups`
- [ ] `kk.default_sort`
