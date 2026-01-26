# GitHub Secrets Setup for Nano Banana Pro

This guide explains how to set up the required secrets for automated AI image generation.

## Required Secrets

You need to add 3 secrets to your GitHub repository:

| Secret Name | Required | Description |
|-------------|----------|-------------|
| `GOOGLE_API_KEY` | ✅ Yes | Google AI Studio API key for Gemini |
| `SHOPIFY_STORE` | For uploads | Your Shopify store URL |
| `SHOPIFY_ACCESS_TOKEN` | For uploads | Shopify Admin API access token |

## Step 1: Get Google API Key

1. Go to [Google AI Studio](https://aistudio.google.com/apikey)
2. Sign in with your Google account
3. Click **"Create API Key"**
4. Copy the key (starts with `AIzaSy...`)

## Step 2: Get Shopify Credentials (Optional - for auto-upload)

### Store URL
Your Shopify store URL is: `your-store-name.myshopify.com`

### Access Token
1. Go to Shopify Admin > **Settings** > **Apps and sales channels**
2. Click **"Develop apps"** (you may need to enable this first)
3. Click **"Create an app"**
4. Name it "Image Generator" or similar
5. Click **"Configure Admin API scopes"**
6. Enable these scopes:
   - `write_products`
   - `read_products`
7. Click **"Save"**
8. Go to **"API credentials"** tab
9. Click **"Install app"**
10. Copy the **Admin API access token** (starts with `shpat_...`)

⚠️ **Important:** The access token is only shown once! Save it immediately.

## Step 3: Add Secrets to GitHub

1. Go to your repository on GitHub
2. Click **Settings** > **Secrets and variables** > **Actions**
3. Click **"New repository secret"** for each:

### GOOGLE_API_KEY
- Name: `GOOGLE_API_KEY`
- Value: Your Google AI Studio API key
- Click **"Add secret"**

### SHOPIFY_STORE
- Name: `SHOPIFY_STORE`
- Value: `your-store.myshopify.com` (without https://)
- Click **"Add secret"**

### SHOPIFY_ACCESS_TOKEN
- Name: `SHOPIFY_ACCESS_TOKEN`
- Value: Your Shopify access token (shpat_...)
- Click **"Add secret"**

## Step 4: Configure Product IDs

To enable auto-upload to specific products, you need to add Shopify product IDs to the presets:

1. Open `tools/nano_banana_generator.py`
2. Find the `PRODUCT_PRESETS` dictionary
3. For each preset, add your product ID:

```python
"ptfe-sheets": {
    "name": "PTFE Heat Press Cover Sheets",
    "product_id": "1234567890",  # <-- Add your product ID here
    ...
}
```

### How to Find Product IDs

1. Go to Shopify Admin > **Products**
2. Click on a product
3. Look at the URL: `https://admin.shopify.com/store/your-store/products/1234567890`
4. The number at the end (`1234567890`) is the product ID

## Usage

### Run via GitHub Actions

1. Go to **Actions** tab in your repository
2. Select **"Generate Product Images (Nano Banana Pro)"**
3. Click **"Run workflow"**
4. Select options:
   - **Mode:** `preset` or `custom`
   - **Preset:** Choose a product preset
   - **Upload to Shopify:** `true` to auto-upload
5. Click **"Run workflow"**

### Run Locally

```bash
# Set environment variables
export GOOGLE_API_KEY="your-key-here"
export SHOPIFY_STORE="your-store.myshopify.com"
export SHOPIFY_ACCESS_TOKEN="shpat_..."

# Test connection
python tools/nano_banana_generator.py --test

# Generate from preset
python tools/nano_banana_generator.py --preset ptfe-sheets

# Generate and upload
python tools/nano_banana_generator.py --preset ptfe-sheets --upload

# Custom prompt
python tools/nano_banana_generator.py "PTFE sheet on white background" -o output.png
```

## Available Presets

| Preset | Description | Images |
|--------|-------------|--------|
| `ptfe-sheets` | PTFE Heat Press Cover Sheets | 6 |
| `release-paper-letter` | Silicone Release Paper 8.5x11 | 6 |
| `diamond-painting-squares` | Diamond Painting 4x4 Squares | 4 |
| `silicone-mats` | Silicone Work Mats | 6 |
| `homepage-hero` | Homepage Hero Images | 3 |
| `project-tiles` | Shop By Project Category Tiles | 5 |

## Troubleshooting

### "API Key not found" error
- Verify the secret name is exactly `GOOGLE_API_KEY`
- Check the key is valid at https://aistudio.google.com/apikey

### "Shopify upload failed" error
- Verify `SHOPIFY_STORE` doesn't include `https://`
- Verify the access token has `write_products` scope
- Verify the product ID exists

### "No images generated" error
- Check the API has sufficient quota
- Try a different model (`gemini` vs `gemini-pro`)
- Check the workflow logs for specific errors

## Cost Estimates

| Model | Approximate Cost |
|-------|-----------------|
| Gemini 2.0 Flash | ~$0.02-0.04 per image |
| Gemini Pro | ~$0.04-0.08 per image |

Generating all presets (~30 images) costs approximately $0.60-$2.40.

## Security Notes

- Never commit API keys to the repository
- Use GitHub Secrets for all sensitive values
- Rotate Shopify tokens periodically
- The `.env` file is gitignored for local development
