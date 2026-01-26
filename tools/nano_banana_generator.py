#!/usr/bin/env python3
"""
Kraft & Kitchen - Nano Banana Pro Image Generator
Uses Google Gemini 3 Pro Image API for AI-powered product photography

Features:
- Competitor reference image search (DuckDuckGo)
- Multi-image generation with variants
- Direct Shopify product upload
- 2K/4K output quality

Usage:
  python nano_banana_generator.py --preset ptfe-sheets --upload
  python nano_banana_generator.py "PTFE cover sheet on white background" -o output.png
  python nano_banana_generator.py --list-presets
  python nano_banana_generator.py --test
"""

import os
import sys
import json
import base64
import argparse
import re
import time
from pathlib import Path
from datetime import datetime

try:
    import requests
except ImportError:
    print("Installing requests...")
    os.system(f"{sys.executable} -m pip install requests")
    import requests

# =============================================================================
# CONFIGURATION
# =============================================================================

# API Keys (set via environment variables or GitHub Secrets)
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY", "")
SHOPIFY_STORE = os.environ.get("SHOPIFY_STORE", "")
SHOPIFY_ACCESS_TOKEN = os.environ.get("SHOPIFY_ACCESS_TOKEN", "")

# API Endpoints
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"

# Available models
MODELS = {
    "gemini": {
        "id": "gemini-2.0-flash-exp-image-generation",
        "name": "Gemini 2.0 Flash (Image Generation)",
        "output": "2K",
        "description": "Fast image generation model"
    },
    "gemini-pro": {
        "id": "gemini-2.0-flash-exp-image-generation",
        "name": "Gemini Pro Image",
        "output": "2K",
        "description": "High quality image generation"
    }
}

DEFAULT_MODEL = "gemini"

# Output directory
OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# KRAFT & KITCHEN PRODUCT PRESETS
# =============================================================================

