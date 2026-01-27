#!/usr/bin/env python3
"""
Generate homepage images using Google Gemini/Imagen API and upload to Shopify.
"""

import argparse
import base64
import json
import os
import time
import requests
from google import genai
from google.genai import types


def generate_image_gemini(client, prompt: str, filename: str) -> bytes:
    """Generate an image using Gemini 2.0 Flash with native image generation."""
    print(f"Generating image for: {prompt[:50]}...")

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash-exp",
            contents=f"Generate a high-quality product photography image: {prompt}",
            config=types.GenerateContentConfig(
                response_modalities=["TEXT", "IMAGE"]
            )
        )

        # Extract image from response
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                print(f"Successfully generated: {filename}")
                return base64.b64decode(part.inline_data.data)

        raise Exception("No image in response")

    except Exception as e:
        print(f"Gemini 2.0 failed, trying Imagen 3: {e}")
        return generate_image_imagen(client, prompt, filename)


def generate_image_imagen(client, prompt: str, filename: str) -> bytes:
    """Generate an image using Imagen 3."""
    print(f"Generating with Imagen 3: {prompt[:50]}...")

    response = client.models.generate_images(
        model='imagen-3.0-generate-002',
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
        )
    )

    if response.generated_images:
        print(f"Successfully generated: {filename}")
        return response.generated_images[0].image.image_bytes

    raise Exception("No image generated")


