-- Kraft & Kitchen Supabase Seed Data
-- Run after 001_initial_schema.sql
-- Seeds products, metafields, differentiators, pages, collections, and priority fixes

-- ============================================================
-- PRODUCTS
-- ============================================================
INSERT INTO products (handle, title, body_html, product_type, tags) VALUES
('ptfe-cover-sheet-16x20',
 'PTFE Heat Press Cover Sheet 16x20',
 '<p>A reusable nonstick sheet that protects your heat press platen from vinyl residue and ink transfer. Essential for HTV, sublimation, DTF, and screen print curing.</p>',
 'Cover Sheets',
 ARRAY['heat-press', 'sublimation', 'htv', 'dtf', 'bestseller']),

('ptfe-cover-sheet-18x20',
 'PTFE Heat Press Cover Sheet 18x20',
 '<p>Larger size cover sheet for commercial heat presses. Same quality PTFE-coated fiberglass for edge-to-edge protection.</p>',
 'Cover Sheets',
 ARRAY['heat-press', 'sublimation', 'htv', 'dtf', 'commercial']),

('ptfe-cover-sheet-12x15',
 'PTFE Heat Press Cover Sheet 12x15',
 '<p>Compact cover sheet for mini and craft heat presses. Perfect size for smaller pressing projects.</p>',
 'Cover Sheets',
 ARRAY['heat-press', 'sublimation', 'htv', 'craft']),

('silicone-release-paper-letter-25',
 'Silicone Release Paper 8.5x11 - 25 Pack',
 '<p>Double-sided nonstick paper for sticker storage and sticker books. Stickers peel clean from both sides without losing adhesive.</p>',
 'Release Paper',
 ARRAY['stickers', 'sticker-book', 'transfers']),

('silicone-release-paper-letter-50',
 'Silicone Release Paper 8.5x11 - 50 Pack',
 '<p>Double-sided nonstick paper for sticker storage and sticker books. Stickers peel clean from both sides without losing adhesive.</p>',
 'Release Paper',
 ARRAY['stickers', 'sticker-book', 'transfers', 'bestseller']),

('silicone-release-paper-letter-100',
 'Silicone Release Paper 8.5x11 - 100 Pack',
 '<p>Double-sided nonstick paper for sticker storage and sticker books. Bulk pack for serious collectors and small businesses.</p>',
 'Release Paper',
 ARRAY['stickers', 'sticker-book', 'transfers', 'bulk']),

('silicone-release-paper-legal-100',
 'Silicone Release Paper 8.5x14 - 100 Pack',
 '<p>Legal size release paper for larger transfers and extended sticker storage. Double-sided silicone coating.</p>',
 'Release Paper',
 ARRAY['transfers', 'stickers', 'legal-size']),

('diamond-painting-squares-100',
 'Diamond Painting Release Paper Squares 4x4 - 100 Pack',
 '<p>Pre-cut squares that protect your diamond painting adhesive while you work section by section. Double-sided silicone coating.</p>',
 'Diamond Painting',
 ARRAY['diamond-painting', 'release-paper']),

('diamond-painting-squares-200',
 'Diamond Painting Release Paper Squares 4x4 - 200 Pack',
 '<p>Pre-cut squares that protect your diamond painting adhesive while you work section by section. Best value for multiple projects.</p>',
 'Diamond Painting',
 ARRAY['diamond-painting', 'release-paper', 'bestseller']),

('silicone-mat-small',
 'Silicone Work Mat - Small',
 '<p>Reusable silicone mat for resin, glue, and messy crafts. Cured materials peel right off. Heat resistant work surface protection.</p>',
 'Work Mats',
 ARRAY['resin', 'glue', 'craft-mat']),

('silicone-mat-medium',
 'Silicone Work Mat - Medium',
 '<p>Medium size silicone mat for craft table sections. Perfect for resin pours, glue projects, and messy crafts.</p>',
 'Work Mats',
 ARRAY['resin', 'glue', 'craft-mat', 'bestseller']),

('silicone-mat-large',
 'Silicone Work Mat - Large',
 '<p>Full table coverage silicone mat for large projects and production work. Maximum workspace protection.</p>',
 'Work Mats',
 ARRAY['resin', 'glue', 'craft-mat', 'commercial']),