PRODUCT_PRESETS = {
    "ptfe-sheets": {
        "name": "PTFE Heat Press Cover Sheets",
        "product_id": None,  # Set your Shopify product ID here
        "search_terms": [
            "PTFE heat press cover sheet product photo",
            "teflon sheet heat press white background",
            "heat press protective sheet professional photography",
            "PTFE coated fiberglass sheet product"
        ],
        "variants": [
            {"size": "12x15", "name": "12x15 inches", "use_case": "Craft press"},
            {"size": "16x20", "name": "16x20 inches", "use_case": "Standard press"},
            {"size": "18x20", "name": "18x20 inches", "use_case": "Commercial press"},
        ],
        "base_prompt": """Professional e-commerce product photograph of a PTFE heat press cover sheet, {size}.
The sheet is a beige/tan color PTFE-coated fiberglass material, shown flat on a pure white seamless background.
The sheet has a subtle woven texture visible. Soft shadow beneath for depth.
{use_case_detail}
Studio lighting, sharp focus, professional product photography style.
CRITICAL: ABSOLUTELY NO text, watermarks, labels, logos, or branding of any kind.""",
        "use_case_prompts": {
            "Craft press": "Compact size perfect for smaller heat press machines.",
            "Standard press": "Standard size for most home and small business heat presses.",
            "Commercial press": "Large size for commercial and industrial heat press applications."
        },
        "aspect_ratio": "1:1",
        "num_images": 2
    },

    "release-paper-letter": {
        "name": "Silicone Release Paper - Letter Size",
        "product_id": None,
        "search_terms": [
            "silicone release paper stack product photo",
            "parchment paper sheets white background",
            "release liner paper professional photography",
            "sticker backing paper product shot"
        ],
        "variants": [
            {"pack": "25", "name": "25 Pack", "audience": "Starter"},
            {"pack": "50", "name": "50 Pack", "audience": "Growing collection"},
            {"pack": "100", "name": "100 Pack", "audience": "Serious collector"},
        ],
        "base_prompt": """Professional e-commerce product photograph of a stack of {pack} white silicone release paper sheets, 8.5x11 inch letter size.
The paper stack is shown at a slight angle on a pure white seamless background.
Clean white paper with subtle sheen from silicone coating visible.
Kraft paper belly band or packaging wrap around the stack.
{audience_detail}
Studio lighting, crisp and clean, professional product photography.
CRITICAL: ABSOLUTELY NO text, watermarks, labels, logos, or branding of any kind.""",
        "audience_prompts": {
            "Starter": "Small neat stack, approachable for beginners.",
            "Growing collection": "Medium stack showing good value.",
            "Serious collector": "Substantial stack emphasizing bulk quantity and value."
        },
        "aspect_ratio": "1:1",
        "num_images": 2
    },

    "diamond-painting-squares": {
        "name": "Diamond Painting Release Paper Squares",
        "product_id": None,
        "search_terms": [
            "diamond painting cover paper product photo",
            "release paper squares craft supplies",
            "diamond art protective sheets white background",
            "small paper squares stack product photography"
        ],
        "variants": [
            {"pack": "100", "name": "100 Pack", "description": "Standard pack"},
            {"pack": "200", "name": "200 Pack", "description": "Value pack"},
        ],
        "base_prompt": """Professional e-commerce product photograph of a stack of {pack} white 4x4 inch release paper squares for diamond painting.
The small paper squares are stacked neatly, with a few squares fanned out elegantly to show quantity.
Pure white seamless background. The squares have a subtle silicone sheen.
{description_detail}
Clean, bright studio lighting, professional product photography for craft supplies.
CRITICAL: ABSOLUTELY NO text, watermarks, labels, logos, or branding of any kind.""",
        "description_prompts": {
            "Standard pack": "Compact stack showing precision-cut squares.",
            "Value pack": "Larger stack emphasizing the generous quantity."
        },
        "aspect_ratio": "1:1",
        "num_images": 2
    },

    "silicone-mats": {
        "name": "Silicone Work Mats",
        "product_id": None,
        "search_terms": [
            "silicone craft mat product photo",
            "resin work mat white background",
            "silicone baking mat professional photography",
            "craft silicone mat product shot"
        ],
        "variants": [
            {"size": "small", "name": "Small (12x16)", "color": "Gray"},
            {"size": "medium", "name": "Medium (18x24)", "color": "Gray"},
            {"size": "large", "name": "Large (24x36)", "color": "Gray"},
        ],
        "base_prompt": """Professional e-commerce product photograph of a {color} silicone work mat, {name}.
The mat is shown flat on a pure white seamless background with one corner slightly lifted to show flexibility and thickness.
Smooth silicone surface with subtle texture. {size_detail}
Clean, professional studio lighting, e-commerce product photography style.
CRITICAL: ABSOLUTELY NO text, watermarks, labels, logos, or branding of any kind.""",
        "size_prompts": {
            "small": "Compact size ideal for desk workspaces and small projects.",
            "medium": "Medium size perfect for craft table sections.",
            "large": "Large size for full table coverage and big projects."
        },
        "aspect_ratio": "1:1",
        "num_images": 2
    },

    "homepage-hero": {
        "name": "Homepage Hero Images",
        "product_id": None,
        "search_terms": [
            "craft workspace flat lay product photography",
            "heat press studio professional photo",
            "craft supplies organized desk white background",
            "maker workspace overhead shot"
        ],
        "variants": [
            {"scene": "craft-studio", "name": "Craft Studio Hero"},
            {"scene": "heat-press", "name": "Heat Press Hero"},
            {"scene": "sticker-making", "name": "Sticker Making Hero"},
        ],
        "base_prompt": """Professional wide-angle hero photograph for e-commerce homepage.
{scene_description}
Bright, aspirational maker aesthetic. Soft natural window lighting.
Leave clear negative space on the left third for text overlay.
High-end lifestyle product photography, 16:9 aspect ratio.
CRITICAL: ABSOLUTELY NO text, watermarks, labels, logos, or branding of any kind.""",
        "scene_prompts": {
            "craft-studio": "Organized craft workspace with PTFE sheets, release paper stacks, silicone mat, and craft tools arranged neatly on a warm off-white surface.",
            "heat-press": "Heat press workstation with a modern clamshell press, blank t-shirts, colorful vinyl rolls, and PTFE cover sheets.",
            "sticker-making": "Sticker maker's desk with cutting machine, release paper sheets, colorful sticker sheets, and organizing supplies."
        },
        "aspect_ratio": "16:9",
        "num_images": 1
    },

    "project-tiles": {
        "name": "Shop By Project Tiles",
        "product_id": None,
        "search_terms": [
            "craft project flat lay photography",
            "sticker collection aesthetic photo",
            "diamond painting supplies product shot",
            "heat press project professional photo"
        ],
        "variants": [
            {"project": "stickers", "name": "Stickers & Sticker Books"},
            {"project": "heat-press", "name": "Heat Press & HTV"},
            {"project": "diamond-painting", "name": "Diamond Painting"},
            {"project": "transfers", "name": "Transfers & DTF"},
            {"project": "resin", "name": "Resin & Glue"},
        ],
        "base_prompt": """Professional square product photograph for e-commerce category tile.
{project_description}
Top-down flat lay on warm off-white or kraft-toned surface.
Bright, high clarity, professional studio lighting.
Square 1:1 aspect ratio crop.
CRITICAL: ABSOLUTELY NO text, watermarks, labels, logos, or branding of any kind.""",
        "project_prompts": {
            "stickers": "White release paper sheet with 6-8 colorful kiss-cut stickers arranged neatly. One sticker partially peeled showing clean release. Small weeding tool and binder clip as props.",
            "heat-press": "Folded beige PTFE cover sheet with kraft paper belly band. Colorful HTV design, heat-resistant glove, and small timer as props.",
            "diamond-painting": "Stack of 4x4 white release paper squares fanned out elegantly. Diamond painting tray with colorful sparkly drills, applicator pen visible.",
            "transfers": "Release paper sheet with a colorful UV DTF transfer design. Squeegee, transfer tape roll, and scissors as props.",
            "resin": "Gray silicone mat with small cured resin pieces in various shapes, one piece mid-peel showing easy release. Mixing cups and stir sticks as props."
        },
        "aspect_ratio": "1:1",
        "num_images": 1
    }
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def search_competitor_images(search_terms: list, max_images: int = 6) -> list:
    """
    Search DuckDuckGo for competitor product images to use as references.
    Returns list of image URLs.
    """
    print(f"\n🔍 Searching for competitor reference images...")

    all_images = []

    for term in search_terms:
        try:
            # DuckDuckGo image search API
            url = "https://duckduckgo.com/"
            params = {"q": term}

            session = requests.Session()
            session.headers.update({
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            })

            # Get search token
            res = session.get(url, params=params, timeout=10)

            # Search for images
            search_url = f"https://duckduckgo.com/i.js"
            params = {
                "q": term,
                "o": "json",
                "p": 1,
                "s": 0,
                "u": "bing"
            }

            res = session.get(search_url, params=params, timeout=10)
            if res.status_code == 200:
                data = res.json()
                results = data.get("results", [])

                for result in results[:3]:  # Get up to 3 per search term
                    image_url = result.get("image")
                    if image_url and image_url.startswith("http"):
                        all_images.append(image_url)
                        print(f"  ✓ Found: {image_url[:60]}...")

                        if len(all_images) >= max_images:
                            break

            if len(all_images) >= max_images:
                break

            time.sleep(0.5)  # Rate limiting

        except Exception as e:
            print(f"  ⚠ Search failed for '{term}': {e}")
            continue

    print(f"  Found {len(all_images)} reference images")
    return all_images[:max_images]


def download_image(url: str, timeout: int = 15) -> bytes:
    """Download image from URL and return bytes."""
    try:
        response = requests.get(url, timeout=timeout, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        })
        if response.status_code == 200:
            return response.content
    except Exception as e:
        print(f"  ⚠ Failed to download {url[:50]}...: {e}")
    return None


