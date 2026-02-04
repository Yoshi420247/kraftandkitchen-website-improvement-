#!/usr/bin/env python3
"""
Kraft & Kitchen - Supabase ↔ Shopify Sync Engine

Uses Supabase as the source of truth for all product content,
then syncs to Shopify via Admin API.

Architecture:
    [Supabase DB] → [Sync Engine] → [Shopify Admin API]
                  ↑                 ↓
            [Deployment Log]   [Live Store]

Usage:
    python supabase_sync.py --action <action> [--dry-run]

Actions:
    sync-products    Sync products from Supabase → Shopify
    sync-pages       Sync pages from Supabase → Shopify
    sync-collections Sync collections from Supabase → Shopify
    sync-all         Sync everything
    status           Show sync status dashboard
    check-fixes      Show priority fixes status
    seed-from-files  Load HTML content files into Supabase pages

Requirements:
    pip install requests python-dotenv supabase
"""

import os
import sys
import json
import time
import argparse
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

try:
    from supabase import create_client, Client
except ImportError:
    print("ERROR: supabase package not installed.")
    print("Run: pip install supabase")
    sys.exit(1)

# Load environment
load_dotenv()

# Supabase config
SUPABASE_URL = os.getenv('SUPABASE_URL')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY') or os.getenv('SUPABASE_KEY')

# Shopify config
SHOPIFY_STORE = os.getenv('SHOPIFY_STORE', 'kraftandkitchen')
SHOPIFY_ACCESS_TOKEN = os.getenv('SHOPIFY_ACCESS_TOKEN')
SHOPIFY_API_VERSION = os.getenv('SHOPIFY_API_VERSION', '2024-01')

SHOPIFY_BASE_URL = f"https://{SHOPIFY_STORE}.myshopify.com/admin/api/{SHOPIFY_API_VERSION}"
SHOPIFY_HEADERS = {
    "X-Shopify-Access-Token": SHOPIFY_ACCESS_TOKEN or "",
    "Content-Type": "application/json"
}

PROJECT_ROOT = Path(__file__).parent.parent


