#!/usr/bin/env python3
"""
Kraft & Kitchen Product Image Generator v2
Uses DALL-E 3 to generate craft product photography

Based on comprehensive build specification with prompts optimized for:
- Heat Press Nation style (size-first, heavy proof)
- Diamond Art Club style (extreme proof, clean merchandising)
- Etsy sticker book aesthetic (double-sided, letter size, small packs)

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

# Load environment variables
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Output directory
OUTPUT_DIR = Path("generated_images")
OUTPUT_DIR.mkdir(exist_ok=True)

# =============================================================================
# PHOTOGRAPHY PROMPTS - Organized by Category
# =============================================================================

PROMPTS = {
    # =========================================================================
    # HOMEPAGE HERO
    # =========================================================================
    "homepage-hero": {
        "prompt": """Bright, clean craft studio. Overhead 3/4 angle of a tidy workspace with:
- a stack of silicone release paper sheets
- a sticker sheet partially peeled and placed onto release paper
- a cutting machine in the background (generic, no logos)
- a few tools (weeding tool, scraper, tweezers)

Warm off-white or subtle kraft surface. Soft natural window light. Minimal props.
Leave clear negative space on the left for headline text.
High-end e-commerce photography. Professional studio lighting.
Aspect ratio: 16:9 horizontal.""",
        "filename": "kk_homepage_hero",
        "size": "1792x1024"
    },

    # =========================================================================
    # SHOP BY PROJECT TILES (6 tiles, 1:1)
    # =========================================================================
    "tile-stickers": {
        "prompt": """Top-down flat lay on warm off-white or kraft-toned surface.
Center: silicone release paper sheet with 6-8 colorful kiss-cut stickers arranged neatly.
One sticker partially peeled, showing clean release action.
Props: small weeding tool, binder clip.
Bright, high clarity. Professional e-commerce photography.
No text, no logos, no brand names.
Square crop 1:1.""",
        "filename": "kk_tile_stickers_sticker_books",
        "size": "1024x1024"
    },

    "tile-transfers": {
        "prompt": """Top-down flat lay on warm off-white surface.
Center: release paper sheet with a UV DTF transfer design (colorful abstract graphic, no copyrighted imagery).
Props: squeegee, transfer tape roll, pair of scissors.
Bright studio lighting. Professional product photography.
No text, no logos.
Square crop 1:1.""",
        "filename": "kk_tile_transfers_uv_dtf",
        "size": "1024x1024"
    },

    "tile-heat-press": {
        "prompt": """Top-down flat lay on warm off-white surface.
Center: folded beige PTFE cover sheet with a kraft paper belly band.
Props: colorful sublimation print (abstract geometric pattern), heat-resistant glove, small timer.
Bright, high clarity. Professional studio lighting.
No text, no logos.
Square crop 1:1.""",
        "filename": "kk_tile_heat_press_sublimation",
        "size": "1024x1024"
    },

    "tile-diamond-painting": {
        "prompt": """Top-down flat lay on warm off-white surface.
Center: stack of 4x4 white release paper squares fanned out elegantly.
Props: diamond painting tray with colorful sparkly drills (red, blue, green, gold), applicator pen, small section of diamond painting canvas visible.
Bright lighting, jewel-toned accents from the drills catching light.
No text, no logos.
Square crop 1:1.""",
        "filename": "kk_tile_diamond_painting",
        "size": "1024x1024"
    },

    "tile-resin": {
        "prompt": """Top-down flat lay on warm off-white surface.
Center: silicone mat (teal or gray color) with small cured resin pieces in various shapes, one piece mid-peel showing easy release.
Props: small mixing cups, wooden stir sticks, generic resin bottle.
Bright, clean lighting. Professional product photography.
No text, no logos.
Square crop 1:1.""",
        "filename": "kk_tile_resin_glue",
        "size": "1024x1024"
    },

    "tile-work-surfaces": {
        "prompt": """Top-down flat lay on warm off-white surface.
Center: gray silicone mat laid flat with corner slightly folded up to show flexibility and thickness.
Props: craft knife, metal ruler, cutting mat edge visible.
Clean, minimal, professional.
No text, no logos.
Square crop 1:1.""",
        "filename": "kk_tile_work_surfaces",
        "size": "1024x1024"
    },

    # =========================================================================
    # PTFE COVER SHEETS - Full Shot List
    # =========================================================================
    "ptfe-pack-shot": {
        "prompt": """Studio product photo on pure white seamless background.
