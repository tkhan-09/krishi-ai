"""
database.py
===========
PostgreSQL ডেটাবেস সংযোগ মডিউল।
psycopg2 ব্যবহার করে krishi_db তে সংযোগ স্থাপন করে।
pgvector extension সহ কাজ করে।
"""

import os
import logging
from typing import Optional

import psycopg2
import psycopg2.extras
from dotenv import load_dotenv

# .env লোড করুন
load_dotenv()

log = logging.getLogger(__name__)

# ============================================================
# ডেটাবেস কনফিগারেশন (.env থেকে)
# ============================================================
DB_CONFIG = {
    "host":     os.getenv("DB_HOST", "localhost"),
    "port":     int(os.getenv("DB_PORT", "5432")),
    "dbname":   os.getenv("DB_NAME", "krishi_db"),
    "user":     os.getenv("DB_USER", "postgres"),
    "password": os.getenv("DB_PASSWORD", ""),
}


def get_db_connection() -> Optional[psycopg2.extensions.connection]:
    """
    PostgreSQL এ নতুন সংযোগ তৈরি করে রিটার্ন করে।

    Returns:
        psycopg2 connection অবজেক্ট, ব্যর্থ হলে None।

    ব্যবহার:
        conn = get_db_connection()
        if conn:
            with conn.cursor() as cur:
                cur.execute("SELECT 1")
            conn.close()
    """
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        # pgvector এর vector type register করুন
        psycopg2.extras.register_default_jsonb(conn)
        log.debug("✅ PostgreSQL সংযোগ সফল")
        return conn
    except psycopg2.OperationalError as e:
        log.error(f"❌ PostgreSQL সংযোগ ব্যর্থ: {e}")
        log.error(
            f"   DB: {DB_CONFIG['user']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}"
            f"/{DB_CONFIG['dbname']}"
        )
        return None


def check_connection() -> dict:
    """
    ডেটাবেস সংযোগ ও pgvector extension যাচাই করে।

    Returns:
        {"status": "ok"|"error", "message": str, "details": dict}
    """
    conn = get_db_connection()
    if conn is None:
        return {
            "status": "error",
            "message": "ডেটাবেস সংযোগ করা যাচ্ছে না",
            "details": DB_CONFIG,
        }

    try:
        with conn.cursor() as cur:
            # PostgreSQL version
            cur.execute("SELECT version()")
            pg_version = cur.fetchone()[0]

            # pgvector extension চেক
            cur.execute(
                "SELECT installed_version FROM pg_available_extensions WHERE name = 'vector'"
            )
            row = cur.fetchone()
            vector_version = row[0] if row else "not installed"

            # knowledge_base table চেক
            cur.execute("SELECT COUNT(*) FROM knowledge_base")
            kb_count = cur.fetchone()[0]

        conn.close()

        return {
            "status": "ok",
            "message": "ডেটাবেস সংযোগ সফল",
            "details": {
                "postgres": pg_version.split(",")[0],
                "pgvector": vector_version,
                "knowledge_entries": kb_count,
            },
        }
    except Exception as e:
        conn.close()
        return {
            "status": "error",
            "message": f"ডেটাবেস পরীক্ষায় ত্রুটি: {e}",
            "details": {},
        }


def execute_query(sql: str, params: tuple = (), fetch: bool = True):
    """
    একটি SQL query চালিয়ে ফলাফল রিটার্ন করে।

    Args:
        sql:    SQL query string
        params: প্যারামিটার tuple
        fetch:  True হলে fetchall() করে, False হলে শুধু commit করে

    Returns:
        fetch=True: list of tuples
        fetch=False: None

    Raises:
        Exception on DB error
    """
    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("ডেটাবেস সংযোগ ব্যর্থ")

    try:
        with conn.cursor() as cur:
            cur.execute(sql, params)
            if fetch:
                results = cur.fetchall()
            else:
                results = None
        conn.commit()
        return results
    except Exception as e:
        conn.rollback()
        log.error(f"Query ত্রুটি: {e}\nSQL: {sql}\nParams: {params}")
        raise
    finally:
        conn.close()


def execute_vector_query(embedding: list, top_k: int = 3, crop: str = None) -> list:
    """
    pgvector cosine similarity দিয়ে knowledge_base এ অনুসন্ধান করে।

    Args:
        embedding: query vector (384 মাত্রা)
        top_k:     কতটি ফলাফল চাই
        crop:      নির্দিষ্ট ফসলে সীমাবদ্ধ রাখতে চাইলে (যেমন "ধান")

    Returns:
        list of dicts with keys: id, title_bn, title_en, content_bn, content_en,
                                  category, crop, keywords, similarity
    """
    # Vector কে PostgreSQL এর জন্য format করুন
    vec_str = "[" + ",".join(str(v) for v in embedding) + "]"

    if crop:
        sql = """
            SELECT
                id, title_bn, title_en, content_bn, content_en,
                category, crop, keywords,
                1 - (embedding <=> %s::vector) AS similarity
            FROM knowledge_base
            WHERE crop = %s OR crop IS NULL
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        params = (vec_str, crop, vec_str, top_k)
    else:
        sql = """
            SELECT
                id, title_bn, title_en, content_bn, content_en,
                category, crop, keywords,
                1 - (embedding <=> %s::vector) AS similarity
            FROM knowledge_base
            ORDER BY embedding <=> %s::vector
            LIMIT %s
        """
        params = (vec_str, vec_str, top_k)

    conn = get_db_connection()
    if conn is None:
        raise ConnectionError("ডেটাবেস সংযোগ ব্যর্থ")

    try:
        with conn.cursor(cursor_factory=psycopg2.extras.DictCursor) as cur:
            cur.execute(sql, params)
            rows = cur.fetchall()

        return [dict(row) for row in rows]

    except Exception as e:
        log.error(f"Vector query ত্রুটি: {e}")
        raise
    finally:
        conn.close()


# ============================================================
# সরাসরি চালালে connection check করুন
# ============================================================
if __name__ == "__main__":
    import json

    logging.basicConfig(level=logging.INFO)
    print("\n📡 ডেটাবেস সংযোগ পরীক্ষা করা হচ্ছে...\n")
    result = check_connection()
    print(json.dumps(result, ensure_ascii=False, indent=2))
