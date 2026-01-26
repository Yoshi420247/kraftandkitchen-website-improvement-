# Shopify Store Management - LLM Handoff Document

This document describes the tools, APIs, and methodologies for programmatically managing a Shopify store. Use this as a reference to make edits and improvements to any Shopify store.

---

## Table of Contents
1. [Authentication](#authentication)
2. [API Overview](#api-overview)
3. [Theme Settings Management](#theme-settings-management)
4. [Collection Management](#collection-management)
5. [Menu/Navigation Management](#menunavigation-management)
6. [File/Image Management](#fileimage-management)
7. [Page Management](#page-management)
8. [Product Management](#product-management)
9. [Metafield Management](#metafield-management)
10. [Inventory Management](#inventory-management)
11. [Shipping/Delivery Management](#shippingdelivery-management)
12. [Webhook Management](#webhook-management)
13. [Error Handling](#error-handling)
14. [Common Patterns & Gotchas](#common-patterns--gotchas)

---

## Authentication

### Required Credentials

Store credentials should be managed securely using environment variables:

```bash
# Set these in your environment (never commit to version control)
export SHOPIFY_STORE="kraftandkitchen"
export SHOPIFY_ACCESS_TOKEN="shpat_xxxxxxxxxxxxx"
export SHOPIFY_API_VERSION="2024-01"
```

```
Store URL: {store-name}.myshopify.com
Access Token: shpat_xxxxxxxxxxxxx (Admin API access token)
API Version: 2024-01 (or latest stable)
```

### Headers for All Requests
```bash
-H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
-H "Content-Type: application/json"
```

### Base URL Helper
```bash
SHOPIFY_BASE_URL="https://${SHOPIFY_STORE}.myshopify.com/admin/api/${SHOPIFY_API_VERSION}"
```

---

## API Overview

Shopify provides two APIs:

| API | Use Case | Base URL |
|-----|----------|----------|
| **REST API** | CRUD operations on resources (products, collections, pages, etc.) | `https://{store}.myshopify.com/admin/api/2024-01/` |
| **GraphQL API** | Complex queries, mutations, bulk operations | `https://{store}.myshopify.com/admin/api/2024-01/graphql.json` |

**When to use which:**
- REST: Simple CRUD, updating single resources
- GraphQL: Querying multiple resources, complex mutations (menus, files, delivery profiles), bulk operations

### API Version Management

Shopify releases new API versions quarterly. Always specify a version:
- **Stable versions**: `2024-01`, `2024-04`, `2024-07`, `2024-10`
- **Deprecation**: Versions are supported for ~12 months after release
- **Check current version**: Visit `https://{store}.myshopify.com/admin/api/versions.json`

---

## Theme Settings Management

Theme settings control homepage sections, colors, and layout. Settings are stored in `config/settings_data.json`.

### Get Theme ID
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/themes.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  | jq '.themes[] | select(.role == "main") | .id'
```

### Download Current Theme Settings
```bash
THEME_ID="your_theme_id"
curl -s -X GET "${SHOPIFY_BASE_URL}/themes/${THEME_ID}/assets.json?asset%5Bkey%5D=config/settings_data.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  | jq -r '.asset.value' > settings.json
```

### Update Theme Settings
```bash
# 1. Modify the JSON file
# 2. Create payload with escaped JSON value
# 3. PUT to update

curl -s -X PUT "${SHOPIFY_BASE_URL}/themes/${THEME_ID}/assets.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "asset": {
      "key": "config/settings_data.json",
      "value": "{escaped JSON string}"
    }
  }'
```

**Python helper for proper JSON escaping:**
```python
import json
import os

SHOPIFY_STORE = os.environ['SHOPIFY_STORE']
SHOPIFY_ACCESS_TOKEN = os.environ['SHOPIFY_ACCESS_TOKEN']

with open('settings.json', 'r') as f:
    settings = json.load(f)

# Modify settings
settings['current']['thumbnail_hover_enabled'] = False

# Create payload
payload = {
    "asset": {
        "key": "config/settings_data.json",
        "value": json.dumps(settings)
    }
}

with open('payload.json', 'w') as f:
    json.dump(payload, f)
```

### Theme Settings Structure
```json
{
  "current": {
    "thumbnail_hover_enabled": true,
    "collection_secondary_image": false,
    "sections": {
      "section_id": {
        "type": "featured-collection",
        "settings": {
          "collection": "collection-handle",
          "title": "Section Title"
        },
        "blocks": {
          "block_id": {
            "type": "block_type",
            "settings": { }
          }
        },
        "block_order": ["block_id_1", "block_id_2"]
      }
    }
  }
}
```

### Common Section Types
- `featured-collection` - Product grid from a collection
- `featured-promotions` - Promotional image blocks
- `collection-list` - Grid of collection links
- `image-text` - Image with text blocks
- `image-with-text-overlay` - Banner with overlay text
- `testimonial` - Customer testimonials
- `newsletter` - Email signup
- `slideshow` - Image carousel/slider
- `rich-text` - Formatted text content
- `video` - Embedded video content

### Image References in Theme Settings
Use format: `shopify://shop_images/{filename}`
```json
{
  "image": "shopify://shop_images/my-image.png"
}
```

---

## Collection Management

### List All Collections (REST)
```bash
# Smart Collections (rule-based)
curl -s -X GET "${SHOPIFY_BASE_URL}/smart_collections.json?limit=250" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"

# Custom Collections (manual)
curl -s -X GET "${SHOPIFY_BASE_URL}/custom_collections.json?limit=250" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Pagination for Large Datasets
```bash
# First page
curl -s -X GET "${SHOPIFY_BASE_URL}/smart_collections.json?limit=250" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -D headers.txt

# Check for Link header with next page
grep -i "link:" headers.txt

# Subsequent pages use page_info parameter from Link header
curl -s -X GET "${SHOPIFY_BASE_URL}/smart_collections.json?limit=250&page_info=eyJsYXN0X2lkIjo..." \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Get Collection with Product Count (GraphQL)
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ collectionByHandle(handle: \"collection-handle\") { id title productsCount { count } products(first: 10) { edges { node { title priceRangeV2 { minVariantPrice { amount } } } } } } }"
  }'
```

### Create Smart Collection
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/smart_collections.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "smart_collection": {
      "title": "Collection Title",
      "body_html": "<p>Description for SEO</p>",
      "rules": [
        {"column": "tag", "relation": "equals", "condition": "family:glass-rig"},
        {"column": "vendor", "relation": "equals", "condition": "Vendor Name"},
        {"column": "variant_price", "relation": "less_than", "condition": "300"}
      ],
      "disjunctive": false,
      "sort_order": "best-selling",
      "published": true
    }
  }'
```

**Rule columns:** `tag`, `title`, `type`, `vendor`, `variant_price`, `variant_compare_at_price`, `variant_weight`, `variant_inventory`, `variant_title`

**Rule relations:** `equals`, `not_equals`, `greater_than`, `less_than`, `starts_with`, `ends_with`, `contains`, `not_contains`

**Sort orders:** `manual`, `best-selling`, `alpha-asc`, `alpha-desc`, `price-desc`, `price-asc`, `created-desc`, `created`

**Disjunctive:** `false` = AND logic, `true` = OR logic

### Create Custom Collection (Manual)
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/custom_collections.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "custom_collection": {
      "title": "Featured Products",
      "body_html": "<p>Hand-picked selections</p>",
      "published": true,
      "sort_order": "manual"
    }
  }'
```

### Add Products to Custom Collection
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/collects.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "collect": {
      "product_id": 1234567890,
      "collection_id": 9876543210,
      "position": 1
    }
  }'
```

### Update Collection
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/smart_collections/{collection_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "smart_collection": {
      "id": {collection_id},
      "title": "New Title",
      "body_html": "<p>New description</p>",
      "image": {
        "src": "https://cdn.shopify.com/...",
        "alt": "Alt text"
      }
    }
  }'
```

### Delete Collection
```bash
curl -s -X DELETE "${SHOPIFY_BASE_URL}/smart_collections/{collection_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

---

## Menu/Navigation Management

Menus are managed via **GraphQL only**.

### Get All Menus
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ menus(first: 10) { edges { node { id handle title items { id title url } } } } }"
  }'
```

### Get Menu with Nested Items
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ menus(first: 10) { edges { node { id handle title items { id title url items { id title url } } } } } }"
  }'
```

### Update Menu
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation menuUpdate($id: ID!, $title: String!, $items: [MenuItemUpdateInput!]!) { menuUpdate(id: $id, title: $title, items: $items) { menu { id title } userErrors { field message } } }",
    "variables": {
      "id": "gid://shopify/Menu/123456789",
      "title": "Main Menu",
      "items": [
        {
          "title": "Shop All",
          "url": "/collections/all",
          "type": "HTTP"
        },
        {
          "title": "Dab Rigs",
          "resourceId": "gid://shopify/Collection/123456789",
          "type": "COLLECTION"
        }
      ]
    }
  }'
```

**Menu item types:**
- `HTTP` - External/custom URL (use `url` field)
- `COLLECTION` - Link to collection (use `resourceId`)
- `PRODUCT` - Link to product (use `resourceId`)
- `PAGE` - Link to page (use `resourceId`)
- `BLOG` - Link to blog (use `resourceId`)
- `CATALOG` - Link to product catalog
- `FRONTPAGE` - Link to homepage (no resourceId needed)

---

## File/Image Management

### Upload Image to Shopify Files (GraphQL)
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt ... on MediaImage { image { url } } } userErrors { field message } } }",
    "variables": {
      "files": [
        {
          "alt": "Image description",
          "contentType": "IMAGE",
          "originalSource": "https://example.com/image.jpg"
        }
      ]
    }
  }'
```

### Upload Multiple Files
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation fileCreate($files: [FileCreateInput!]!) { fileCreate(files: $files) { files { id alt ... on MediaImage { image { url } } } userErrors { field message } } }",
    "variables": {
      "files": [
        {"alt": "Image 1", "contentType": "IMAGE", "originalSource": "https://example.com/image1.jpg"},
        {"alt": "Image 2", "contentType": "IMAGE", "originalSource": "https://example.com/image2.jpg"},
        {"alt": "Image 3", "contentType": "IMAGE", "originalSource": "https://example.com/image3.jpg"}
      ]
    }
  }'
```

### Get Uploaded Files
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ files(first: 20, sortKey: CREATED_AT, reverse: true) { edges { node { ... on MediaImage { id alt image { url } createdAt } } } } }"
  }'
```

### Check File Processing Status
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ node(id: \"gid://shopify/MediaImage/123456789\") { ... on MediaImage { id status image { url } } } }"
  }'
```

**File statuses:** `UPLOADED`, `PROCESSING`, `READY`, `FAILED`

**Note:** After uploading, wait 2-3 seconds for processing before querying the URL.

### Delete File
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation fileDelete($fileIds: [ID!]!) { fileDelete(fileIds: $fileIds) { deletedFileIds userErrors { field message } } }",
    "variables": {
      "fileIds": ["gid://shopify/MediaImage/123456789"]
    }
  }'
```

### Using Uploaded Images in Theme
Extract filename from URL and use in theme settings:
```
URL: https://cdn.shopify.com/s/files/1/1234/5678/files/my-image.png?v=123
Theme reference: shopify://shop_images/my-image.png
```

---

## Page Management

### List All Pages
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/pages.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Get Single Page
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/pages/{page_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Create Page
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/pages.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "page": {
      "title": "About Us",
      "handle": "about-us",
      "body_html": "<h1>About Our Store</h1><p>Our story...</p>",
      "published": true,
      "template_suffix": ""
    }
  }'
```

### Update Page
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/pages/{page_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "page": {
      "id": {page_id},
      "title": "Page Title",
      "body_html": "<h1>Content</h1><p>Page content here</p>",
      "published": true
    }
  }'
```

### Unpublish Page
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/pages/{page_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"page": {"id": {page_id}, "published": false}}'
```

### Delete Page
```bash
curl -s -X DELETE "${SHOPIFY_BASE_URL}/pages/{page_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

---

## Product Management

### Get Products (GraphQL - better for complex queries)
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ products(first: 50, query: \"vendor:\\\"Vendor Name\\\"\") { edges { node { id title handle tags priceRangeV2 { minVariantPrice { amount } } } } } }"
  }'
```

### Get Products (REST)
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/products.json?limit=50" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Get Single Product
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/products/{product_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Create Product
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/products.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "title": "Product Name",
      "body_html": "<p>Product description</p>",
      "vendor": "Vendor Name",
      "product_type": "Category",
      "tags": "tag1, tag2, tag3",
      "status": "active",
      "variants": [
        {
          "price": "29.99",
          "sku": "SKU-001",
          "inventory_management": "shopify",
          "inventory_quantity": 100
        }
      ],
      "images": [
        {"src": "https://example.com/image.jpg", "alt": "Product image"}
      ]
    }
  }'
```

### Update Product
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/products/{product_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "id": {product_id},
      "title": "Updated Product Name",
      "body_html": "<p>Updated description</p>"
    }
  }'
```

### Update Product Tags
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/products/{product_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "id": {product_id},
      "tags": "tag1, tag2, family:glass-rig, material:glass"
    }
  }'
```

### Update Product Status (Publish/Unpublish)
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/products/{product_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "product": {
      "id": {product_id},
      "status": "draft"
    }
  }'
```

**Product statuses:** `active`, `draft`, `archived`

### Get Products in Collection
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ collectionByHandle(handle: \"collection-handle\") { products(first: 50, sortKey: BEST_SELLING) { edges { node { title priceRangeV2 { minVariantPrice { amount } } featuredImage { url } } } } } }"
  }'
```

### Delete Product
```bash
curl -s -X DELETE "${SHOPIFY_BASE_URL}/products/{product_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

---

## Metafield Management

Metafields store custom data on resources (products, collections, orders, etc.).

### Get Product Metafields
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/products/{product_id}/metafields.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Create Product Metafield
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/products/{product_id}/metafields.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "metafield": {
      "namespace": "custom",
      "key": "care_instructions",
      "value": "Hand wash only",
      "type": "single_line_text_field"
    }
  }'
```

### Common Metafield Types
- `single_line_text_field` - Short text
- `multi_line_text_field` - Long text
- `rich_text_field` - HTML content
- `number_integer` - Whole numbers
- `number_decimal` - Decimal numbers
- `boolean` - True/false
- `date` - Date (YYYY-MM-DD)
- `json` - JSON object
- `url` - URL/link
- `color` - Hex color code
- `product_reference` - Reference to another product
- `collection_reference` - Reference to a collection
- `file_reference` - Reference to a file

### Update Metafield
```bash
curl -s -X PUT "${SHOPIFY_BASE_URL}/metafields/{metafield_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "metafield": {
      "id": {metafield_id},
      "value": "New value"
    }
  }'
```

### Delete Metafield
```bash
curl -s -X DELETE "${SHOPIFY_BASE_URL}/metafields/{metafield_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Shop Metafields (Global Settings)
```bash
# Get shop metafields
curl -s -X GET "${SHOPIFY_BASE_URL}/metafields.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"

# Create shop metafield
curl -s -X POST "${SHOPIFY_BASE_URL}/metafields.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "metafield": {
      "namespace": "store_settings",
      "key": "announcement_bar_text",
      "value": "Free shipping on orders over $50!",
      "type": "single_line_text_field"
    }
  }'
```

---

## Inventory Management

### Get Inventory Levels
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/inventory_levels.json?inventory_item_ids={item_id}" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Get Inventory Item
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/inventory_items/{item_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Adjust Inventory Level
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/inventory_levels/adjust.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": 123456789,
    "inventory_item_id": 987654321,
    "available_adjustment": 10
  }'
```

### Set Inventory Level (Absolute)
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/inventory_levels/set.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": 123456789,
    "inventory_item_id": 987654321,
    "available": 50
  }'
```

### Get Locations
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/locations.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Connect Inventory Item to Location
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/inventory_levels/connect.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "location_id": 123456789,
    "inventory_item_id": 987654321
  }'
```

---

## Shipping/Delivery Management

### Get Delivery Profiles (GraphQL)
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "{ deliveryProfiles(first: 10) { edges { node { id name profileLocationGroups { locationGroupZones(first: 10) { edges { node { zone { id name } methodDefinitions(first: 20) { edges { node { id name rateProvider { ... on DeliveryRateDefinition { id price { amount } } } } } } } } } } } } } }"
  }'
```

### Delete Shipping Rate
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation deliveryProfileUpdate($id: ID!, $profile: DeliveryProfileInput!) { deliveryProfileUpdate(id: $id, profile: $profile) { profile { id } userErrors { field message } } }",
    "variables": {
      "id": "gid://shopify/DeliveryProfile/123456789",
      "profile": {
        "methodDefinitionsToDelete": ["gid://shopify/DeliveryMethodDefinition/987654321"]
      }
    }
  }'
```

### Get Shipping Zones (REST)
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/shipping_zones.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

---

## Webhook Management

Webhooks notify your application of events in real-time.

### List Webhooks
```bash
curl -s -X GET "${SHOPIFY_BASE_URL}/webhooks.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Create Webhook
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/webhooks.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "webhook": {
      "topic": "orders/create",
      "address": "https://your-app.com/webhooks/orders",
      "format": "json"
    }
  }'
```

### Common Webhook Topics
- `orders/create` - New order placed
- `orders/updated` - Order modified
- `orders/paid` - Order payment received
- `orders/fulfilled` - Order shipped
- `products/create` - New product added
- `products/update` - Product modified
- `products/delete` - Product removed
- `collections/create` - New collection
- `collections/update` - Collection modified
- `customers/create` - New customer
- `inventory_levels/update` - Stock changed
- `app/uninstalled` - App removed from store

### Delete Webhook
```bash
curl -s -X DELETE "${SHOPIFY_BASE_URL}/webhooks/{webhook_id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
```

### Webhook Verification
Verify webhook signatures to ensure authenticity:
```python
import hmac
import hashlib
import base64

def verify_webhook(data, hmac_header, secret):
    digest = hmac.new(
        secret.encode('utf-8'),
        data,
        hashlib.sha256
    ).digest()
    computed_hmac = base64.b64encode(digest).decode()
    return hmac.compare_digest(computed_hmac, hmac_header)
```

---

## Error Handling

### Common HTTP Status Codes

| Code | Meaning | Action |
|------|---------|--------|
| 200 | Success | Request completed |
| 201 | Created | Resource created |
| 400 | Bad Request | Check request format |
| 401 | Unauthorized | Verify access token |
| 403 | Forbidden | Check API permissions |
| 404 | Not Found | Verify resource ID/handle |
| 422 | Unprocessable | Validation error - check response body |
| 429 | Too Many Requests | Rate limited - implement backoff |
| 500 | Server Error | Retry with backoff |

### Handling Rate Limits
```bash
#!/bin/bash
# Retry with exponential backoff

max_retries=4
retry_count=0
base_delay=2

while [ $retry_count -lt $max_retries ]; do
  response=$(curl -s -w "\n%{http_code}" -X GET "${SHOPIFY_BASE_URL}/products.json" \
    -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}")

  http_code=$(echo "$response" | tail -n1)
  body=$(echo "$response" | sed '$d')

  if [ "$http_code" = "200" ]; then
    echo "$body"
    break
  elif [ "$http_code" = "429" ]; then
    delay=$((base_delay * (2 ** retry_count)))
    echo "Rate limited. Waiting ${delay}s..." >&2
    sleep $delay
    retry_count=$((retry_count + 1))
  else
    echo "Error: HTTP $http_code" >&2
    echo "$body" >&2
    break
  fi
done
```

### GraphQL Error Handling
```bash
response=$(curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"query": "..."}')

# Check for errors
errors=$(echo "$response" | jq '.errors')
user_errors=$(echo "$response" | jq '.data.*.userErrors')

if [ "$errors" != "null" ]; then
  echo "GraphQL errors: $errors" >&2
fi

if [ "$user_errors" != "null" ] && [ "$user_errors" != "[]" ]; then
  echo "User errors: $user_errors" >&2
fi
```

### Python Error Handler
```python
import requests
import time

class ShopifyAPI:
    def __init__(self, store, token, version="2024-01"):
        self.base_url = f"https://{store}.myshopify.com/admin/api/{version}"
        self.headers = {
            "X-Shopify-Access-Token": token,
            "Content-Type": "application/json"
        }

    def request(self, method, endpoint, data=None, max_retries=4):
        url = f"{self.base_url}/{endpoint}"

        for attempt in range(max_retries):
            response = requests.request(
                method, url, headers=self.headers, json=data
            )

            if response.status_code == 429:
                retry_after = int(response.headers.get('Retry-After', 2 ** attempt))
                time.sleep(retry_after)
                continue

            if response.status_code >= 500:
                time.sleep(2 ** attempt)
                continue

            response.raise_for_status()
            return response.json()

        raise Exception(f"Max retries exceeded for {endpoint}")
```

---

## Common Patterns & Gotchas

### 1. GraphQL ID Format
GraphQL uses global IDs: `gid://shopify/Collection/123456789`
REST uses numeric IDs: `123456789`

**Extract numeric ID from GraphQL ID:**
```bash
echo "gid://shopify/Collection/123456789" | grep -oE '[0-9]+$'
```

**Convert REST ID to GraphQL ID:**
```bash
RESOURCE_TYPE="Collection"
REST_ID="123456789"
GQL_ID="gid://shopify/${RESOURCE_TYPE}/${REST_ID}"
```

### 2. JSON Escaping for Theme Updates
Theme settings require double-escaping. Use Python or a proper JSON library:
```python
payload = {"asset": {"key": "config/settings_data.json", "value": json.dumps(settings)}}
```

### 3. Block IDs Must Be Unique
When adding blocks to theme sections, ensure block IDs are unique across ALL sections:
```json
"blocks": {
  "section1-block-1": { },
  "section1-block-2": { }
}
```
Not: `"block-1"`, `"block-2"` (may conflict with other sections)

### 4. Collection Images
Set collection images via REST API on the collection itself:
```bash
curl -X PUT "${SHOPIFY_BASE_URL}/smart_collections/{id}.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -d '{"smart_collection": {"image": {"src": "https://...", "alt": "..."}}}'
```

### 5. Rate Limiting
- REST: 40 requests/second (bucket with leaky bucket algorithm)
- GraphQL: Cost-based (check `throttleStatus` in response extensions)

**Check rate limit status in response headers:**
```
X-Shopify-Shop-Api-Call-Limit: 32/40
```

If rate limited, wait and retry with exponential backoff.

### 6. Webhook for Async Operations
Some operations (like file uploads) are async. Poll for completion or wait 2-3 seconds.

### 7. Theme Settings Validation
Invalid settings can break the theme. Always:
1. Download current settings first
2. Make incremental changes
3. Validate JSON before uploading
4. Test on a duplicate theme if possible

### 8. Collection Rule Limitations
- Max 60 rules per smart collection
- Some rule combinations can match unintended products
- Use `disjunctive: false` (AND) for precise matching

### 9. Handle vs ID
- **Handle**: URL-friendly slug (e.g., `my-collection`)
- **ID**: Numeric identifier (e.g., `123456789`)
- Handles can change; IDs are permanent
- Use handles for human-readable configs, IDs for programmatic operations

### 10. Variant Inventory
- Products have variants (even single-variant products)
- Inventory is tracked at the variant level, not product level
- Each variant has an `inventory_item_id` for stock management

### 11. Bulk Operations (GraphQL)
For large operations (1000+ items), use bulk operations:
```bash
curl -s -X POST "${SHOPIFY_BASE_URL}/graphql.json" \
  -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation { bulkOperationRunQuery(query: \"{ products { edges { node { id title } } } }\") { bulkOperation { id status } userErrors { field message } } }"
  }'
```

### 12. Testing Changes Safely
1. Create a duplicate theme for testing
2. Use the `preview_theme_id` parameter for orders
3. Test on a development store first
4. Keep backups of theme settings before major changes

---

## Quick Reference: Common Tasks

| Task | Method | Endpoint/Query |
|------|--------|----------------|
| Get theme ID | REST GET | `/themes.json` |
| Update homepage section | REST PUT | `/themes/{id}/assets.json` (settings_data.json) |
| Create collection | REST POST | `/smart_collections.json` |
| Update collection | REST PUT | `/smart_collections/{id}.json` |
| Set collection image | REST PUT | `/smart_collections/{id}.json` with `image` object |
| Delete collection | REST DELETE | `/smart_collections/{id}.json` |
| Update menu | GraphQL | `menuUpdate` mutation |
| Upload image | GraphQL | `fileCreate` mutation |
| Get products by price | GraphQL | `products(query: "...")` |
| Update product tags | REST PUT | `/products/{id}.json` |
| Update page content | REST PUT | `/pages/{id}.json` |
| Create metafield | REST POST | `/{resource}/{id}/metafields.json` |
| Adjust inventory | REST POST | `/inventory_levels/adjust.json` |
| Delete shipping rate | GraphQL | `deliveryProfileUpdate` with `methodDefinitionsToDelete` |
| Create webhook | REST POST | `/webhooks.json` |

---

## Example Workflow: Homepage Redesign

1. **Get current theme settings**
   ```bash
   curl -X GET "${SHOPIFY_BASE_URL}/themes/${THEME_ID}/assets.json?asset[key]=config/settings_data.json" \
     -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}"
   ```

2. **Identify section IDs** (in `sections` object of settings)

3. **Create new collections if needed**
   ```bash
   curl -X POST "${SHOPIFY_BASE_URL}/smart_collections.json" \
     -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
     -d '{...}'
   ```

4. **Upload images if needed**
   ```bash
   # GraphQL fileCreate mutation
   ```

5. **Update theme settings JSON**
   - Modify section settings
   - Update collection handles
   - Add image references

6. **Push updated settings**
   ```bash
   curl -X PUT "${SHOPIFY_BASE_URL}/themes/${THEME_ID}/assets.json" \
     -H "X-Shopify-Access-Token: ${SHOPIFY_ACCESS_TOKEN}" \
     -d '{"asset": {"key": "config/settings_data.json", "value": "..."}}'
   ```

7. **Verify changes** on storefront

---

## Security Best Practices

1. **Never commit credentials** - Use environment variables
2. **Rotate access tokens** periodically
3. **Use minimum required scopes** for API access
4. **Verify webhook signatures** before processing
5. **Sanitize user input** before API calls
6. **Use HTTPS** for all webhook endpoints
7. **Log API calls** for auditing (exclude sensitive data)
8. **Implement rate limiting** on your webhook endpoints

---

## Environment Setup Template

```bash
# .env file (DO NOT COMMIT)
SHOPIFY_STORE="your-store-name"
SHOPIFY_ACCESS_TOKEN="shpat_xxxxxxxxxxxxx"
SHOPIFY_API_VERSION="2024-01"

# Load in your scripts
source .env
export SHOPIFY_BASE_URL="https://${SHOPIFY_STORE}.myshopify.com/admin/api/${SHOPIFY_API_VERSION}"
```

---

## Useful Tools

- **Shopify Admin API GraphiQL**: `https://{store}.myshopify.com/admin/api/2024-01/graphql.json` (with GraphQL client)
- **Shopify CLI**: `npm install -g @shopify/cli` for theme development
- **jq**: JSON processor for parsing responses
- **Postman/Insomnia**: API testing with saved collections
