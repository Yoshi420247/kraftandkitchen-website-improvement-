#!/usr/bin/env python3
"""
Kraft & Kitchen Product Image Generator
Uses DALL-E 3 to generate craft product photography

IMPORTANT: Create a .env file with your API key:
OPENAI_API_KEY=your_key_here

DO NOT commit your API key to version control.
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from .env file
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Output directory for generated images
OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

# Image generation prompts based on photography shot list
PRODUCT_PROMPTS = {
    # PTFE Cover Sheets
    "ptfe-hero-on-press": {
        "prompt": """Professional product photography of a beige/tan PTFE Teflon cover sheet laying flat on a heat press platen. The heat press is a modern clamshell style, partially open at a 45-degree angle to show the sheet clearly. The PTFE sheet is smooth, slightly translucent, and extends slightly beyond the platen edges. Clean, bright studio lighting with soft shadows. White/light gray background. Commercial e-commerce product photography style. 16:20 aspect ratio sheet visible. High-end craft supply aesthetic.""",
        "filename": "ptfe-cover-sheet-hero-on-press"
    },

    "ptfe-covering-design": {
        "prompt": """Professional product photography showing hands placing a beige PTFE cover sheet over a colorful heat transfer vinyl design on a dark t-shirt. The design beneath shows through slightly. Heat press visible in background, ready to close. Demonstrates the protective barrier use case. Clean, well-lit craft workspace. Natural hand positioning, realistic use scenario. E-commerce lifestyle photography style.""",
        "filename": "ptfe-cover-sheet-in-use"
    },

    "ptfe-texture-closeup": {
        "prompt": """Macro close-up photography of PTFE-coated fiberglass sheet texture. Shows the fine woven fiberglass pattern beneath the smooth PTFE coating. Beige/tan color with slight sheen. Neutral gray background. Sharp focus on material texture. Professional product detail shot for e-commerce. Clean, minimalist composition.""",
        "filename": "ptfe-texture-closeup"
    },

    "ptfe-cleaning-demo": {
        "prompt": """Product photography showing a hand wiping a PTFE cover sheet with a white microfiber cloth. The sheet is beige/tan, laying on a clean white surface. Some light residue visible being wiped away. Demonstrates easy cleaning and maintenance. Bright, clean lighting. E-commerce instructional photography style.""",
        "filename": "ptfe-cleaning-demo"
    },

    "ptfe-storage-flat": {
        "prompt": """Product photography showing PTFE cover sheets stored flat on a shelf or hanging on a hook. Multiple sheets stacked neatly. Clean, organized craft storage aesthetic. Demonstrates proper flat storage - not folded or rolled. Small text overlay area for 'Store Flat' messaging. Bright, clean e-commerce style.""",
        "filename": "ptfe-storage-flat"
    },

    # Silicone Release Paper - Sticker Use
    "release-paper-sticker-peel": {
        "prompt": """Professional product photography of a colorful decorative sticker being peeled from white silicone release paper. The sticker is lifting cleanly, showing no residue on the paper. Fingers holding the sticker edge naturally. The release paper has a smooth, slightly shiny surface. Bright, cheerful lighting. Clean white background. E-commerce hero shot for sticker storage product. Satisfying peel action visible.""",
        "filename": "release-paper-sticker-peel-hero"
    },

    "release-paper-sticker-book": {
        "prompt": """Product photography of a sticker organization system using silicone release paper in a 3-ring binder. Multiple colorful stickers organized on white release paper pages. The binder is open showing several pages. Demonstrates letter-size (8.5x11) paper with 3-hole punch. Craft room aesthetic. Organized, colorful, appealing to sticker collectors. E-commerce lifestyle photography.""",
        "filename": "release-paper-sticker-book"
    },

    "release-paper-multiple-stickers": {
        "prompt": """Flat lay photography of silicone release paper with various colorful stickers arranged neatly. Mix of sticker sizes and styles - decorative, planner stickers, die cuts. White release paper with slight sheen visible. Clean white background. Demonstrates storage capacity and organization potential. Bright, Pinterest-worthy craft aesthetic.""",
        "filename": "release-paper-sticker-storage-flatlay"
    },

    # Diamond Painting Release Paper
    "diamond-painting-squares-hero": {
        "prompt": """Professional product photography of a diamond painting canvas in progress with white 4x4 inch release paper squares covering unexposed sections. Some diamonds already placed in completed area. The release paper squares protect the adhesive canvas. Clean craft workspace. Shows section-by-section working method. Colorful diamond painting design visible in completed areas. E-commerce hero shot.""",
        "filename": "diamond-painting-squares-hero"
    },

    "diamond-painting-squares-closeup": {
        "prompt": """Close-up product photography showing 4x4 inch white release paper squares positioned on a diamond painting canvas. One square being lifted to reveal the adhesive beneath. Shows the protective function clearly. Some colorful diamonds visible in adjacent completed section. Clean, focused composition. E-commerce detail shot.""",
        "filename": "diamond-painting-squares-detail"
    },

    "diamond-painting-squares-pack": {
        "prompt": """Product photography of a stack of white 4x4 inch silicone release paper squares. Neat stack showing approximately 200 squares. Clean white background. A ruler or hand for scale reference. Some squares fanned out to show quantity. Professional e-commerce pack shot. Clean, commercial aesthetic.""",
        "filename": "diamond-painting-squares-pack"
    },

    # Lifestyle and Collection Images
    "craft-supplies-flatlay": {
        "prompt": """Overhead flat lay photography of craft supplies including PTFE cover sheets, silicone release paper, colorful stickers, heat press supplies, and diamond painting materials. Organized, aesthetically pleasing arrangement. Pastel and bright colors. Clean white marble or light wood surface. Pinterest-worthy craft blogger aesthetic. Professional product photography for collection page header.""",
        "filename": "craft-supplies-lifestyle-flatlay"
    },

    "heat-press-workspace": {
        "prompt": """Lifestyle photography of a clean, organized heat press workspace. Modern clamshell heat press, stack of blank t-shirts, PTFE cover sheets nearby, HTV vinyl rolls visible. Bright, well-lit craft room. Professional but approachable. Small business or serious hobbyist aesthetic. E-commerce collection page header image.""",
        "filename": "heat-press-workspace-lifestyle"
    },

    "sticker-maker-workspace": {
        "prompt": """Lifestyle photography of a sticker maker's workspace. Sticker sheets, cutting machine visible, silicone release paper stacks, organized sticker storage binder. Colorful, creative atmosphere. Clean desk with natural light. Small business crafter aesthetic. E-commerce lifestyle photography for sticker supplies collection.""",
        "filename": "sticker-maker-workspace-lifestyle"
    }
}