def upload_to_shopify(image_bytes: bytes, filename: str, alt_text: str,
                      store: str, token: str) -> str:
    """Upload image to Shopify Files and return the URL."""
    print(f"Uploading {filename} to Shopify...")

    # First, create a staged upload URL
    graphql_url = f"https://{store}.myshopify.com/admin/api/2024-01/graphql.json"
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    # Stage the upload
    stage_query = """
    mutation stagedUploadsCreate($input: [StagedUploadInput!]!) {
      stagedUploadsCreate(input: $input) {
        stagedTargets {
          url
          resourceUrl
          parameters {
            name
            value
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    stage_variables = {
        "input": [{
            "resource": "FILE",
            "filename": filename,
            "mimeType": "image/png",
            "httpMethod": "POST",
            "fileSize": str(len(image_bytes))
        }]
    }

    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": stage_query, "variables": stage_variables}
    )
    result = response.json()

    if "errors" in result or result.get("data", {}).get("stagedUploadsCreate", {}).get("userErrors"):
        print(f"Stage upload error: {result}")
        raise Exception(f"Failed to stage upload: {result}")

    staged_target = result["data"]["stagedUploadsCreate"]["stagedTargets"][0]
    upload_url = staged_target["url"]
    resource_url = staged_target["resourceUrl"]
    parameters = {p["name"]: p["value"] for p in staged_target["parameters"]}

    # Upload the file
    files = {"file": (filename, image_bytes, "image/png")}
    upload_response = requests.post(upload_url, data=parameters, files=files)

    if upload_response.status_code not in [200, 201, 204]:
        raise Exception(f"Upload failed: {upload_response.status_code}")

    # Create the file in Shopify
    create_query = """
    mutation fileCreate($files: [FileCreateInput!]!) {
      fileCreate(files: $files) {
        files {
          ... on MediaImage {
            id
            image {
              url
            }
          }
        }
        userErrors {
          field
          message
        }
      }
    }
    """

    create_variables = {
        "files": [{
            "alt": alt_text,
            "contentType": "IMAGE",
            "originalSource": resource_url
        }]
    }

    response = requests.post(
        graphql_url,
        headers=headers,
        json={"query": create_query, "variables": create_variables}
    )
    result = response.json()

    # Wait for processing
    time.sleep(3)

    # Get the file URL
    if result.get("data", {}).get("fileCreate", {}).get("files"):
        file_data = result["data"]["fileCreate"]["files"][0]
        if file_data.get("image", {}).get("url"):
            url = file_data["image"]["url"]
            print(f"Uploaded successfully: {url}")
            return url

    print(f"File create result: {result}")
    raise Exception("Failed to get uploaded file URL")


def update_theme_settings(store: str, token: str, image_updates: dict):
    """Update theme settings with new image URLs."""
    print("Updating theme settings...")

    base_url = f"https://{store}.myshopify.com/admin/api/2024-01"
    headers = {
        "X-Shopify-Access-Token": token,
        "Content-Type": "application/json"
    }

    # Get main theme ID
    response = requests.get(f"{base_url}/themes.json", headers=headers)
    themes = response.json().get("themes", [])
    main_theme = next((t for t in themes if t["role"] == "main"), None)

    if not main_theme:
        raise Exception("No main theme found")

    theme_id = main_theme["id"]
    print(f"Found main theme: {theme_id}")

    # Get current settings
    response = requests.get(
        f"{base_url}/themes/{theme_id}/assets.json?asset%5Bkey%5D=config/settings_data.json",
        headers=headers
    )
    settings = json.loads(response.json()["asset"]["value"])

    # Update images in sections
    sections = settings.get("current", {}).get("sections", {})

    # Update hero banner (image-with-text-overlay)
    if "hero" in image_updates:
        for section_id, section in sections.items():
            if section.get("type") == "image-with-text-overlay":
                filename = image_updates["hero"].split("/")[-1].split("?")[0]
                sections[section_id]["settings"]["image"] = f"shopify://shop_images/{filename}"
                print(f"Updated hero banner in section {section_id}")
                break

    # Update featured promotions blocks
    promo_section = None
    for section_id, section in sections.items():
        if section.get("type") == "featured-promotions":
            promo_section = section_id
            break

    if promo_section and sections[promo_section].get("blocks"):
        blocks = sections[promo_section]["blocks"]
        block_ids = list(blocks.keys())

        promo_keys = ["promo1", "promo2", "promo3", "promo4"]
        for i, key in enumerate(promo_keys):
            if key in image_updates and i < len(block_ids):
                filename = image_updates[key].split("/")[-1].split("?")[0]
                blocks[block_ids[i]]["settings"]["image"] = f"shopify://shop_images/{filename}"
                print(f"Updated promo block {block_ids[i]}")

    # Save updated settings
    payload = {
        "asset": {
            "key": "config/settings_data.json",
            "value": json.dumps(settings)
        }
    }

    response = requests.put(
        f"{base_url}/themes/{theme_id}/assets.json",
        headers=headers,
        json=payload
    )

    if response.status_code == 200:
        print("Theme settings updated successfully!")
    else:
        print(f"Failed to update theme: {response.text}")

    # Save results to file for reference
    with open("image_generation_results.json", "w") as f:
        json.dump({
            "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
            "images": image_updates,
            "theme_id": theme_id
        }, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="Generate homepage images")
    parser.add_argument("--hero", required=True, help="Hero banner prompt")
    parser.add_argument("--promo1", required=True, help="Promo 1 prompt")
    parser.add_argument("--promo2", required=True, help="Promo 2 prompt")
    parser.add_argument("--promo3", required=True, help="Promo 3 prompt")
    parser.add_argument("--promo4", required=True, help="Promo 4 prompt")
    args = parser.parse_args()

    # Get credentials from environment
    google_api_key = os.environ.get("GOOGLE_API_KEY")
    shopify_token = os.environ.get("SHOPIFY_ACCESS_TOKEN")
    shopify_store = os.environ.get("SHOPIFY_STORE", "kraftandkitchen")

    # Normalize store name - remove .myshopify.com suffix if present
    shopify_store = shopify_store.replace(".myshopify.com", "").replace("https://", "").replace("http://", "").strip("/")
    print(f"Using Shopify store: {shopify_store}")

    if not google_api_key:
        raise Exception("GOOGLE_API_KEY not set")
    if not shopify_token:
        raise Exception("SHOPIFY_ACCESS_TOKEN not set")

    # Initialize Gemini client
    client = genai.Client(api_key=google_api_key)

    # Generate images
    prompts = {
        "hero": (args.hero, "homepage-hero-banner.png", "Kraft & Kitchen - Quality Kitchen & Craft Supplies"),
        "promo1": (args.promo1, "promo-glass-jars.png", "Premium Glass Jars Collection"),
        "promo2": (args.promo2, "promo-nonstick-paper.png", "Nonstick Paper Products"),
        "promo3": (args.promo3, "promo-fep-sheets.png", "Crystal Clear FEP Sheets"),
        "promo4": (args.promo4, "promo-silicone-pads.png", "Heat Resistant Silicone Pads"),
    }

    image_urls = {}

    for key, (prompt, filename, alt_text) in prompts.items():
        try:
            # Generate image
            image_bytes = generate_image_gemini(client, prompt, filename)

            # Upload to Shopify
            url = upload_to_shopify(
                image_bytes, filename, alt_text,
                shopify_store, shopify_token
            )
            image_urls[key] = url

            # Rate limiting
            time.sleep(2)

        except Exception as e:
            print(f"Error generating {key}: {e}")
            continue

    # Update theme settings
    if image_urls:
        update_theme_settings(shopify_store, shopify_token, image_urls)
    else:
        print("No images were generated successfully")


if __name__ == "__main__":
    main()