('ptfe-roll-16x50',
 'PTFE Roll 16" x 50''',
 '<p>Cut-to-size PTFE roll for shops and high-volume users. Same material as our cover sheets at bulk pricing.</p>',
 'Bulk Rolls',
 ARRAY['heat-press', 'bulk', 'commercial']);

-- ============================================================
-- PRODUCT VARIANTS
-- ============================================================
INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-PTFE-16x20-1', 'Single', 'Pack Size', 'Single', 8.99, 500
FROM products WHERE handle = 'ptfe-cover-sheet-16x20';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-PTFE-16x20-2', '2-Pack', 'Pack Size', '2-Pack', 14.99, 300
FROM products WHERE handle = 'ptfe-cover-sheet-16x20';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-PTFE-16x20-5', '5-Pack', 'Pack Size', '5-Pack', 29.99, 200
FROM products WHERE handle = 'ptfe-cover-sheet-16x20';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-SRP-LETTER-25', 'Default Title', NULL, NULL, 9.99, 400
FROM products WHERE handle = 'silicone-release-paper-letter-25';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-SRP-LETTER-50', 'Default Title', NULL, NULL, 14.99, 600
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-SRP-LETTER-100', 'Default Title', NULL, NULL, 24.99, 400
FROM products WHERE handle = 'silicone-release-paper-letter-100';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-SRP-LEGAL-100', 'Default Title', NULL, NULL, 29.99, 200
FROM products WHERE handle = 'silicone-release-paper-legal-100';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-DP-4x4-100', 'Default Title', NULL, NULL, 12.99, 500
FROM products WHERE handle = 'diamond-painting-squares-100';

INSERT INTO product_variants (product_id, sku, title, option1_name, option1_value, price, inventory_qty)
SELECT id, 'KK-DP-4x4-200', 'Default Title', NULL, NULL, 19.99, 400
FROM products WHERE handle = 'diamond-painting-squares-200';

-- ============================================================
-- PRODUCT METAFIELDS
-- ============================================================
INSERT INTO product_metafields (product_id, best_for, size_code, size_inches, size_cm, format, pack_count, bulk_tier, material, coating_sides, thickness_mil, temp_max_f, temp_max_c, color, reusable, one_liner, bullet_1, bullet_2, bullet_3, care_instructions, storage_instructions, seo_title, seo_description)
SELECT id,
    ARRAY['heat-press', 'sublimation', 'htv', 'dtf'],
    '16x20', '16" x 20"', '40.6cm x 50.8cm', 'sheet', 1, 'starter',
    'PTFE-coated fiberglass', 'single', 3.0, 500, 260,
    'Beige/tan', TRUE,
    'Protects your heat press platen from residue',
    'Reusable hundreds of times', 'Rated to 500°F (260°C)', 'Wipes clean easily',
    'Wipe clean with damp cloth while warm. For stubborn residue use plastic scraper.',
    'Store flat - do not fold',
    'PTFE Cover Sheet 16x20 | Kraft & Kitchen',
    'Reusable PTFE cover sheet for heat press. Protects platen rated to 500°F. Fast shipping from WA.'
FROM products WHERE handle = 'ptfe-cover-sheet-16x20';

INSERT INTO product_metafields (product_id, best_for, size_code, size_inches, size_cm, format, pack_count, bulk_tier, material, coating_sides, color, reusable, one_liner, bullet_1, bullet_2, bullet_3, care_instructions, storage_instructions, seo_title, seo_description)
SELECT id,
    ARRAY['stickers', 'sticker-book', 'transfers'],
    '8.5x11', '8.5" x 11"', '21.6cm x 27.9cm', 'sheet', 50, 'refill',
    'Silicone-coated paper', 'double', 'White', FALSE,
    'Stickers peel clean from both sides',
    'Fits standard 3-ring binders', 'Double-sided silicone coating', 'Best value for growing collections',
    'Store flat away from heat and direct sunlight', 'Store flat in binder or folder',
    'Sticker Book Paper 8.5x11 - 50 Pack | Kraft & Kitchen',
    'Double-sided release paper for sticker books. Letter size fits binders. 50 sheets best value.'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_metafields (product_id, best_for, size_code, size_inches, size_cm, format, pack_count, bulk_tier, material, coating_sides, color, reusable, one_liner, bullet_1, bullet_2, bullet_3, care_instructions, storage_instructions, seo_title, seo_description)
