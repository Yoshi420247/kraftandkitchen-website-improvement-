# Kraft & Kitchen - Deployment Guide

This guide walks you through deploying the website improvements to your live Shopify store.

---

## Quick Start

```bash
# 1. Install dependencies
pip install requests python-dotenv

# 2. Configure credentials
cp scripts/.env.example scripts/.env
# Edit scripts/.env with your Shopify API token

# 3. Test deployment (dry run)
cd scripts
python deploy_to_shopify.py --action all --dry-run

# 4. Deploy for real
python deploy_to_shopify.py --action all
```

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Getting Shopify API Credentials](#getting-shopify-api-credentials)
3. [Configuration](#configuration)
4. [Deployment Options](#deployment-options)
5. [Priority Fixes (Do First)](#priority-fixes-do-first)
6. [Manual Actions Required](#manual-actions-required)
7. [Troubleshooting](#troubleshooting)

---

## Prerequisites

### Software Requirements

- Python 3.8+
- pip (Python package manager)

### Install Dependencies

```bash
pip install requests python-dotenv
```

---

## Getting Shopify API Credentials

### Step 1: Create a Custom App

1. Log into your Shopify Admin at `kraftandkitchen.myshopify.com/admin`
2. Go to **Settings** (bottom left)
3. Click **Apps and sales channels**
4. Click **Develop apps** (top right)
5. Click **Create an app**
6. Name it: "Website Deployment Script"
7. Click **Create app**

### Step 2: Configure API Scopes

1. Click **Configure Admin API scopes**
2. Enable these scopes:
   - `write_products` - Update product descriptions
   - `read_products` - Read product data
   - `write_content` - Create/update pages
   - `read_content` - Read page data
   - `write_themes` - Update theme settings
   - `read_themes` - Read theme data
   - `write_inventory` - Manage inventory (optional)
3. Click **Save**

### Step 3: Install and Get Token

1. Click **Install app**
2. Click **Install** in the confirmation dialog
3. Click **Reveal token once** under Admin API access token
4. **Copy this token immediately** - it won't be shown again!

### Step 4: Store Your Token Securely

```bash
# Create your .env file
cp scripts/.env.example scripts/.env

# Edit the file and add your token
# NEVER commit .env to version control
```

Your `.env` file should look like:

```
SHOPIFY_STORE=kraftandkitchen
SHOPIFY_ACCESS_TOKEN=shpat_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
SHOPIFY_API_VERSION=2024-01
```

---

## Configuration

### Environment File Location

```
scripts/.env          # Your credentials (DO NOT COMMIT)
scripts/.env.example  # Template (safe to commit)
```

### Required Variables

| Variable | Description | Example |
|----------|-------------|---------|
| `SHOPIFY_STORE` | Your store name (without .myshopify.com) | `kraftandkitchen` |
| `SHOPIFY_ACCESS_TOKEN` | Admin API access token | `shpat_xxx...` |
| `SHOPIFY_API_VERSION` | API version | `2024-01` |

---

## Deployment Options

### Full Deployment

Deploy all improvements at once:

```bash
python deploy_to_shopify.py --action all
```

### Selective Deployment

Deploy specific components:

```bash
# Deploy only pages (SEO content + landing pages)
python deploy_to_shopify.py --action pages

# Deploy only product updates
python deploy_to_shopify.py --action products

# Create craft collections
python deploy_to_shopify.py --action collections

# Show priority fixes instructions
python deploy_to_shopify.py --action priority-fixes
```

### Dry Run Mode

See what would happen without making changes:

```bash
python deploy_to_shopify.py --action all --dry-run
```

---

## Priority Fixes (Do First)

These are conversion-critical issues that should be fixed immediately.

### Fix 1: Remove "Recurring Purchase" Warning

**Problem:** The release paper PDP shows subscription-style authorization text that scares buyers.

**Solution:**
1. Go to **Shopify Admin > Products**
2. Find "Silicone release paper" product
3. Scroll to **Purchase options** section
4. Remove any selling plan associations
5. OR check **Apps** for a subscription app and disable it for this product

**Verification:** Visit the product page - no "recurring or deferred purchase" text should appear.

### Fix 2: Remove $7,500 Item from Related Products

**Problem:** The custom printing product ($7,500) appears in related items, causing sticker shock.

**Solution:**
1. Go to **Online Store > Themes > Customize**
2. Navigate to a product page
3. Find the **Related Products** section
4. Either:
   - Exclude products tagged `b2b` or `custom-printing`
   - Create a manual "retail-cross-sells" collection
   - Hide custom products from all collections

### Fix 3: Fix Privacy Policy Placeholders

**Problem:** Privacy policy contains `[[INSERT...]]` placeholders.

**Solution:**
1. Go to **Settings > Policies > Privacy policy**
2. Search for `[[` to find placeholders
3. Replace with actual information:
   - Payment types: "Shop Pay, Visa, Mastercard, American Express, Discover, PayPal"
   - Tracking: "cookies and analytics for site functionality"
   - Contact: your actual support email
4. Save

### Fix 4: Standardize Shipping Origin & Phone

**Problem:** Shipping policy says Seattle but store may ship from Bellingham.

**Solution:**
1. Go to **Settings > Policies > Shipping policy**
2. Update to consistent location (Bellingham, WA)
3. Go to **Settings > Store details**
4. Verify phone number
5. Go to **Online Store > Themes > Customize > Footer**
6. Ensure contact info matches

---

## Manual Actions Required

Some improvements cannot be deployed via API and require manual work:

### 1. Product Photography

Upload new product images manually:
- Go to **Products > [Product] > Media**
- Add images from the shot list in `creative/photography-shot-list.md`

### 2. Theme Customization

For layout changes:
- Go to **Online Store > Themes > Customize**
- Add/configure sections per `BUILD-SPECIFICATION.md`

### 3. Navigation Updates

Update main menu:
- Go to **Online Store > Navigation**
- Update menus per `config/navigation-v2.md`

### 4. Review App Setup

Install a review app for customer photos:
1. Go to **Apps > Shopify App Store**
2. Search for "Product Reviews" or "Judge.me"
3. Install and configure

### 5. Product Tags

Add tags to products for collection rules:
- `heat-press`, `sublimation` - for heat press products
- `stickers`, `release-paper` - for sticker products
- `diamond-painting` - for DP products
- `best-seller`, `craft` - for best sellers collection

---

## What Gets Deployed

### Pages Created/Updated

| Page | URL | Source File |
|------|-----|-------------|
| Craft Hub | `/pages/craft-supplies` | `pages/craft-hub-landing-page.html` |
| Sticker Guide | `/pages/release-paper-for-stickers` | `pages/seo-content/release-paper-for-stickers.html` |
| Diamond Painting Guide | `/pages/diamond-painting-release-paper` | `pages/seo-content/diamond-painting-release-paper.html` |
| Dust Protection | `/pages/diamond-painting-dust-protection` | `pages/seo-content/diamond-painting-dust-protection.html` |
| PTFE Guide | `/pages/ptfe-sheet-for-heat-press` | `pages/seo-content/ptfe-sheet-for-heat-press.html` |
| Release vs Parchment | `/pages/release-paper-vs-parchment` | `pages/seo-content/release-paper-vs-parchment.html` |

### Collections Created

| Collection | Handle | Rules |
|------------|--------|-------|
| Heat Press + Sublimation | `heat-press-sublimation` | Tags: heat-press OR sublimation |
| Stickers + Decals | `stickers-decals` | Tags: stickers OR release-paper |
| Diamond Painting | `diamond-painting` | Tag: diamond-painting |
| Craft Best Sellers | `craft-best-sellers` | Tags: best-seller AND craft |

### Products Updated

| Product | Changes |
|---------|---------|
| Silicone Release Paper | New title, description, tags |

---

## Troubleshooting

### "SHOPIFY_ACCESS_TOKEN not set"

**Cause:** The `.env` file is missing or not configured.

**Solution:**
```bash
cp scripts/.env.example scripts/.env
# Edit scripts/.env and add your token
```

### "401 Unauthorized"

**Cause:** Invalid or expired access token.

**Solution:**
1. Go to Shopify Admin > Settings > Apps > Develop apps
2. Find your app
3. Generate a new token
4. Update `.env` with the new token

### "403 Forbidden"

**Cause:** Missing API scopes.

**Solution:**
1. Go to your app in Shopify Admin
2. Configure Admin API scopes
3. Add the missing scope (check error message)
4. Reinstall the app to apply new scopes

### "429 Too Many Requests"

**Cause:** Rate limiting.

**Solution:** The script handles this automatically with retry logic. If persistent, wait a few minutes and try again.

### "Page/Product not found"

**Cause:** The handle doesn't match what's in the store.

**Solution:**
1. Check the actual handle in Shopify Admin
2. Update the script or create the product/page first

---

## Rollback

If something goes wrong:

### Pages

Pages can be unpublished or deleted:
1. Go to **Online Store > Pages**
2. Find the page
3. Click to edit
4. Change visibility to "Hidden" or delete

### Collections

Collections can be deleted:
1. Go to **Products > Collections**
2. Find the collection
3. Click **Delete collection**

### Products

Product changes should be backed up before deployment. To restore:
1. Go to **Products > [Product]**
2. Edit to restore previous content

---

## Verification Checklist

After deployment, verify:

- [ ] SEO pages are accessible (e.g., `/pages/release-paper-for-stickers`)
- [ ] Craft Hub page loads correctly
- [ ] Collections appear in store navigation (if added)
- [ ] Product descriptions are updated
- [ ] No "recurring purchase" warning on release paper page
- [ ] Related products don't show B2B/custom items
- [ ] Privacy policy has no placeholders

---

## Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review `SHOPIFY_MANAGEMENT.md` for API reference
3. Check Shopify Admin for manual fixes

---

## Security Notes

- **Never commit `.env` to version control**
- **Rotate access tokens periodically**
- **Use minimum required API scopes**
- **Keep backup of current settings before major changes**