def generate_image(prompt_key: str, prompt_data: dict, size: str = "1024x1024", quality: str = "hd") -> dict:
    """
    Generate a single image using DALL-E 3.

    Args:
        prompt_key: Identifier for the prompt
        prompt_data: Dict containing 'prompt' and 'filename'
        size: Image size (1024x1024, 1792x1024, or 1024x1792)
        quality: 'standard' or 'hd' for enhanced detail

    Returns:
        Dict with generation results
    """
    print(f"\n{'='*60}")
    print(f"Generating: {prompt_key}")
    print(f"{'='*60}")

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_data["prompt"],
            size=size,
            quality=quality,  # 'hd' for maximum quality
            n=1
        )

        # Get the image URL and revised prompt
        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt

        # Download the image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prompt_data['filename']}_{timestamp}.png"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(image_response.content)

            print(f"✓ Saved: {filepath}")
            print(f"  Revised prompt: {revised_prompt[:100]}...")

            return {
                "success": True,
                "prompt_key": prompt_key,
                "filepath": str(filepath),
                "revised_prompt": revised_prompt,
                "original_prompt": prompt_data["prompt"]
            }
        else:
            print(f"✗ Failed to download image")
            return {"success": False, "prompt_key": prompt_key, "error": "Download failed"}

    except Exception as e:
        print(f"✗ Error: {str(e)}")
        return {"success": False, "prompt_key": prompt_key, "error": str(e)}


def generate_all_images(quality: str = "hd"):
    """Generate all product images from the prompt list."""

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found in environment variables.")
        print("Create a .env file with: OPENAI_API_KEY=your_key_here")
        return

    print("\n" + "="*60)
    print("KRAFT & KITCHEN PRODUCT IMAGE GENERATOR")
    print("="*60)
    print(f"Output directory: {OUTPUT_DIR.absolute()}")
    print(f"Quality setting: {quality}")
    print(f"Total images to generate: {len(PRODUCT_PROMPTS)}")
    print("="*60)

    results = []

    for prompt_key, prompt_data in PRODUCT_PROMPTS.items():
        result = generate_image(prompt_key, prompt_data, quality=quality)
        results.append(result)

    # Save results log
    log_file = OUTPUT_DIR / f"generation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w') as f:
        json.dump(results, f, indent=2)

    # Print summary
    successful = sum(1 for r in results if r["success"])
    print("\n" + "="*60)
    print("GENERATION COMPLETE")
    print("="*60)
    print(f"Successful: {successful}/{len(results)}")
    print(f"Results log: {log_file}")
    print("="*60)

    return results


def generate_single(prompt_key: str, quality: str = "hd"):
    """Generate a single specific image."""

    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found.")
        return

    if prompt_key not in PRODUCT_PROMPTS:
        print(f"Unknown prompt key: {prompt_key}")
        print(f"Available keys: {list(PRODUCT_PROMPTS.keys())}")
        return

    return generate_image(prompt_key, PRODUCT_PROMPTS[prompt_key], quality=quality)


def list_prompts():
    """List all available prompts."""
    print("\nAvailable image prompts:")
    print("-" * 40)
    for key, data in PRODUCT_PROMPTS.items():
        print(f"  {key}")
        print(f"    -> {data['filename']}")
    print("-" * 40)
    print(f"Total: {len(PRODUCT_PROMPTS)} prompts")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "list":
            list_prompts()
        elif command == "single" and len(sys.argv) > 2:
            generate_single(sys.argv[2])
        elif command == "all":
            generate_all_images()
        else:
            print("Usage:")
            print("  python generate_images.py list          - List all prompts")
            print("  python generate_images.py single <key>  - Generate single image")
            print("  python generate_images.py all           - Generate all images")
    else:
        # Interactive mode
        print("\nKraft & Kitchen Image Generator")
        print("-" * 40)
        print("1. List available prompts")
        print("2. Generate single image")
        print("3. Generate all images")
        print("-" * 40)

        choice = input("Select option (1-3): ").strip()

        if choice == "1":
            list_prompts()
        elif choice == "2":
            list_prompts()
            key = input("\nEnter prompt key: ").strip()
            generate_single(key)
        elif choice == "3":
            confirm = input("Generate all images? This may take a while and cost API credits. (y/n): ")
            if confirm.lower() == 'y':
                generate_all_images()