SELECT id,
    ARRAY['diamond-painting'],
    '4x4', '4" x 4"', '10.2cm x 10.2cm', 'square', 200, 'studio',
    'Silicone-coated paper', 'double', 'White', TRUE,
    'Never run out across multiple projects',
    'Pre-cut standard 4x4 size', 'Double-sided - use either side', 'Best value for active diamond painters',
    'Store flat in original packaging', 'Store flat - reuse until worn',
    'Diamond Painting Squares 4x4 - 200 Pack | Kraft & Kitchen',
    'Pre-cut 4x4 release paper squares. 200 pack for multiple diamond painting projects.'
FROM products WHERE handle = 'diamond-painting-squares-200';

-- ============================================================
-- PRODUCT DIFFERENTIATORS (Flagship: Release Paper)
-- ============================================================
INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Clean Release', 1,
    'Stickers peel clean, adhesive stays intact',
    'Medical-grade silicone coating releases adhesives without removing or degrading them. Less product loss, less residue, less frustration.',
    'photo', FALSE, 'Need: peel test photo sequence, residue-free lift macro',
    'Grocery parchment can leave fibers and degrade adhesive'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Thick & Durable', 2,
    '40 lb base weight - nearly 2x thicker than grocery parchment',
    'Resists tearing, holds up to repeated use, professional feel. 40 lb basis weight vs 15-25 lb for typical parchment.',
    'photo', FALSE, 'Need: thickness macro, side-by-side with parchment',
    'Grocery parchment is typically 15-25 lb'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Pre-Cut & Lies Flat', 3,
    'Pre-cut sheets that lie flat immediately - no fighting curl',
    'Legal and letter size sheets ready to use. No unrolling, no curling, no waste from cutting. Fits printers and binders.',
    'photo', FALSE, 'Need: lies flat comparison vs rolled paper',
    'Competitors sell rolls that curl'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Dual-Surface Design', 4,
    'Silicone side releases, paper side prints',
    'Single-sided coating gives you two functional surfaces: silicone for clean release, plain paper for printing templates, notes, or labels.',
    'photo', FALSE, 'Need: side identification photo, printed template example',
    'Double-sided paper wastes one usable surface'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Translucent', 5,
    'See symbols through the paper for diamond painting',
    'Paper is translucent enough to see underlying symbols, enabling diamond painters to work in sections without losing their place.',
    'photo', FALSE, 'Need: photo showing symbols visible through paper',
    'Opaque alternatives require lifting to check position'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Heat Safe', 6,
    'Safe up to 450°F for baking and heat applications',
    'Crosses over into kitchen use as a baking liner and heat press applications. No spray needed, clean release at temperature.',
    'certificate', FALSE, 'CRITICAL: Only claim if third-party tested. Remove if unverified.',
    'Some parchment papers are only rated to 400°F'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO product_differentiators (product_id, pillar_name, pillar_order, headline, description, proof_type, proof_available, proof_notes, comparison_point)
SELECT id, 'Clean Materials', 7,
    'PFAS-free, BPA-free, Quilon-free, unbleached',
    'Clean material claims that matter for food contact and health-conscious makers. No harsh chemicals in the coating process.',
    'certificate', FALSE, 'CRITICAL: Each claim needs manufacturer documentation. Only market verified claims.',
    'Many imports cannot document material safety'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

-- ============================================================
-- USE CASE CONTENT (Stickers tab for Release Paper)
-- ============================================================
INSERT INTO use_case_content (product_id, use_case, tab_order, bullet_1, bullet_2, bullet_3, how_to_step_1, how_to_step_2, how_to_step_3, faq_1_q, faq_1_a, faq_2_q, faq_2_a, faq_3_q, faq_3_a)
SELECT id, 'stickers', 1,
    'Stickers peel clean without losing adhesive',
    'Printable back for custom templates and labels',
    'Fits standard binders for sticker book pages',
    'Place stickers on the silicone (glossy) side',
    'Peel and re-place without losing stickiness',
    'Store flat in a binder, folder, or sticker book',
    'Will my stickers lose their stickiness?',
    'No. Silicone release paper is designed to release adhesives cleanly. Your stickers keep their full adhesive.',
    'Can I print on this paper?',
    'Yes. Laser printers work on the matte (paper) side. Test before full production runs. Inkjet is not recommended.',
    'What size fits my sticker binder?',
    'Letter size (8.5x11) fits standard 3-ring binders. Legal size (8.5x14) needs trimming or oversized binders.'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO use_case_content (product_id, use_case, tab_order, bullet_1, bullet_2, bullet_3, how_to_step_1, how_to_step_2, how_to_step_3, faq_1_q, faq_1_a, faq_2_q, faq_2_a, faq_3_q, faq_3_a)
