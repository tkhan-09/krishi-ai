-- ============================================================
-- স্মার্ট কৃষি সহকারী — PostgreSQL Schema
-- pgvector extension সহ RAG-এর জন্য
-- ============================================================

-- pgvector extension চালু করুন (একবারই লাগবে)
CREATE EXTENSION IF NOT EXISTS vector;

-- ============================================================
-- knowledge_base টেবিল — কৃষি তথ্য ও embedding
-- ============================================================
CREATE TABLE IF NOT EXISTS knowledge_base (
    id          SERIAL PRIMARY KEY,
    category    VARCHAR(100) NOT NULL,           -- রোগ / সার / আবহাওয়া / ফসল
    crop        VARCHAR(100),                     -- ধান / গম / পাট / সবজি / ফল
    title_bn    TEXT NOT NULL,                   -- বাংলা শিরোনাম
    title_en    TEXT,                            -- English শিরোনাম
    content_bn  TEXT NOT NULL,                   -- বাংলায় বিস্তারিত তথ্য
    content_en  TEXT,                            -- English-এ বিস্তারিত তথ্য
    keywords    TEXT[],                          -- অনুসন্ধানের কীওয়ার্ড
    embedding   vector(384),                     -- all-MiniLM-L6-v2 এর output
    created_at  TIMESTAMP DEFAULT NOW()
);

-- embedding-এর জন্য IVFFlat index (দ্রুত cosine similarity search)
CREATE INDEX IF NOT EXISTS knowledge_embedding_idx
    ON knowledge_base
    USING ivfflat (embedding vector_cosine_ops)
    WITH (lists = 50);

-- category ও crop-এর জন্য সাধারণ index
CREATE INDEX IF NOT EXISTS knowledge_category_idx ON knowledge_base (category);
CREATE INDEX IF NOT EXISTS knowledge_crop_idx     ON knowledge_base (crop);

-- ============================================================
-- chat_history টেবিল — কথোপকথনের ইতিহাস
-- ============================================================
CREATE TABLE IF NOT EXISTS chat_history (
    id          SERIAL PRIMARY KEY,
    session_id  VARCHAR(100) NOT NULL,
    role        VARCHAR(20) NOT NULL CHECK (role IN ('user', 'assistant')),
    message     TEXT NOT NULL,
    language    VARCHAR(5) DEFAULT 'bn',
    district    VARCHAR(100),
    created_at  TIMESTAMP DEFAULT NOW()
);

CREATE INDEX IF NOT EXISTS chat_session_idx ON chat_history (session_id, created_at);

-- ============================================================
-- analysis_log টেবিল — ছবি বিশ্লেষণের লগ
-- ============================================================
CREATE TABLE IF NOT EXISTS analysis_log (
    id              SERIAL PRIMARY KEY,
    district        VARCHAR(100),
    crop_type       VARCHAR(100),
    disease_name    VARCHAR(200),
    severity        VARCHAR(50),
    confidence      INTEGER,
    language        VARCHAR(5) DEFAULT 'bn',
    created_at      TIMESTAMP DEFAULT NOW()
);

-- ============================================================
-- সফলভাবে তৈরি হলে নিশ্চিত করুন
-- ============================================================
DO $$
BEGIN
    RAISE NOTICE '✅ krishi_db schema সফলভাবে তৈরি হয়েছে।';
    RAISE NOTICE '   Tables: knowledge_base, chat_history, analysis_log';
    RAISE NOTICE '   Extension: pgvector (vector dimension: 384)';
END $$;