PTFE cover sheet (beige/tan color) folded neatly with a kraft paper belly band label.
Label shows minimal black typography: "PTFE Cover Sheet" and size marking.
Soft shadow beneath product, high clarity, no harsh reflections.
Professional e-commerce product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_ptfe_pack_shot_white",
        "size": "1024x1024"
    },

    "ptfe-texture-macro": {
        "prompt": """Macro close-up photography of PTFE-coated fiberglass sheet surface.
Shows the fine woven fiberglass texture beneath the PTFE coating.
Beige/tan color with subtle sheen.
Neutral off-white background.
Side lighting at 45 degrees to reveal surface texture and material quality.
Sharp focus on weave pattern, shallow depth of field.
Professional macro product photography.
Aspect ratio: 1:1 square.""",
        "filename": "kk_ptfe_texture_macro",
        "size": "1024x1024"
    },

    "ptfe-in-use-heat-press": {
        "prompt": """Heat press workstation scene - clean, organized, realistic small business setting.
Hands placing beige PTFE cover sheet over a black t-shirt with colorful HTV vinyl design.
The vinyl design is visible beneath the translucent PTFE sheet.
Heat press is modern clamshell style, open at 60 degrees, ready to close.
No visible brand logos on equipment.
Natural lighting mixed with workspace lighting.
Focus on the PTFE sheet edge and precise alignment.
Professional lifestyle product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_ptfe_in_use_heat_press",
        "size": "1024x1024"
    },

    "ptfe-finish-comparison": {
        "prompt": """Before/after comparison diptych showing PTFE cover sheet effect.
Two identical white t-shirts with same colorful HTV design, side by side.

LEFT: Pressed without cover sheet - design shows slight texture, matte finish.
Small subtle label in corner: "Without"

RIGHT: Pressed with PTFE cover sheet - design shows smoother, subtle semi-gloss finish.
Small subtle label in corner: "With PTFE"

Same camera angle, same exposure, same studio lighting for both.
Clean, honest comparison. Professional product photography.
Aspect ratio: 16:9 horizontal.""",
        "filename": "kk_ptfe_finish_comparison",
        "size": "1792x1024"
    },

    "ptfe-cleaning-demo": {
        "prompt": """Close-up product photography showing PTFE sheet care and maintenance.
Hands holding white microfiber cloth, wiping a small area of ink residue off PTFE cover sheet.
Sheet is beige/tan color, laying on clean white surface.
Shows the easy-clean action - residue lifting off cleanly.
Bright, clean workspace lighting.
Professional instructional product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_ptfe_cleaning_demo",
        "size": "1024x1024"
    },

    "ptfe-storage-flat": {
        "prompt": """Product photography showing proper PTFE sheet storage for longevity.
Multiple PTFE cover sheets (beige/tan) stacked flat inside a kraft paper portfolio folder.
OR laying flat between two rigid cardboard sheets.
Shows the "store flat, never fold" best practice.
Minimal scene, tidy craft storage aesthetic.
Professional instructional photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_ptfe_storage_flat",
        "size": "1024x1024"
    },

    # =========================================================================
    # RELEASE PAPER SHEETS - Full Shot List
    # =========================================================================
    "release-pack-shot": {
        "prompt": """Studio product photo on pure white seamless background.
Stack of 50 white silicone release paper sheets in kraft paper envelope or with kraft belly band.
Label visible showing: "Silicone Release Paper" / "8.5 x 11" / "50 Sheets"
Soft shadow beneath, high clarity.
Professional e-commerce product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_release_paper_pack_shot",
        "size": "1024x1024"
    },

    "release-texture-macro": {
        "prompt": """Macro photography of silicone-coated paper surface.
Shallow angle lighting to catch the subtle sheen of silicone coating.
Shows the smooth, almost liquid-like surface quality.
Neutral gray background.
Professional macro product photography.
Aspect ratio: 1:1 square.""",
        "filename": "kk_release_paper_texture_macro",
        "size": "1024x1024"
    },

    "release-sticker-peel-hero": {
        "prompt": """Top-down desk scene - the hero conversion shot for sticker storage.
Warm off-white or kraft surface.
Release paper sheet laying flat with 8-10 colorful kiss-cut stickers (various shapes: hearts, stars, flowers, phrases) placed on it.
One hand holding tweezers, lifting a sticker off the release paper.
The peel action shows clean release - no residue, sticker adhesive intact, satisfying separation.
Props: weeding tool, scraper nearby.
Soft natural daylight from window.
Professional lifestyle product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_release_paper_sticker_peel_hero",
        "size": "1024x1024"
    },

    "release-sticker-book-storage": {
        "prompt": """Sticker book organization system in action.
Open white 3-ring binder on clean light wood desk surface.
Inside: release paper sheets on rings or in page protectors.
Multiple pages visible with colorful stickers organized across them - decorative stickers, planner stickers, washi samples.
Shows the sticker book storage system that Etsy buyers love.
Clean, minimal aesthetic. No logos on binder.
Professional lifestyle photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_release_paper_sticker_book",
        "size": "1024x1024"
    },

    "release-printer-proof": {
        "prompt": """Laser printer compatibility proof shot.
Generic white laser printer, output tray view.
Release paper sheet emerging from printer.
Printed sticker sheet layout visible (simple geometric shapes, circles, squares - no copyrighted imagery).
Shows "laser printer compatible" claim.
Clean office/craft room lighting.
Professional product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_release_paper_printer_proof",
        "size": "1024x1024"
    },

    "release-how-to-graphic": {
        "prompt": """Three-panel instructional graphic showing release paper usage, horizontal layout.

PANEL 1 labeled "1. Place": Hand placing a colorful sticker onto white release paper surface.

PANEL 2 labeled "2. Peel": Hand peeling sticker off - shows clean release action, no residue.

PANEL 3 labeled "3. Store": Sticker storage page inside an open binder.

Minimal style, real photo cutouts on warm off-white background.
Consistent bright lighting across all panels.
Professional instructional graphic.
Aspect ratio: 16:9 horizontal.""",
        "filename": "kk_release_paper_how_to_3step",
        "size": "1792x1024"
    },

    # =========================================================================
    # DIAMOND PAINTING SQUARES - Full Shot List
    # =========================================================================
    "diamond-canvas-sectioning-hero": {
        "prompt": """Diamond painting canvas in progress - the hero shot for diamond painting release paper.
Top-down view of 12x16 inch canvas showing a colorful landscape design (mountains, sunset, trees).
Multiple 4x4 white release paper squares placed in grid pattern covering unexposed sections.
Squares slightly overlap at edges (2-3mm overlap visible).
One section exposed showing adhesive canvas with diamonds partially placed.
Diamond drill tray with colorful sparkly drills (organized by color) at bottom of frame.
Applicator pen visible.
Bright, clean white desk surface.
Soft daylight lighting.
Professional lifestyle product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_diamond_painting_squares_hero",
        "size": "1024x1024"
    },

    "diamond-peel-place-closeup": {
        "prompt": """Close-up shot showing diamond painting workflow.
Hands lifting original plastic cover film from one section of colorful diamond painting canvas.
A 4x4 white release paper square is about to be placed onto the exposed adhesive.
Focus on the edges of the release paper square - clean, precise.
Shows the replacement action - protective cover to release paper.
Shallow depth of field, professional product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_diamond_painting_peel_place",
        "size": "1024x1024"
    },

    "diamond-progress-triptych": {
        "prompt": """Three-panel horizontal image showing diamond painting workflow:

PANEL 1 "Cover": Full canvas view with all sections covered by white 4x4 release paper squares in neat grid. Clean, protected.

PANEL 2 "Work": One section uncovered and exposed. Hand with applicator pen placing colorful diamonds. Drill tray visible.

PANEL 3 "Protect": Same section now re-covered with release paper square. Work paused safely.

Consistent lighting and camera angle across all three panels.
Professional instructional product photography.
Aspect ratio: 16:9 horizontal.""",
        "filename": "kk_diamond_painting_progress_triptych",
        "size": "1792x1024"
    },

    "diamond-pack-quantity": {
        "prompt": """Product quantity shot on pure white background.
Stack of 200 white 4x4 release paper squares.
Stack is neat, edges precisely aligned.
A few squares (5-6) fanned out elegantly to show quantity.
Small metal ruler positioned at edge showing 4 inch measurement.
Simple, clean commercial product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_diamond_painting_squares_pack",
        "size": "1024x1024"
    },

    "diamond-size-reference": {
        "prompt": """Size reference shot for 4x4 release paper square.
Single white 4x4 release paper square held in hand (natural pose).
OR laying on surface with small metal ruler clearly showing exact 4 inch measurement on both sides.
Clean white background.
Shows actual size clearly for customer confidence.
Professional product photography.
Aspect ratio: 1:1 square.""",
        "filename": "kk_diamond_painting_size_reference",
        "size": "1024x1024"
    },

    # =========================================================================
    # SILICONE MATS - Full Shot List
    # =========================================================================
    "mat-flat-product": {
        "prompt": """Silicone mat product shot.
Gray or teal silicone mat (18x24 inches) laying flat on clean white table.
Corner of mat slightly lifted to show flexibility and thickness.
Small metal ruler positioned at edge for scale reference.
Clean, minimal props.
Soft shadow beneath.
Professional e-commerce product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_silicone_mat_product",
        "size": "1024x1024"
    },

    "mat-resin-proof": {
        "prompt": """Silicone mat cleanup proof shot - shows non-stick property.
Close-up action shot of cured resin piece being peeled off silicone mat surface.
Hand pulling up the cured clear resin piece - it releases cleanly with no residue.
Shows the non-stick property that crafters need.
Clean workshop lighting.
Professional product photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_silicone_mat_resin_proof",
        "size": "1024x1024"
    },

    "mat-workspace-setup": {
        "prompt": """Silicone mat in real workspace use.
Gray silicone mat on craft table as work surface.
Resin project in progress on top: silicone molds with colored resin, mixing cups, stir sticks.
OR hot glue gun with hot glue strings on mat.
Shows real use case - protection and easy cleanup promise.
Clean but realistic workshop aesthetic.
Professional lifestyle photography.
Aspect ratio: 4:5 portrait.""",
        "filename": "kk_silicone_mat_workspace",
        "size": "1024x1024"
    },

    # =========================================================================
    # COLLECTION HERO IMAGES (21:9)
    # =========================================================================
    "hero-craft-collection": {
        "prompt": """Wide horizontal hero shot for craft collection page.
Organized craft workspace - aspirational maker studio aesthetic.
Clean white desk surface with craft supplies arranged:
- Stack of white release paper sheets
- Folded beige PTFE cover sheets with kraft belly band
- Gray silicone mat rolled at edge
- Small heat press visible in background (no logos)
- Colorful stickers, scissors, weeding tools

Soft natural lighting from large window on right.
Leave clear negative space on left third for text overlay.
Professional wide-angle lifestyle photography.
Aspect ratio: 21:9 ultra-wide horizontal.""",
        "filename": "kk_hero_craft_collection",
        "size": "1792x1024"
    },

    "hero-heat-press-collection": {
        "prompt": """Wide horizontal hero for heat press collection page.
Heat press workstation - clean, organized, professional but approachable.
Modern clamshell heat press (no visible brand logos).
Stack of blank t-shirts (white, black, gray).
Colorful HTV vinyl rolls stored upright.
PTFE cover sheets nearby, neatly stacked.
Maker/small business aesthetic.
Leave text space on left third.
Soft studio lighting.
Aspect ratio: 21:9 ultra-wide horizontal.""",
        "filename": "kk_hero_heat_press_collection",
        "size": "1792x1024"
    },

    "hero-sticker-collection": {
        "prompt": """Wide horizontal hero for sticker supplies collection page.
Sticker maker's workspace - colorful, creative, but organized.
Cutting machine (generic, no brand logos) on white desk.
Stacked white release paper sheets.
Sticker storage binder open showing colorful organization.
Tools: weeding tools, scraper, scissors, tweezers.
Colorful sticker sheets and vinyl scraps.
Natural light from window.
Leave text space on left third.
Aspect ratio: 21:9 ultra-wide horizontal.""",
        "filename": "kk_hero_sticker_collection",
        "size": "1792x1024"
    },

    "hero-diamond-painting-collection": {
        "prompt": """Wide horizontal hero for diamond painting collection page.
Diamond painting workspace - cozy, focused crafting atmosphere.
Canvas in progress on light pad (glowing softly).
Stack of 4x4 white release paper squares nearby.
Diamond drill trays organized by color (rainbow arrangement).
Applicator pen, wax pad, tweezers arranged neatly.
Warm, inviting lighting.
Leave text space on left third.
Aspect ratio: 21:9 ultra-wide horizontal.""",
        "filename": "kk_hero_diamond_painting_collection",
        "size": "1792x1024"
    },
}


