#!/usr/bin/env python3
"""
Kraft & Kitchen Shopify Deployment Script

This script deploys improvements to the live Shopify store including:
- Creating/updating pages (SEO content, landing pages)
- Updating product descriptions
- Fixing policies (privacy, shipping)
- Creating collections

Usage:
    python deploy_to_shopify.py --action <action> [--dry-run]

Actions:
    all              - Deploy all improvements
    pages            - Deploy SEO and landing pages
    products         - Update product descriptions
    policies         - Fix privacy and shipping policies
    collections      - Create craft-focused collections
    priority-fixes   - Deploy critical conversion fixes only

Requirements:
    pip install requests python-dotenv
"""

import os
import sys
import json
import time
import argparse
import requests
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
SHOPIFY_STORE = os.getenv('SHOPIFY_STORE', 'kraftandkitchen')
SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-01')

BASE_URL = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}"
HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN,
    "Content-Type": "application/json"
}

# Project paths
PROJECT_ROOT = Path(__file__).parent.parent
PAGES_DIR = PROJECT_ROOT / "pages"
PRODUCTS_DIR = PROJECT_ROOT / "products"
SEO_CONTENT_DIR = PAGES_DIR / "seo-content"


class ShopifyDeployer:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.results = {"success": [], "failed": [], "skipped": []}

    def log(self, message, level="INFO"):
        prefix = {"INFO": "[INFO]", "SUCCESS": "[OK]", "ERROR": "[ERROR]", "DRY": "[DRY-RUN]"}
        print(f"{prefix.get(level, '[INFO]')} {message}")

    def api_request(self, method, endpoint, data=None, max_retries=4):
        """Make API request with retry logic for rate limiting."""
        if self.dry_run:
            self.log(f"Would {method} {endpoint}", "DRY")
            if data:
                self.log(f"Data: {json.dumps(data, indent=2)[:500]}...", "DRY")
            return {"dry_run": True}

        url = f"{BASE_URL}/{endpoint}"

        for attempt in range(max_retries):
            try:
                response = requests.request(
                    method, url, headers=HEADERS, json=data, timeout=30
                )

                if response.status_code == 429:
                    retry_after = int(response.headers.get('Retry-After', 2 ** attempt))
                    self.log(f"Rate limited. Waiting {retry_after}s...", "INFO")
                    time.sleep(retry_after)
                    continue

                if response.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue

                response.raise_for_status()
                return response.json()

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)

        raise Exception(f"Max retries exceeded for {endpoint}")

    def graphql_request(self, query, variables=None):
        """Make GraphQL API request."""
        if self.dry_run:
            self.log(f"Would execute GraphQL query", "DRY")
            return {"dry_run": True}

        url = f"{BASE_URL}/graphql.json"
        payload = {"query": query}
        if variables:
            payload["variables"] = variables

        response = requests.post(url, headers=HEADERS, json=payload, timeout=30)
        response.raise_for_status()
        return response.json()

    # =========================================================================
    # PAGE MANAGEMENT
    # =========================================================================

    def get_existing_pages(self):
        """Get all existing pages from store."""
        try:
            result = self.api_request("GET", "pages.json?limit=250")
            return {p['handle']: p for p in result.get('pages', [])}
        except Exception as e:
            self.log(f"Error fetching pages: {e}", "ERROR")
            return {}

    def create_or_update_page(self, title, handle, body_html, published=True):
        """Create or update a page."""
        existing_pages = self.get_existing_pages()

        page_data = {
            "page": {
                "title": title,
                "handle": handle,
                "body_html": body_html,
                "published": published
            }
        }

        try:
            if handle in existing_pages:
                page_id = existing_pages[handle]['id']
                page_data["page"]["id"] = page_id
                self.api_request("PUT", f"pages/{page_id}.json", page_data)
                self.log(f"Updated page: {title}", "SUCCESS")
            else:
                self.api_request("POST", "pages.json", page_data)
                self.log(f"Created page: {title}", "SUCCESS")

            self.results["success"].append(f"Page: {handle}")
            return True

        except Exception as e:
            self.log(f"Error with page {handle}: {e}", "ERROR")
            self.results["failed"].append(f"Page: {handle} - {e}")
            return False

    def deploy_seo_pages(self):
        """Deploy all SEO content pages."""
        self.log("Deploying SEO content pages...")

        seo_pages = [
            {
                "file": "release-paper-for-stickers.html",
                "title": "Release Paper for Stickers - Storage & Organization Guide",
                "handle": "release-paper-for-stickers"
            },
            {
                "file": "diamond-painting-release-paper.html",
                "title": "Diamond Painting Release Paper - Protect Your Canvas",
                "handle": "diamond-painting-release-paper"
            },
            {
                "file": "diamond-painting-dust-protection.html",
                "title": "Diamond Painting Dust Protection Tips",
                "handle": "diamond-painting-dust-protection"
            },
            {
                "file": "ptfe-sheet-for-heat-press.html",
                "title": "PTFE Sheet for Heat Press - Complete Guide",
                "handle": "ptfe-sheet-for-heat-press"
            },
            {
                "file": "release-paper-vs-parchment.html",
                "title": "Release Paper vs Parchment Paper - What's the Difference?",
                "handle": "release-paper-vs-parchment"
            }
        ]

        for page in seo_pages:
            file_path = SEO_CONTENT_DIR / page["file"]
            if file_path.exists():
                body_html = file_path.read_text()
                self.create_or_update_page(page["title"], page["handle"], body_html)
            else:
                self.log(f"File not found: {file_path}", "ERROR")
                self.results["skipped"].append(f"Page: {page['handle']} (file missing)")

    def deploy_landing_pages(self):
        """Deploy landing pages."""
        self.log("Deploying landing pages...")

        landing_pages = [
            {
                "file": "craft-hub-landing-page.html",
                "title": "Craft Supplies - Release Paper, PTFE Sheets & More",
                "handle": "craft-supplies"
            }
        ]

        for page in landing_pages:
            file_path = PAGES_DIR / page["file"]
            if file_path.exists():
                body_html = file_path.read_text()
                self.create_or_update_page(page["title"], page["handle"], body_html)
            else:
                self.log(f"File not found: {file_path}", "ERROR")

    # =========================================================================
    # POLICY FIXES
    # =========================================================================

    def fix_privacy_policy(self):
        """Fix privacy policy placeholders."""
        self.log("Fixing privacy policy...")

        # Get current privacy policy
        try:
            result = self.api_request("GET", "policies.json")
            policies = result.get('policies', [])

            privacy_policy = None
            for policy in policies:
                if policy.get('handle') == 'privacy-policy':
                    privacy_policy = policy
                    break

            if not privacy_policy:
                self.log("Privacy policy not found via API. Update manually in Shopify Admin.", "ERROR")
                return False

            body = privacy_policy.get('body', '')

            # Replace common placeholders
            replacements = {
                '[[INSERT DESCRIPTIONS OF TYPES OF TRACKING TECHNOLOGIES USED]]':
                    'cookies, web beacons, and local storage for analytics and site functionality',
                '[[INSERT OTHER COVERAGE COVERAGE AS NECESSARY]]':
                    'Shop Pay, credit/debit cards (Visa, Mastercard, American Express, Discover), and PayPal',
                '[[INSERT CONTACT INFORMATION]]':
                    'support@kraftandkitchen.com',
                '[[INSERT...]':
                    '',
                '[[': '',
                ']]': ''
            }

            updated_body = body
            for placeholder, replacement in replacements.items():
                updated_body = updated_body.replace(placeholder, replacement)

            if updated_body != body:
                self.log("Privacy policy has placeholders that need manual review.", "INFO")
                self.log("Go to Shopify Admin > Settings > Policies > Privacy policy", "INFO")
                self.results["skipped"].append("Privacy policy - needs manual review")
            else:
                self.log("Privacy policy appears clean", "SUCCESS")

            return True

        except Exception as e:
            self.log(f"Error checking privacy policy: {e}", "ERROR")
            self.log("Update privacy policy manually in Shopify Admin > Settings > Policies", "INFO")
            return False

    # =========================================================================
    # COLLECTION MANAGEMENT
    # =========================================================================

    def create_craft_collections(self):
        """Create craft-focused collections."""
        self.log("Creating craft collections...")

        collections = [
            {
                "title": "Heat Press + Sublimation",
                "handle": "heat-press-sublimation",
                "body_html": "<p>PTFE cover sheets and accessories for heat press, sublimation, and DTF transfers.</p>",
                "rules": [
                    {"column": "tag", "relation": "equals", "condition": "heat-press"},
                    {"column": "tag", "relation": "equals", "condition": "sublimation"}
                ],
                "disjunctive": True
            },
            {
                "title": "Stickers + Decals",
                "handle": "stickers-decals",
                "body_html": "<p>Silicone release paper for sticker storage, sticker books, and transfer backing.</p>",
                "rules": [
                    {"column": "tag", "relation": "equals", "condition": "stickers"},
                    {"column": "tag", "relation": "equals", "condition": "release-paper"}
                ],
                "disjunctive": True
            },
            {
                "title": "Diamond Painting",
                "handle": "diamond-painting",
                "body_html": "<p>Release paper squares and sheets to protect your diamond painting canvas adhesive.</p>",
                "rules": [
                    {"column": "tag", "relation": "equals", "condition": "diamond-painting"}
                ],
                "disjunctive": False
            },
            {
                "title": "Craft Best Sellers",
                "handle": "craft-best-sellers",
                "body_html": "<p>Our most popular craft supplies, chosen by makers like you.</p>",
                "rules": [
                    {"column": "tag", "relation": "equals", "condition": "best-seller"},
                    {"column": "tag", "relation": "equals", "condition": "craft"}
                ],
                "disjunctive": False
            }
        ]

        # Get existing collections
        try:
            result = self.api_request("GET", "smart_collections.json?limit=250")
            existing = {c['handle']: c for c in result.get('smart_collections', [])}
        except Exception:
            existing = {}

        for coll in collections:
            try:
                coll_data = {
                    "smart_collection": {
                        "title": coll["title"],
                        "body_html": coll["body_html"],
                        "rules": coll["rules"],
                        "disjunctive": coll["disjunctive"],
                        "published": True,
                        "sort_order": "best-selling"
                    }
                }

                if coll["handle"] in existing:
                    coll_id = existing[coll["handle"]]["id"]
                    coll_data["smart_collection"]["id"] = coll_id
                    self.api_request("PUT", f"smart_collections/{coll_id}.json", coll_data)
                    self.log(f"Updated collection: {coll['title']}", "SUCCESS")
                else:
                    self.api_request("POST", "smart_collections.json", coll_data)
                    self.log(f"Created collection: {coll['title']}", "SUCCESS")

                self.results["success"].append(f"Collection: {coll['handle']}")

            except Exception as e:
                self.log(f"Error with collection {coll['handle']}: {e}", "ERROR")
                self.results["failed"].append(f"Collection: {coll['handle']} - {e}")

    # =========================================================================
    # PRODUCT UPDATES
    # =========================================================================

    def get_products_by_handle(self, handles):
        """Get products by their handles."""
        products = {}
        for handle in handles:
            try:
                result = self.api_request("GET", f"products.json?handle={handle}")
                if result.get('products'):
                    products[handle] = result['products'][0]
            except Exception as e:
                self.log(f"Error fetching product {handle}: {e}", "ERROR")
        return products

    def update_product_description(self, product_id, body_html, title=None, tags=None):
        """Update a product's description and optionally title/tags."""
        data = {
            "product": {
                "id": product_id,
                "body_html": body_html
            }
        }
        if title:
            data["product"]["title"] = title
        if tags:
            data["product"]["tags"] = tags

        try:
            self.api_request("PUT", f"products/{product_id}.json", data)
            return True
        except Exception as e:
            self.log(f"Error updating product {product_id}: {e}", "ERROR")
            return False

    def deploy_product_updates(self):
        """Update product descriptions from HTML files."""
        self.log("Updating product descriptions...")

        product_updates = [
            {
                "handle": "silicone-release-paper-for-rosin-and-storage",
                "file": "release-paper-bulk-legal-size.html",
                "new_title": "Slick Silicone Release Paper Sheets (8.5\" x 14\" Legal)",
                "tags": "release-paper, craft, stickers, diamond-painting, baking, best-seller"
            }
        ]

        for update in product_updates:
            file_path = PRODUCTS_DIR / update["file"]
            if not file_path.exists():
                self.log(f"Product file not found: {file_path}", "ERROR")
                continue

            products = self.get_products_by_handle([update["handle"]])
            if update["handle"] not in products:
                self.log(f"Product not found in store: {update['handle']}", "ERROR")
                continue

            product = products[update["handle"]]
            body_html = file_path.read_text()

            success = self.update_product_description(
                product["id"],
                body_html,
                title=update.get("new_title"),
                tags=update.get("tags")
            )

            if success:
                self.log(f"Updated product: {update['handle']}", "SUCCESS")
                self.results["success"].append(f"Product: {update['handle']}")
            else:
                self.results["failed"].append(f"Product: {update['handle']}")

    # =========================================================================
    # PRIORITY FIXES (Critical conversion issues)
    # =========================================================================

    def deploy_priority_fixes(self):
        """Deploy critical fixes that are actively costing sales."""
        self.log("=" * 60)
        self.log("DEPLOYING PRIORITY FIXES (Conversion Critical)")
        self.log("=" * 60)

        # Fix 1: Instructions for recurring purchase warning
        self.log("\n[FIX 1] Recurring Purchase Warning")
        self.log("-" * 40)
        self.log("This requires manual action in Shopify Admin:")
        self.log("1. Go to Products > [Release Paper Product]")
        self.log("2. Scroll to 'Purchase options'")
        self.log("3. If selling plans exist, remove them OR")
        self.log("4. Check Apps > find subscription app > disable for this product")
        self.results["skipped"].append("Recurring purchase warning - needs manual action")

        # Fix 2: Related items cross-sell
        self.log("\n[FIX 2] High-Price B2B Items in Related Products")
        self.log("-" * 40)
        self.log("This requires theme customization:")
        self.log("1. Go to Online Store > Themes > Customize")
        self.log("2. Navigate to Product pages")
        self.log("3. Edit Related Products section")
        self.log("4. Exclude products tagged 'b2b' or 'custom-printing'")
        self.log("5. Or set up a 'retail-cross-sell' collection")
        self.results["skipped"].append("Related items - needs theme customization")

        # Fix 3: Privacy policy
        self.log("\n[FIX 3] Privacy Policy Placeholders")
        self.log("-" * 40)
        self.fix_privacy_policy()

        # Fix 4: Shipping origin consistency
        self.log("\n[FIX 4] Shipping Origin / Phone Number Consistency")
        self.log("-" * 40)
        self.log("Review and update in Shopify Admin:")
        self.log("1. Settings > Policies > Shipping policy")
        self.log("2. Settings > Store details (for contact info)")
        self.log("3. Online Store > Themes > Customize > Footer")
        self.log("Ensure consistent: Bellingham, WA as shipping origin")
        self.results["skipped"].append("Shipping/phone consistency - needs manual review")

        self.log("\n" + "=" * 60)
        self.log("Priority fixes summary logged. See manual actions above.")
        self.log("=" * 60)

    # =========================================================================
    # MAIN DEPLOYMENT ACTIONS
    # =========================================================================

    def deploy_all(self):
        """Deploy all improvements."""
        self.log("=" * 60)
        self.log("FULL DEPLOYMENT - Kraft & Kitchen Improvements")
        self.log("=" * 60)

        self.deploy_priority_fixes()
        self.deploy_landing_pages()
        self.deploy_seo_pages()
        self.create_craft_collections()
        self.deploy_product_updates()

        self.print_summary()

    def deploy_pages_only(self):
        """Deploy only pages."""
        self.deploy_landing_pages()
        self.deploy_seo_pages()
        self.print_summary()

    def print_summary(self):
        """Print deployment summary."""
        self.log("\n" + "=" * 60)
        self.log("DEPLOYMENT SUMMARY")
        self.log("=" * 60)

        self.log(f"\nSuccessful: {len(self.results['success'])}")
        for item in self.results['success']:
            self.log(f"  - {item}", "SUCCESS")

        if self.results['failed']:
            self.log(f"\nFailed: {len(self.results['failed'])}")
            for item in self.results['failed']:
                self.log(f"  - {item}", "ERROR")

        if self.results['skipped']:
            self.log(f"\nSkipped/Manual: {len(self.results['skipped'])}")
            for item in self.results['skipped']:
                self.log(f"  - {item}", "INFO")