class SyncEngine:
    def __init__(self, dry_run=False):
        self.dry_run = dry_run
        self.supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)
        self.stats = {"synced": 0, "failed": 0, "skipped": 0}

    def log(self, msg, level="INFO"):
        prefix = {
            "INFO": "[INFO]", "OK": "[OK]", "ERROR": "[ERR]",
            "DRY": "[DRY]", "WARN": "[WARN]"
        }
        print(f"{prefix.get(level, '[INFO]')} {msg}")

    # =================================================================
    # DEPLOYMENT LOGGING
    # =================================================================
    def log_deployment(self, dtype, handle, action, status,
                       request_payload=None, response_payload=None,
                       error_message=None, shopify_id=None, duration_ms=None):
        """Write to deployment_log in Supabase."""
        try:
            self.supabase.table('deployment_log').insert({
                'deployment_type': dtype,
                'target_handle': handle,
                'target_shopify_id': shopify_id,
                'action': action,
                'status': status,
                'request_payload': request_payload,
                'response_payload': response_payload,
                'error_message': error_message,
                'duration_ms': duration_ms
            }).execute()
        except Exception as e:
            self.log(f"Warning: failed to write deployment log: {e}", "WARN")

    # =================================================================
    # SHOPIFY API
    # =================================================================
    def shopify_request(self, method, endpoint, data=None, max_retries=4):
        """Make Shopify API request with retry and rate limit handling."""
        if self.dry_run:
            self.log(f"Would {method} {endpoint}", "DRY")
            return {"dry_run": True}

        if not SHOPIFY_ACCESS_TOKEN:
            self.log("No SHOPIFY_ACCESS_TOKEN set - skipping Shopify API call", "WARN")
            return None

        url = f"{SHOPIFY_BASE_URL}/{endpoint}"
        start = time.time()

        for attempt in range(max_retries):
            try:
                resp = requests.request(
                    method, url, headers=SHOPIFY_HEADERS, json=data, timeout=30
                )

                if resp.status_code == 429:
                    wait = int(resp.headers.get('Retry-After', 2 ** attempt))
                    self.log(f"Rate limited, waiting {wait}s...", "WARN")
                    time.sleep(wait)
                    continue

                if resp.status_code >= 500:
                    time.sleep(2 ** attempt)
                    continue

                duration = int((time.time() - start) * 1000)

                if resp.status_code >= 400:
                    error = resp.text[:500]
                    self.log(f"Shopify error {resp.status_code}: {error}", "ERROR")
                    return {"error": True, "status": resp.status_code, "body": error, "duration": duration}

                return {**resp.json(), "duration": duration}

            except requests.exceptions.RequestException as e:
                if attempt == max_retries - 1:
                    return {"error": True, "message": str(e)}
                time.sleep(2 ** attempt)

        return {"error": True, "message": "Max retries exceeded"}

    # =================================================================
    # SYNC: PAGES
    # =================================================================
    def sync_pages(self):
        """Sync pages from Supabase to Shopify."""
        self.log("Syncing pages from Supabase → Shopify...")

        # Get pages that need syncing
        result = self.supabase.table('pages').select('*').in_(
            'shopify_sync_status', ['pending', 'dirty', 'failed']
        ).execute()

        pages = result.data
        if not pages:
            self.log("No pages need syncing.", "INFO")
            return

        self.log(f"Found {len(pages)} pages to sync.")

        for page in pages:
            handle = page['handle']
            self.log(f"Syncing page: {handle}")

            # Load body_html from source file if not in DB
            body_html = page.get('body_html')
            if not body_html and page.get('source_file'):
                file_path = PROJECT_ROOT / page['source_file']
                if file_path.exists():
                    body_html = file_path.read_text()
                else:
                    self.log(f"Source file not found: {file_path}", "ERROR")
                    self.stats["failed"] += 1
                    continue

            if not body_html:
                self.log(f"No content for page {handle}", "ERROR")
                self.stats["failed"] += 1
                continue

            page_data = {
                "page": {
                    "title": page['title'],
                    "handle": handle,
                    "body_html": body_html,
                    "published": page.get('published', True)
                }
            }

            # Check if page exists in Shopify
            if page.get('shopify_page_id'):
                # Update existing
                resp = self.shopify_request(
                    "PUT", f"pages/{page['shopify_page_id']}.json", page_data
                )
                action = 'update'
            else:
                # Create new
                resp = self.shopify_request("POST", "pages.json", page_data)
                action = 'create'

            if resp and not resp.get('error') and not resp.get('dry_run'):
                shopify_page = resp.get('page', {})
                shopify_id = shopify_page.get('id')

                # Update Supabase record
                self.supabase.table('pages').update({
                    'shopify_page_id': shopify_id,
                    'shopify_synced_at': datetime.now(timezone.utc).isoformat(),
                    'shopify_sync_status': 'synced',
                    'body_html': body_html
                }).eq('id', page['id']).execute()

                self.log_deployment('page', handle, action, 'success',
                                    shopify_id=shopify_id,
                                    duration_ms=resp.get('duration'))
                self.log(f"Page synced: {handle} (Shopify ID: {shopify_id})", "OK")
                self.stats["synced"] += 1

            elif resp and resp.get('dry_run'):
                self.stats["skipped"] += 1
            else:
                error = resp.get('body', resp.get('message', 'Unknown error')) if resp else 'No response'
                self.supabase.table('pages').update({
                    'shopify_sync_status': 'failed'
                }).eq('id', page['id']).execute()

                self.log_deployment('page', handle, action, 'failed',
                                    error_message=str(error)[:500])
                self.log(f"Failed to sync page: {handle}", "ERROR")
                self.stats["failed"] += 1

    # =================================================================
    # SYNC: COLLECTIONS
    # =================================================================
    def sync_collections(self):
        """Sync collections from Supabase to Shopify."""
        self.log("Syncing collections from Supabase → Shopify...")

        result = self.supabase.table('collections').select('*').in_(
            'shopify_sync_status', ['pending', 'dirty', 'failed']
        ).execute()

        collections = result.data
        if not collections:
            self.log("No collections need syncing.", "INFO")
            return

        self.log(f"Found {len(collections)} collections to sync.")

        for coll in collections:
            handle = coll['handle']
            self.log(f"Syncing collection: {handle}")

            rules = coll.get('rules', [])
            if isinstance(rules, str):
                rules = json.loads(rules)

            coll_data = {
                "smart_collection": {
                    "title": coll['title'],
                    "body_html": coll.get('body_html', ''),
                    "rules": rules,
                    "disjunctive": coll.get('disjunctive', False),
                    "published": coll.get('published', True),
                    "sort_order": coll.get('sort_order', 'best-selling')
                }
            }

            if coll.get('shopify_collection_id'):
                resp = self.shopify_request(
                    "PUT", f"smart_collections/{coll['shopify_collection_id']}.json", coll_data
                )
                action = 'update'
            else:
                resp = self.shopify_request("POST", "smart_collections.json", coll_data)
                action = 'create'

            if resp and not resp.get('error') and not resp.get('dry_run'):
                shopify_coll = resp.get('smart_collection', {})
                shopify_id = shopify_coll.get('id')

                self.supabase.table('collections').update({
                    'shopify_collection_id': shopify_id,
                    'shopify_synced_at': datetime.now(timezone.utc).isoformat(),
                    'shopify_sync_status': 'synced'
                }).eq('id', coll['id']).execute()

                self.log_deployment('collection', handle, action, 'success',
                                    shopify_id=shopify_id)
                self.log(f"Collection synced: {handle}", "OK")
                self.stats["synced"] += 1

            elif resp and resp.get('dry_run'):
                self.stats["skipped"] += 1
            else:
                error = resp.get('body', resp.get('message', 'Unknown')) if resp else 'No response'
                self.supabase.table('collections').update({
                    'shopify_sync_status': 'failed'
                }).eq('id', coll['id']).execute()
                self.log_deployment('collection', handle, action, 'failed',
                                    error_message=str(error)[:500])
                self.stats["failed"] += 1

    # =================================================================
    # SYNC: PRODUCTS
    # =================================================================
    def sync_products(self):
        """Sync products from Supabase to Shopify."""
        self.log("Syncing products from Supabase → Shopify...")

        result = self.supabase.table('products').select('*').in_(
            'shopify_sync_status', ['pending', 'dirty', 'failed']
        ).execute()

        products = result.data
        if not products:
            self.log("No products need syncing.", "INFO")
            return

        self.log(f"Found {len(products)} products to sync.")

        for product in products:
            handle = product['handle']
            self.log(f"Syncing product: {handle}")

            # Get variants
            variants_result = self.supabase.table('product_variants').select('*').eq(
                'product_id', product['id']
            ).execute()

            shopify_variants = []
            for v in variants_result.data:
                sv = {
                    "sku": v.get('sku'),
                    "price": str(v.get('price', '0')),
                    "inventory_management": "shopify",
                    "inventory_policy": v.get('inventory_policy', 'continue'),
                    "requires_shipping": v.get('requires_shipping', True),
                    "taxable": v.get('taxable', True),
                }
                if v.get('option1_name'):
                    sv["option1"] = v.get('option1_value')
                if v.get('compare_at_price'):
                    sv["compare_at_price"] = str(v['compare_at_price'])
                if v.get('shopify_variant_id'):
                    sv["id"] = v['shopify_variant_id']
                shopify_variants.append(sv)

            product_data = {
                "product": {
                    "title": product['title'],
                    "body_html": product.get('body_html', ''),
                    "vendor": product.get('vendor', 'Kraft & Kitchen'),
                    "product_type": product.get('product_type', ''),
                    "tags": ', '.join(product.get('tags', [])),
                    "published": product.get('published', True),
                }
            }

            if shopify_variants:
                product_data["product"]["variants"] = shopify_variants

            if product.get('shopify_product_id'):
                product_data["product"]["id"] = product['shopify_product_id']
                resp = self.shopify_request(
                    "PUT", f"products/{product['shopify_product_id']}.json", product_data
                )
                action = 'update'
            else:
                resp = self.shopify_request("POST", "products.json", product_data)
                action = 'create'

            if resp and not resp.get('error') and not resp.get('dry_run'):
                shopify_prod = resp.get('product', {})
                shopify_id = shopify_prod.get('id')

                self.supabase.table('products').update({
                    'shopify_product_id': shopify_id,
                    'shopify_synced_at': datetime.now(timezone.utc).isoformat(),
                    'shopify_sync_status': 'synced'
                }).eq('id', product['id']).execute()

                self.log_deployment('product', handle, action, 'success',
                                    shopify_id=shopify_id)
                self.log(f"Product synced: {handle}", "OK")
                self.stats["synced"] += 1

            elif resp and resp.get('dry_run'):
                self.stats["skipped"] += 1
            else:
                error = resp.get('body', resp.get('message', 'Unknown')) if resp else 'No response'
                self.supabase.table('products').update({
                    'shopify_sync_status': 'failed'
                }).eq('id', product['id']).execute()
                self.log_deployment('product', handle, action, 'failed',
                                    error_message=str(error)[:500])
                self.stats["failed"] += 1

    # =================================================================
    # SEED: Load file content into Supabase
    # =================================================================
    def seed_page_content(self):
        """Load HTML content from source files into Supabase page records."""
        self.log("Loading page content from source files into Supabase...")

        result = self.supabase.table('pages').select('*').execute()
        pages = result.data

        updated = 0
        for page in pages:
            source_file = page.get('source_file')
            if not source_file:
                continue

            file_path = PROJECT_ROOT / source_file
            if not file_path.exists():
                self.log(f"File not found: {file_path}", "WARN")
                continue

            body_html = file_path.read_text()
            if not body_html.strip():
                continue

            self.supabase.table('pages').update({
                'body_html': body_html,
                'shopify_sync_status': 'pending'
            }).eq('id', page['id']).execute()

            self.log(f"Loaded content for: {page['handle']}", "OK")
            updated += 1

        self.log(f"Updated {updated} pages with file content.", "INFO")

    # =================================================================
    # STATUS DASHBOARD
    # =================================================================
    def show_status(self):
        """Display sync status dashboard."""
        print("\n" + "=" * 60)
        print("  KRAFT & KITCHEN - SYNC STATUS DASHBOARD")
        print("=" * 60)

        # Products
        products = self.supabase.table('products').select('shopify_sync_status').execute().data
        prod_status = {}
        for p in products:
            s = p['shopify_sync_status']
            prod_status[s] = prod_status.get(s, 0) + 1

        print(f"\n  PRODUCTS ({len(products)} total)")
        for status, count in sorted(prod_status.items()):
            icon = {"synced": "+", "pending": "~", "failed": "!", "dirty": "*"}.get(status, "?")
            print(f"    [{icon}] {status}: {count}")

        # Pages
        pages = self.supabase.table('pages').select('shopify_sync_status').execute().data
        page_status = {}
        for p in pages:
            s = p['shopify_sync_status']
            page_status[s] = page_status.get(s, 0) + 1

        print(f"\n  PAGES ({len(pages)} total)")
        for status, count in sorted(page_status.items()):
            icon = {"synced": "+", "pending": "~", "failed": "!", "dirty": "*"}.get(status, "?")
            print(f"    [{icon}] {status}: {count}")

        # Collections
        colls = self.supabase.table('collections').select('shopify_sync_status').execute().data
        coll_status = {}
        for c in colls:
            s = c['shopify_sync_status']
            coll_status[s] = coll_status.get(s, 0) + 1

        print(f"\n  COLLECTIONS ({len(colls)} total)")
        for status, count in sorted(coll_status.items()):
            icon = {"synced": "+", "pending": "~", "failed": "!", "dirty": "*"}.get(status, "?")
            print(f"    [{icon}] {status}: {count}")

        # Reviews
        reviews = self.supabase.table('reviews').select('approved, featured').execute().data
        approved = sum(1 for r in reviews if r.get('approved'))
        featured = sum(1 for r in reviews if r.get('featured'))
        print(f"\n  REVIEWS ({len(reviews)} total)")
        print(f"    Approved: {approved}")
        print(f"    Featured: {featured}")

        # Recent deployments
        deploys = self.supabase.table('deployment_log').select('*').order(
            'created_at', desc=True
        ).limit(5).execute().data

        if deploys:
            print(f"\n  RECENT DEPLOYMENTS")
            for d in deploys:
                icon = {"success": "+", "failed": "!", "started": "~"}.get(d['status'], "?")
                ts = d['created_at'][:19]
                print(f"    [{icon}] {ts} {d['deployment_type']}: {d['target_handle']} → {d['status']}")

        print("\n" + "=" * 60)

    def show_fixes(self):
        """Show priority fixes status."""
        print("\n" + "=" * 60)
        print("  PRIORITY FIXES STATUS")
        print("=" * 60)

        fixes = self.supabase.table('priority_fixes').select('*').order(
            'severity'
        ).execute().data

        for fix in fixes:
            severity_icon = {
                "critical": "!!!",
                "high": "!! ",
                "medium": "!  ",
                "low": ".  "
            }.get(fix['severity'], "?  ")

            status_icon = {
                "open": "[ ]",
                "in_progress": "[~]",
                "completed": "[x]",
                "verified": "[+]"
            }.get(fix['status'], "[?]")

            manual = " (MANUAL)" if fix.get('manual_action_required') else ""
            print(f"\n  {status_icon} {severity_icon} {fix['fix_id']}: {fix['title']}{manual}")
            if fix.get('instructions') and fix['status'] == 'open':
                for line in fix['instructions'].split('\n'):
                    print(f"        {line}")

        print("\n" + "=" * 60)

    # =================================================================
    # MAIN
    # =================================================================
    def sync_all(self):
        """Sync everything."""
        self.sync_pages()
        self.sync_collections()
        self.sync_products()

    def print_stats(self):
        """Print final stats."""
        print(f"\n  Synced: {self.stats['synced']} | "
              f"Failed: {self.stats['failed']} | "
              f"Skipped: {self.stats['skipped']}")