def generate_image(prompt_key: str, prompt_data: dict) -> dict:
    """Generate a single image using DALL-E 3 with HD quality."""

    print(f"\n{'='*60}")
    print(f"Generating: {prompt_key}")
    print(f"{'='*60}")

    size = prompt_data.get("size", "1024x1024")

    try:
        response = client.images.generate(
            model="dall-e-3",
            prompt=prompt_data["prompt"],
            size=size,
            quality="hd",  # Always HD for maximum quality
            n=1
        )

        image_url = response.data[0].url
        revised_prompt = response.data[0].revised_prompt

        # Download image
        image_response = requests.get(image_url)
        if image_response.status_code == 200:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"{prompt_data['filename']}_{timestamp}.png"
            filepath = OUTPUT_DIR / filename

            with open(filepath, 'wb') as f:
                f.write(image_response.content)

            print(f"  Saved: {filepath}")
            print(f"  Size: {size}")
            print(f"  Revised prompt: {revised_prompt[:80]}...")

            return {
                "success": True,
                "prompt_key": prompt_key,
                "filepath": str(filepath),
                "size": size,
                "revised_prompt": revised_prompt
            }
        else:
            print(f"  Failed to download")
            return {"success": False, "prompt_key": prompt_key, "error": "Download failed"}

    except Exception as e:
        print(f"  Error: {str(e)}")
        return {"success": False, "prompt_key": prompt_key, "error": str(e)}