def main():
    parser = argparse.ArgumentParser(description="Deploy Kraft & Kitchen improvements to Shopify")
    parser.add_argument('--action', choices=['all', 'pages', 'products', 'policies', 'collections', 'priority-fixes'],
                        default='all', help='Deployment action to perform')
    parser.add_argument('--dry-run', action='store_true', help='Show what would be done without making changes')

    args = parser.parse_args()

    # Validate credentials
    if not SHOPIFY_ACCESS_TOKEN:
        print("ERROR: SHOPIFY_ACCESS_TOKEN not set!")
        print("\nTo configure:")
        print("1. Copy scripts/.env.example to scripts/.env")
        print("2. Add your Shopify Admin API access token")
        print("3. Run this script again")
        print("\nTo get an access token:")
        print("1. Go to Shopify Admin > Settings > Apps > Develop apps")
        print("2. Create an app with scopes: write_products, write_themes, write_content")
        print("3. Install the app and copy the Admin API access token")
        sys.exit(1)

    deployer = ShopifyDeployer(dry_run=args.dry_run)

    if args.dry_run:
        deployer.log("DRY RUN MODE - No changes will be made", "DRY")

    if args.action == 'all':
        deployer.deploy_all()
    elif args.action == 'pages':
        deployer.deploy_pages_only()
    elif args.action == 'products':
        deployer.deploy_product_updates()
    elif args.action == 'policies':
        deployer.fix_privacy_policy()
    elif args.action == 'collections':
        deployer.create_craft_collections()
    elif args.action == 'priority-fixes':
        deployer.deploy_priority_fixes()


if __name__ == "__main__":
    main()