SELECT id, 'diamond_painting', 2,
    'See symbols through the paper while it protects adhesive',
    'Cover sections you are not working on',
    'Reusable - move squares as you complete areas',
    'Remove original plastic from one section of your canvas',
    'Place release paper squares over exposed adhesive you are not working on',
    'Move squares as you complete sections; re-cover during breaks',
    'Does it work with poured glue canvases?',
    'Yes. Silicone coating releases cleanly from poured glue adhesive without damaging the sticky surface.',
    'How many squares do I need per canvas?',
    '8-12 squares cover a typical 12x16 canvas. 100-pack handles 1-2 projects; 200-pack for multiple.',
    'Can I see the symbols through the paper?',
    'Yes. The paper is translucent enough to see the symbol grid underneath, helping you track your position.'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

INSERT INTO use_case_content (product_id, use_case, tab_order, bullet_1, bullet_2, bullet_3, how_to_step_1, how_to_step_2, how_to_step_3, faq_1_q, faq_1_a, faq_2_q, faq_2_a, faq_3_q, faq_3_a)
SELECT id, 'baking', 3,
    'Clean release - no spray or oil needed',
    'Thick 40 lb base resists tearing even when wet',
    'PFAS-free, BPA-free, Quilon-free (if verified)',
    'Line your baking tray with a sheet, silicone side up',
    'Place food directly on the paper',
    'Bake at your normal settings up to 450°F (if verified)',
    'Is this the same as grocery parchment?',
    'No. This is thicker (40 lb vs ~20 lb), has more consistent silicone coating, and we document our materials.',
    'Can I use it above 400°F?',
    'Our paper is rated to 450°F (pending verification). Do not use under a broiler or over open flame.',
    'Is it safe for food?',
    'Our paper is PFAS-free, BPA-free, and Quilon-free (pending documentation). Contact us for materials documentation.'
FROM products WHERE handle = 'silicone-release-paper-letter-50';

-- ============================================================
-- PAGES
-- ============================================================
INSERT INTO pages (handle, title, page_type, target_keywords, source_file) VALUES
('craft-supplies',
 'Craft Supplies - Release Paper, PTFE Sheets & More',
 'hub',
 ARRAY['craft supplies', 'nonstick craft supplies', 'heat press supplies'],
 'pages/craft-hub-landing-page.html'),

('release-paper-for-stickers',
 'Release Paper for Stickers - Storage & Organization Guide',
 'guide',
 ARRAY['silicone release paper stickers', 'sticker storage paper', 'sticker book pages', 'reusable sticker pages'],
 'pages/seo-content/release-paper-for-stickers.html'),

('diamond-painting-release-paper',
 'Diamond Painting Release Paper - Protect Your Canvas',
 'guide',
 ARRAY['diamond painting release paper', 'diamond painting squares', 'diamond art release paper'],
 'pages/seo-content/diamond-painting-release-paper.html'),

('diamond-painting-dust-protection',
 'Diamond Painting Dust Protection Tips',
 'guide',
 ARRAY['keep dust off diamond painting', 'diamond painting dust', 'diamond painting adhesive protection'],
 'pages/seo-content/diamond-painting-dust-protection.html'),

('ptfe-sheet-for-heat-press',
 'PTFE Sheet for Heat Press - Complete Guide',
 'guide',
 ARRAY['teflon sheet for heat press', 'ptfe sheet heat press', 'non-stick cover sheet'],
 'pages/seo-content/ptfe-sheet-for-heat-press.html'),

('release-paper-vs-parchment',
 'Release Paper vs Parchment Paper - What''s the Difference?',
 'comparison',
 ARRAY['release paper vs parchment paper', 'silicone paper vs parchment', 'parchment paper for crafts'],
 'pages/seo-content/release-paper-vs-parchment.html');

-- ============================================================
-- COLLECTIONS
-- ============================================================
INSERT INTO collections (handle, title, body_html, collection_type, rules, disjunctive, sort_order) VALUES
('heat-press-sublimation',
 'Heat Press + Sublimation',
 '<p>PTFE cover sheets and accessories for heat press, sublimation, and DTF transfers.</p>',
 'smart',
 '[{"column":"tag","relation":"equals","condition":"heat-press"},{"column":"tag","relation":"equals","condition":"sublimation"}]'::jsonb,
 TRUE, 'best-selling'),