def generate_category(category: str):
    """Generate all images for a specific category."""

    categories = {
        "homepage": ["homepage-hero"],
        "tiles": [k for k in PROMPTS.keys() if k.startswith("tile-")],
        "ptfe": [k for k in PROMPTS.keys() if k.startswith("ptfe-")],
        "release": [k for k in PROMPTS.keys() if k.startswith("release-")],
        "diamond": [k for k in PROMPTS.keys() if k.startswith("diamond-")],
        "mat": [k for k in PROMPTS.keys() if k.startswith("mat-")],
        "hero": [k for k in PROMPTS.keys() if k.startswith("hero-")],
    }

    if category not in categories:
        print(f"Unknown category: {category}")
        print(f"Available: {list(categories.keys())}")
        return

    prompts_to_run = categories[category]
    print(f"\nGenerating {len(prompts_to_run)} images for category: {category}")

    results = []
    for key in prompts_to_run:
        result = generate_image(key, PROMPTS[key])
        results.append(result)

    return results


def generate_all():
    """Generate all images."""
    if not os.getenv("OPENAI_API_KEY"):
        print("ERROR: OPENAI_API_KEY not found")
        return

    print(f"\nGenerating {len(PROMPTS)} total images...")
    print(f"Output: {OUTPUT_DIR.absolute()}")

    results = []
    for key, data in PROMPTS.items():
        result = generate_image(key, data)
        results.append(result)

    # Save log
    log_file = OUTPUT_DIR / f"generation_log_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(log_file, 'w') as f:
        json.dump(results, f, indent=2)

    successful = sum(1 for r in results if r["success"])
    print(f"\n{'='*60}")
    print(f"Complete: {successful}/{len(results)} successful")
    print(f"Log: {log_file}")

    return results