def main():
    parser = argparse.ArgumentParser(description="Supabase ↔ Shopify Sync Engine")
    parser.add_argument('--action', required=True,
                        choices=['sync-products', 'sync-pages', 'sync-collections',
                                 'sync-all', 'status', 'check-fixes', 'seed-from-files'])
    parser.add_argument('--dry-run', action='store_true')
    args = parser.parse_args()

    # Validate Supabase credentials
    if not SUPABASE_URL or not SUPABASE_KEY:
        print("ERROR: Supabase credentials not set!")
        print("\nAdd to scripts/.env:")
        print("  SUPABASE_URL=https://YOUR_PROJECT.supabase.co")
        print("  SUPABASE_KEY=your-service-role-key")
        print("\nFind these in: Supabase Dashboard > Settings > API")
        sys.exit(1)

    engine = SyncEngine(dry_run=args.dry_run)

    if args.dry_run:
        engine.log("DRY RUN MODE", "DRY")

    action_map = {
        'sync-products': engine.sync_products,
        'sync-pages': engine.sync_pages,
        'sync-collections': engine.sync_collections,
        'sync-all': engine.sync_all,
        'status': engine.show_status,
        'check-fixes': engine.show_fixes,
        'seed-from-files': engine.seed_page_content,
    }

    action_map[args.action]()

    if args.action.startswith('sync'):
        engine.print_stats()


if __name__ == "__main__":
    main()