('stickers-decals',
 'Stickers + Decals',
 '<p>Silicone release paper for sticker storage, sticker books, and transfer backing.</p>',
 'smart',
 '[{"column":"tag","relation":"equals","condition":"stickers"},{"column":"tag","relation":"equals","condition":"release-paper"}]'::jsonb,
 TRUE, 'best-selling'),

('diamond-painting',
 'Diamond Painting',
 '<p>Release paper squares and sheets to protect your diamond painting canvas adhesive.</p>',
 'smart',
 '[{"column":"tag","relation":"equals","condition":"diamond-painting"}]'::jsonb,
 FALSE, 'best-selling'),

('craft-best-sellers',
 'Craft Best Sellers',
 '<p>Our most popular craft supplies, chosen by makers like you.</p>',
 'smart',
 '[{"column":"tag","relation":"equals","condition":"best-seller"},{"column":"tag","relation":"equals","condition":"craft"}]'::jsonb,
 FALSE, 'best-selling'),

('bulk-business',
 'Bulk & Business',
 '<p>Volume pricing for studios, shops, and production facilities. Same quality, bulk savings.</p>',
 'smart',
 '[{"column":"tag","relation":"equals","condition":"bulk"},{"column":"tag","relation":"equals","condition":"commercial"}]'::jsonb,
 TRUE, 'price-ascending');

-- ============================================================
-- PRIORITY FIXES
-- ============================================================
INSERT INTO priority_fixes (fix_id, title, description, severity, category, manual_action_required, instructions) VALUES
('FIX-001',
 'Remove recurring purchase warning on Release Paper PDP',
 'Shopify shows subscription-style authorization text on the flagship product page. Reads like a hidden subscription even if it is not.',
 'critical', 'conversion', TRUE,
 '1. Go to Shopify Admin > Products > [Release Paper]\n2. Scroll to Purchase options\n3. Remove selling plan associations\n4. OR check Apps > find subscription app > disable for this product\n5. Verify: no "recurring or deferred purchase" text visible on PDP'),

('FIX-002',
 'Remove $7,500 B2B item from Related Products',
 'Custom printing product ($7,500) appears in related items on retail pages, causing sticker shock for craft buyers.',
 'critical', 'conversion', TRUE,
 '1. Go to Online Store > Themes > Customize\n2. Navigate to Product page template\n3. Edit Related Products section\n4. Exclude products tagged b2b or custom-printing\n5. OR create a retail-cross-sells manual collection'),

('FIX-003',
 'Fix Privacy Policy placeholders',
 'Privacy policy contains [[INSERT...]] bracketed placeholders. Credibility hit and potential compliance risk.',
 'critical', 'compliance', TRUE,
 '1. Go to Settings > Policies > Privacy policy\n2. Search for [[ to find all placeholders\n3. Replace with: payment types (Shop Pay, Visa, MC, Amex, Discover, PayPal), tracking (cookies, analytics), contact (support email)\n4. Save and verify'),

('FIX-004',
 'Standardize shipping origin and phone number',
 'Shipping policy says Seattle but store may ship from Bellingham. Different phone numbers across site.',
 'high', 'trust', TRUE,
 '1. Decide on true shipping origin\n2. Update Settings > Policies > Shipping policy\n3. Update Settings > Store details (phone, address)\n4. Update Online Store > Themes > Customize > Footer\n5. Verify consistency across all touchpoints'),

('FIX-005',
 'Add product photography (minimum 10 images)',
 'Current PDP has minimal product storytelling. Need pack shot, thickness macro, side ID, use-case shots, and demo video.',
 'high', 'conversion', TRUE,
 'See creative/photography-shot-list.md for full requirements. Minimum: pack shot, dual-surface diagram, sticker peel demo, diamond painting sectioning, thickness comparison.'),

('FIX-006',
 'Replace quantity dropdown with value ladder',
 'Current bulk quantity selector (1/12/48/144 boxes) overwhelms retail shoppers.',
 'high', 'conversion', TRUE,
 'Replace with named tiers: Starter (50), Standard (250), Studio (500). Gate bulk (3000+) behind Wholesale tab or divider.');