def generate_image_gemini(
    prompt: str,
    reference_images: list = None,
    model_key: str = DEFAULT_MODEL,
    aspect_ratio: str = "1:1"
) -> bytes:
    """
    Generate image using Google Gemini API.

    Args:
        prompt: Text description of image to generate
        reference_images: List of image bytes to use as references
        model_key: Model to use (gemini, gemini-pro)
        aspect_ratio: Output aspect ratio (1:1, 16:9, 9:16, 4:3, 3:4)

    Returns:
        Generated image as bytes, or None on failure
    """
    if not GOOGLE_API_KEY:
        print("❌ Error: GOOGLE_API_KEY not set")
        return None

    model_info = MODELS.get(model_key, MODELS[DEFAULT_MODEL])
    model_id = model_info["id"]

    print(f"\n🎨 Generating image with {model_info['name']}...")
    print(f"   Prompt: {prompt[:100]}...")

    # Build request parts
    parts = []

    # Add reference images if provided
    if reference_images:
        print(f"   Using {len(reference_images)} reference images")
        for i, img_data in enumerate(reference_images):
            if img_data:
                parts.append({
                    "inline_data": {
                        "mime_type": "image/jpeg",
                        "data": base64.b64encode(img_data).decode("utf-8")
                    }
                })

    # Add the prompt
    parts.append({"text": prompt})

    # Build request body
    request_body = {
        "contents": [{
            "parts": parts
        }],
        "generationConfig": {
            "responseModalities": ["TEXT", "IMAGE"]
        }
    }

    # Make API request
    url = GEMINI_API_URL.format(model=model_id)
    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GOOGLE_API_KEY
    }

    try:
        response = requests.post(url, headers=headers, json=request_body, timeout=120)

        if response.status_code != 200:
            print(f"❌ API Error {response.status_code}: {response.text[:500]}")
            return None

        data = response.json()

        # Extract generated image from response
        candidates = data.get("candidates", [])
        if not candidates:
            print("❌ No candidates in response")
            return None

        parts = candidates[0].get("content", {}).get("parts", [])

        for part in parts:
            if "inline_data" in part:
                image_data = part["inline_data"].get("data")
                if image_data:
                    print("   ✓ Image generated successfully")
                    return base64.b64decode(image_data)
            elif "text" in part:
                print(f"   AI response: {part['text'][:100]}...")

        print("❌ No image in response")
        return None

    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return None
    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def upload_to_shopify(image_data: bytes, product_id: str, alt_text: str = "", position: int = 1) -> bool:
    """
    Upload image to Shopify product.

    Args:
        image_data: Image bytes
        product_id: Shopify product ID
        alt_text: Alt text for SEO
        position: Image position (1 = featured)

    Returns:
        True on success, False on failure
    """
    if not SHOPIFY_STORE or not SHOPIFY_ACCESS_TOKEN:
        print("❌ Shopify credentials not configured")
        return False

    if not product_id:
        print("❌ No product ID specified")
        return False

    print(f"\n📤 Uploading to Shopify product {product_id}...")

    url = f"https://{SHOPIFY_STORE}/admin/api/2024-01/products/{product_id}/images.json"
    headers = {
        "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
        "Content-Type": "application/json"
    }

    payload = {
        "image": {
            "attachment": base64.b64encode(image_data).decode("utf-8"),
            "position": position,
            "alt": alt_text or "Product image"
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload, timeout=60)

        if response.status_code in [200, 201]:
            print("   ✓ Uploaded successfully")
            return True
        else:
            print(f"❌ Upload failed: {response.status_code} - {response.text[:200]}")
            return False

    except Exception as e:
        print(f"❌ Upload error: {e}")
        return False


def generate_from_preset(preset_key: str, upload: bool = False, model_key: str = DEFAULT_MODEL):
    """
    Generate images for all variants in a product preset.

    Args:
        preset_key: Key from PRODUCT_PRESETS
        upload: Whether to upload to Shopify
        model_key: Model to use
    """
    if preset_key not in PRODUCT_PRESETS:
        print(f"❌ Unknown preset: {preset_key}")
        print(f"   Available presets: {', '.join(PRODUCT_PRESETS.keys())}")
        return

    preset = PRODUCT_PRESETS[preset_key]
    print(f"\n{'='*60}")
    print(f"🎯 Generating images for: {preset['name']}")
    print(f"{'='*60}")

    # Search for competitor reference images
    reference_urls = search_competitor_images(preset.get("search_terms", []))

    # Download reference images
    reference_images = []
    for url in reference_urls:
        img_data = download_image(url)
        if img_data:
            reference_images.append(img_data)

    print(f"   Downloaded {len(reference_images)} reference images")

    # Generate images for each variant
    generated_count = 0
    for variant in preset.get("variants", [{"name": "Default"}]):
        print(f"\n--- Variant: {variant.get('name', 'Default')} ---")

        # Build prompt with variant details
        prompt = preset["base_prompt"]

        # Replace variant placeholders
        for key, value in variant.items():
            prompt = prompt.replace("{" + key + "}", str(value))

        # Add variant-specific details from prompts dict
        for prompt_key in ["use_case_prompts", "audience_prompts", "description_prompts",
                          "size_prompts", "scene_prompts", "project_prompts", "material_prompts"]:
            if prompt_key in preset:
                detail_key = prompt_key.replace("_prompts", "")
                if detail_key in variant:
                    detail_value = preset[prompt_key].get(variant[detail_key], "")
                    prompt = prompt.replace("{" + detail_key + "_detail}", detail_value)
                    prompt = prompt.replace("{" + detail_key + "_description}", detail_value)

        # Clean up any remaining placeholders
        prompt = re.sub(r'\{[^}]+\}', '', prompt)

        # Generate multiple images per variant
        num_images = preset.get("num_images", 1)
        aspect_ratio = preset.get("aspect_ratio", "1:1")

        for i in range(num_images):
            image_data = generate_image_gemini(
                prompt=prompt,
                reference_images=reference_images,
                model_key=model_key,
                aspect_ratio=aspect_ratio
            )

            if image_data:
                # Save locally
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                variant_slug = variant.get("name", "default").lower().replace(" ", "_")
                filename = f"kk_{preset_key}_{variant_slug}_{i+1}_{timestamp}.png"
                filepath = OUTPUT_DIR / filename

                with open(filepath, "wb") as f:
                    f.write(image_data)
                print(f"   💾 Saved: {filepath}")

                generated_count += 1

                # Upload to Shopify if requested
                if upload and preset.get("product_id"):
                    alt_text = f"{preset['name']} - {variant.get('name', '')}"
                    upload_to_shopify(image_data, preset["product_id"], alt_text)

            time.sleep(1)  # Rate limiting between generations

    print(f"\n{'='*60}")
    print(f"✅ Generated {generated_count} images for {preset['name']}")
    print(f"{'='*60}")


def test_api_connection():
    """Test the Gemini API connection."""
    print("\n🧪 Testing Gemini API connection...")

    if not GOOGLE_API_KEY:
        print("❌ GOOGLE_API_KEY not set")
        print("   Set it via: export GOOGLE_API_KEY=your_key")
        return False

    print(f"   API Key: {GOOGLE_API_KEY[:10]}...{GOOGLE_API_KEY[-4:]}")

    # Simple text generation test
    model_id = MODELS[DEFAULT_MODEL]["id"]
    url = GEMINI_API_URL.format(model=model_id)

    headers = {
        "Content-Type": "application/json",
        "x-goog-api-key": GOOGLE_API_KEY
    }

    request_body = {
        "contents": [{
            "parts": [{"text": "Say 'API connection successful' in exactly those words."}]
        }]
    }

    try:
        response = requests.post(url, headers=headers, json=request_body, timeout=30)

        if response.status_code == 200:
            print("✅ API connection successful!")
            return True
        else:
            print(f"❌ API Error {response.status_code}")
            print(f"   Response: {response.text[:300]}")
            return False

    except Exception as e:
        print(f"❌ Connection error: {e}")
        return False


def list_presets():
    """List all available product presets."""
    print("\n📋 Available Product Presets:")
    print("-" * 50)

    for key, preset in PRODUCT_PRESETS.items():
        variants = len(preset.get("variants", []))
        num_images = preset.get("num_images", 1)
        total = variants * num_images

        print(f"\n  {key}")
        print(f"    Name: {preset['name']}")
        print(f"    Variants: {variants}")
        print(f"    Images per variant: {num_images}")
        print(f"    Total images: {total}")

        if preset.get("product_id"):
            print(f"    Shopify Product ID: {preset['product_id']}")
        else:
            print(f"    Shopify Product ID: Not configured")


def list_models():
    """List available Gemini models."""
    print("\n🤖 Available Models:")
    print("-" * 50)

    for key, model in MODELS.items():
        print(f"\n  {key}")
        print(f"    Model ID: {model['id']}")
        print(f"    Name: {model['name']}")
        print(f"    Output: {model['output']}")
        print(f"    Description: {model['description']}")


# =============================================================================
# CLI INTERFACE
# =============================================================================

def main():
    parser = argparse.ArgumentParser(
        description="Kraft & Kitchen - AI Product Image Generator (Nano Banana Pro)",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s --test                           Test API connection
  %(prog)s --list-presets                   List available presets
  %(prog)s --preset ptfe-sheets             Generate PTFE sheet images
  %(prog)s --preset ptfe-sheets --upload    Generate and upload to Shopify
  %(prog)s "PTFE sheet on white" -o out.png Generate custom image
        """
    )

    parser.add_argument("prompt", nargs="?", help="Custom prompt for image generation")
    parser.add_argument("-o", "--output", help="Output filename for custom prompt")
    parser.add_argument("--preset", help="Generate from product preset")
    parser.add_argument("--upload", action="store_true", help="Upload to Shopify")
    parser.add_argument("--model", default=DEFAULT_MODEL, choices=MODELS.keys(), help="Model to use")
    parser.add_argument("--reference", nargs="+", help="Reference image files")
    parser.add_argument("--search-competitors", action="store_true", help="Search for competitor images as reference")
    parser.add_argument("--test", action="store_true", help="Test API connection")
    parser.add_argument("--list-presets", action="store_true", help="List available presets")
    parser.add_argument("--list-models", action="store_true", help="List available models")

    args = parser.parse_args()

    # Handle info commands
    if args.test:
        test_api_connection()
        return

    if args.list_presets:
        list_presets()
        return

    if args.list_models:
        list_models()
        return

    # Generate from preset
    if args.preset:
        generate_from_preset(args.preset, upload=args.upload, model_key=args.model)
        return

    # Generate from custom prompt
    if args.prompt:
        reference_images = []

        # Load reference images from files
        if args.reference:
            for ref_path in args.reference:
                if os.path.exists(ref_path):
                    with open(ref_path, "rb") as f:
                        reference_images.append(f.read())
                    print(f"Loaded reference: {ref_path}")

        # Search for competitor images
        if args.search_competitors:
            urls = search_competitor_images([args.prompt])
            for url in urls:
                img_data = download_image(url)
                if img_data:
                    reference_images.append(img_data)

        # Generate image
        image_data = generate_image_gemini(
            prompt=args.prompt,
            reference_images=reference_images if reference_images else None,
            model_key=args.model
        )

        if image_data:
            output_path = args.output or f"generated_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"\n✅ Saved to: {output_path}")
        return

    # No arguments - show help
    parser.print_help()


if __name__ == "__main__":
    main()