def list_prompts():
    """List all available prompts organized by category."""
    print("\nAvailable prompts:")
    print("-" * 50)

    categories = {}
    for key in PROMPTS.keys():
        cat = key.split("-")[0]
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(key)

    for cat, keys in sorted(categories.items()):
        print(f"\n{cat.upper()} ({len(keys)} prompts):")
        for key in keys:
            print(f"  - {key}")

    print(f"\n{'-'*50}")
    print(f"Total: {len(PROMPTS)} prompts")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        cmd = sys.argv[1]

        if cmd == "list":
            list_prompts()
        elif cmd == "single" and len(sys.argv) > 2:
            key = sys.argv[2]
            if key in PROMPTS:
                generate_image(key, PROMPTS[key])
            else:
                print(f"Unknown prompt: {key}")
        elif cmd == "category" and len(sys.argv) > 2:
            generate_category(sys.argv[2])
        elif cmd == "all":
            confirm = input(f"Generate all {len(PROMPTS)} images? (y/n): ")
            if confirm.lower() == 'y':
                generate_all()
        else:
            print("Usage:")
            print("  python generate_images.py list")
            print("  python generate_images.py single <prompt-key>")
            print("  python generate_images.py category <category>")
            print("  python generate_images.py all")
    else:
        print("\nKraft & Kitchen Image Generator v2")
        print("-" * 40)
        list_prompts()
        print("\nRun with: python generate_images.py <command>")
