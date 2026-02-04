-- Kraft & Kitchen Supabase Schema
-- Migration: 001_initial_schema
-- Run this in Supabase SQL Editor: https://supabase.com/dashboard/project/YOUR_PROJECT/sql

-- ============================================================
-- 1. PRODUCTS TABLE (Source of truth for all product content)
-- ============================================================
CREATE TABLE IF NOT EXISTS products (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    handle TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    body_html TEXT,
    vendor TEXT DEFAULT 'Kraft & Kitchen',
    product_type TEXT,
    tags TEXT[],
    published BOOLEAN DEFAULT TRUE,

    -- Shopify sync
    shopify_product_id BIGINT,
    shopify_synced_at TIMESTAMPTZ,
    shopify_sync_status TEXT DEFAULT 'pending' CHECK (shopify_sync_status IN ('pending', 'synced', 'failed', 'dirty')),

    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 2. PRODUCT VARIANTS
-- ============================================================
CREATE TABLE IF NOT EXISTS product_variants (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    sku TEXT,
    title TEXT NOT NULL DEFAULT 'Default Title',
    option1_name TEXT,
    option1_value TEXT,
    option2_name TEXT,
    option2_value TEXT,
    price DECIMAL(10,2) NOT NULL,
    compare_at_price DECIMAL(10,2),
    inventory_qty INTEGER DEFAULT 0,
    inventory_policy TEXT DEFAULT 'continue',
    requires_shipping BOOLEAN DEFAULT TRUE,
    taxable BOOLEAN DEFAULT TRUE,

    -- Shopify sync
    shopify_variant_id BIGINT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 3. PRODUCT METAFIELDS (Structured product attributes)
-- ============================================================
CREATE TABLE IF NOT EXISTS product_metafields (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,

    -- Core attributes
    best_for TEXT[],
    size_code TEXT,
    size_inches TEXT,
    size_cm TEXT,
    format TEXT CHECK (format IN ('sheet', 'square', 'roll', 'mat')),
    pack_count INTEGER,
    bulk_tier TEXT CHECK (bulk_tier IN ('starter', 'refill', 'studio', 'case', 'master')),

    -- Material specs
    material TEXT,
    coating_sides TEXT CHECK (coating_sides IN ('single', 'double')),
    thickness_mil DECIMAL(4,2),
    basis_weight TEXT,
    color TEXT,
    reusable BOOLEAN DEFAULT FALSE,

    -- Temperature
    temp_max_f INTEGER,
    temp_max_c INTEGER,

    -- Safety claims (with verification tracking)
    pfas_free BOOLEAN,
    pfas_free_verified BOOLEAN DEFAULT FALSE,
    bpa_free BOOLEAN,
    bpa_free_verified BOOLEAN DEFAULT FALSE,
    quilon_free BOOLEAN,
    quilon_free_verified BOOLEAN DEFAULT FALSE,
    food_safe BOOLEAN,
    food_safe_verified BOOLEAN DEFAULT FALSE,

    -- Marketing copy
    one_liner TEXT,
    bullet_1 TEXT,
    bullet_2 TEXT,
    bullet_3 TEXT,
    care_instructions TEXT,
    storage_instructions TEXT,

    -- SEO
    seo_title TEXT,
    seo_description TEXT,
    image_alt_text TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(product_id)
);

-- ============================================================
-- 4. PRODUCT DIFFERENTIATORS
-- ============================================================
CREATE TABLE IF NOT EXISTS product_differentiators (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    pillar_name TEXT NOT NULL,
    pillar_order INTEGER NOT NULL DEFAULT 0,
    headline TEXT NOT NULL,
    description TEXT NOT NULL,
    proof_type TEXT CHECK (proof_type IN ('photo', 'video', 'testimonial', 'spec', 'comparison', 'certificate')),
    proof_available BOOLEAN DEFAULT FALSE,
    proof_notes TEXT,
    comparison_point TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 5. USE CASE CONTENT (Per-product, per-segment messaging)
-- ============================================================
CREATE TABLE IF NOT EXISTS use_case_content (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID NOT NULL REFERENCES products(id) ON DELETE CASCADE,
    use_case TEXT NOT NULL CHECK (use_case IN (
        'stickers', 'sticker_books', 'diamond_painting',
        'baking', 'heat_press', 'transfers',
        'lab_packaging', 'resin', 'general'
    )),
    tab_order INTEGER DEFAULT 0,

    -- Messaging
    bullet_1 TEXT,
    bullet_2 TEXT,
    bullet_3 TEXT,
    how_to_step_1 TEXT,
    how_to_step_2 TEXT,
    how_to_step_3 TEXT,

    -- FAQs for this use case
    faq_1_q TEXT,
    faq_1_a TEXT,
    faq_2_q TEXT,
    faq_2_a TEXT,
    faq_3_q TEXT,
    faq_3_a TEXT,

    -- Recommended add-ons
    addon_1_handle TEXT,
    addon_2_handle TEXT,
    addon_3_handle TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(product_id, use_case)
);

-- ============================================================
-- 6. PAGES (SEO content, landing pages)
-- ============================================================
CREATE TABLE IF NOT EXISTS pages (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    handle TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    body_html TEXT,
    page_type TEXT CHECK (page_type IN ('landing', 'guide', 'comparison', 'hub', 'policy', 'about')),
    published BOOLEAN DEFAULT TRUE,

    -- SEO
    seo_title TEXT,
    seo_description TEXT,
    target_keywords TEXT[],

    -- Shopify sync
    shopify_page_id BIGINT,
    shopify_synced_at TIMESTAMPTZ,
    shopify_sync_status TEXT DEFAULT 'pending' CHECK (shopify_sync_status IN ('pending', 'synced', 'failed', 'dirty')),

    -- Source file reference
    source_file TEXT,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 7. COLLECTIONS
-- ============================================================
CREATE TABLE IF NOT EXISTS collections (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    handle TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    body_html TEXT,
    collection_type TEXT DEFAULT 'smart' CHECK (collection_type IN ('smart', 'manual')),
    rules JSONB,
    disjunctive BOOLEAN DEFAULT FALSE,
    sort_order TEXT DEFAULT 'best-selling',
    published BOOLEAN DEFAULT TRUE,

    -- Shopify sync
    shopify_collection_id BIGINT,
    shopify_synced_at TIMESTAMPTZ,
    shopify_sync_status TEXT DEFAULT 'pending' CHECK (shopify_sync_status IN ('pending', 'synced', 'failed', 'dirty')),

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 8. CUSTOMER REVIEWS (Review pipeline)
-- ============================================================
CREATE TABLE IF NOT EXISTS reviews (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    product_id UUID REFERENCES products(id) ON DELETE SET NULL,
    source TEXT NOT NULL CHECK (source IN ('website', 'email_request', 'import', 'marketplace')),
    author_name TEXT,
    author_email TEXT,
    rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
    title TEXT,
    body TEXT NOT NULL,
    use_case_tags TEXT[],
    highlight_quote TEXT,
    pdp_section TEXT,
    photo_urls TEXT[],
    verified_purchase BOOLEAN DEFAULT FALSE,
    approved BOOLEAN DEFAULT FALSE,
    featured BOOLEAN DEFAULT FALSE,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 9. DEPLOYMENT LOG (Track all sync attempts)
-- ============================================================
CREATE TABLE IF NOT EXISTS deployment_log (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    deployment_type TEXT NOT NULL CHECK (deployment_type IN (
        'product', 'page', 'collection', 'metafield', 'theme', 'full'
    )),
    target_handle TEXT,
    target_shopify_id BIGINT,
    action TEXT NOT NULL CHECK (action IN ('create', 'update', 'delete')),
    status TEXT NOT NULL CHECK (status IN ('started', 'success', 'failed', 'retrying')),
    request_payload JSONB,
    response_payload JSONB,
    error_message TEXT,
    retry_count INTEGER DEFAULT 0,
    duration_ms INTEGER,

    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- 10. PRIORITY FIXES TRACKER
-- ============================================================
CREATE TABLE IF NOT EXISTS priority_fixes (
    id UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    fix_id TEXT UNIQUE NOT NULL,
    title TEXT NOT NULL,
    description TEXT,
    severity TEXT NOT NULL CHECK (severity IN ('critical', 'high', 'medium', 'low')),
    category TEXT CHECK (category IN ('conversion', 'trust', 'compliance', 'ux', 'seo')),
    status TEXT DEFAULT 'open' CHECK (status IN ('open', 'in_progress', 'completed', 'verified', 'wont_fix')),
    manual_action_required BOOLEAN DEFAULT FALSE,
    instructions TEXT,
    completed_at TIMESTAMPTZ,
    verified_at TIMESTAMPTZ,

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ============================================================
-- INDEXES
-- ============================================================
CREATE INDEX IF NOT EXISTS idx_products_handle ON products(handle);
CREATE INDEX IF NOT EXISTS idx_products_sync_status ON products(shopify_sync_status);
CREATE INDEX IF NOT EXISTS idx_pages_handle ON pages(handle);
CREATE INDEX IF NOT EXISTS idx_pages_sync_status ON pages(shopify_sync_status);
CREATE INDEX IF NOT EXISTS idx_collections_handle ON collections(handle);
CREATE INDEX IF NOT EXISTS idx_reviews_product ON reviews(product_id);
CREATE INDEX IF NOT EXISTS idx_reviews_approved ON reviews(approved, featured);
CREATE INDEX IF NOT EXISTS idx_reviews_use_case ON reviews USING GIN(use_case_tags);
CREATE INDEX IF NOT EXISTS idx_deployment_log_type ON deployment_log(deployment_type, status);
CREATE INDEX IF NOT EXISTS idx_deployment_log_created ON deployment_log(created_at DESC);
CREATE INDEX IF NOT EXISTS idx_priority_fixes_status ON priority_fixes(status, severity);

-- ============================================================
-- UPDATED_AT TRIGGER
-- ============================================================
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE OR REPLACE TRIGGER products_updated_at
    BEFORE UPDATE ON products FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE OR REPLACE TRIGGER product_metafields_updated_at
    BEFORE UPDATE ON product_metafields FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE OR REPLACE TRIGGER pages_updated_at
    BEFORE UPDATE ON pages FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE OR REPLACE TRIGGER collections_updated_at
    BEFORE UPDATE ON collections FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE OR REPLACE TRIGGER reviews_updated_at
    BEFORE UPDATE ON reviews FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE OR REPLACE TRIGGER priority_fixes_updated_at
    BEFORE UPDATE ON priority_fixes FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================
-- VIEWS (Useful dashboard queries)
-- ============================================================

-- Products pending sync
CREATE OR REPLACE VIEW v_products_pending_sync AS
SELECT p.handle, p.title, p.shopify_sync_status, p.updated_at,
       pm.one_liner, pm.best_for
FROM products p
LEFT JOIN product_metafields pm ON pm.product_id = p.id
WHERE p.shopify_sync_status IN ('pending', 'dirty', 'failed')
ORDER BY p.updated_at DESC;

-- Pages pending sync
CREATE OR REPLACE VIEW v_pages_pending_sync AS
SELECT handle, title, page_type, shopify_sync_status, updated_at
FROM pages
WHERE shopify_sync_status IN ('pending', 'dirty', 'failed')
ORDER BY updated_at DESC;

-- Review highlights by use case
CREATE OR REPLACE VIEW v_review_highlights AS
SELECT
    unnest(use_case_tags) AS use_case,
    highlight_quote,
    rating,
    author_name,
    pdp_section
FROM reviews
WHERE approved = TRUE AND featured = TRUE AND highlight_quote IS NOT NULL
ORDER BY rating DESC;

-- Deployment summary
CREATE OR REPLACE VIEW v_deployment_summary AS
SELECT
    deployment_type,
    status,
    COUNT(*) AS count,
    MAX(created_at) AS last_attempt
FROM deployment_log
GROUP BY deployment_type, status
ORDER BY deployment_type, status;

-- Open priority fixes
CREATE OR REPLACE VIEW v_open_fixes AS
SELECT fix_id, title, severity, category, status, manual_action_required
FROM priority_fixes
WHERE status NOT IN ('completed', 'verified', 'wont_fix')
ORDER BY
    CASE severity
        WHEN 'critical' THEN 1
        WHEN 'high' THEN 2
        WHEN 'medium' THEN 3
        WHEN 'low' THEN 4
    END;

-- Differentiator proof status
CREATE OR REPLACE VIEW v_differentiator_proof_status AS
SELECT
    p.title AS product,
    pd.pillar_name,
    pd.headline,
    pd.proof_type,
    pd.proof_available,
    pd.proof_notes
FROM product_differentiators pd
JOIN products p ON p.id = pd.product_id
ORDER BY p.title, pd.pillar_order;
