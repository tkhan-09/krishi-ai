"""
embed_knowledge.py
==================
Bengali agricultural knowledge base এর text embedding তৈরি করে
PostgreSQL (pgvector) এ সংরক্ষণ করে।

চালানোর আগে নিশ্চিত করুন:
  - PostgreSQL চালু আছে এবং krishi_db তৈরি হয়েছে
  - setup_db.sql রান করা হয়েছে
  - sentence-transformers ইনস্টল আছে
  - .env ফাইলে সঠিক DB credentials আছে

চালানোর পদ্ধতি:
  python backend/knowledge_base/embed_knowledge.py
"""

import sys
import os

# প্রজেক্টের root থেকে চালানোর জন্য path ঠিক করুন
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

import time
import logging
from dotenv import load_dotenv
from sentence_transformers import SentenceTransformer
from backend.database import get_db_connection
from backend.knowledge_base.seed_data import get_all_entries

# লগ সেটআপ
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger(__name__)

# .env লোড করুন
load_dotenv()

# ============================================================
# Embedding Model লোড করুন
# all-MiniLM-L6-v2: 384 মাত্রা, দ্রুত ও বাংলায় মোটামুটি কার্যকর
# ============================================================
MODEL_NAME = "all-MiniLM-L6-v2"


def load_model() -> SentenceTransformer:
    """Sentence-Transformer মডেল লোড করে"""
    log.info(f"মডেল লোড হচ্ছে: {MODEL_NAME}")
    model = SentenceTransformer(MODEL_NAME)
    log.info("✅ মডেল লোড সম্পন্ন")
    return model


def build_embed_text(entry: dict) -> str:
    """
    একটি knowledge entry থেকে embedding-এর জন্য text তৈরি করে।
    বাংলা ও English উভয় কন্টেন্ট মিলিয়ে দিলে retrieval ভালো হয়।
    """
    parts = [
        entry.get("title_bn", ""),
        entry.get("title_en", ""),
        entry.get("content_bn", ""),
        entry.get("content_en", "") or "",
        " ".join(entry.get("keywords", [])),
    ]
    # শূন্য অংশ বাদ দিয়ে জোড়া দিন
    return " | ".join(p for p in parts if p.strip())


def clear_existing_data(conn) -> None:
    """knowledge_base টেবিল পরিষ্কার করে নতুন করে insert করার জন্য"""
    with conn.cursor() as cur:
        cur.execute("DELETE FROM knowledge_base")
    conn.commit()
    log.info("🗑️  পুরনো knowledge_base ডেটা মুছে ফেলা হয়েছে")


def insert_entry(conn, entry: dict, embedding: list) -> None:
    """একটি entry ও তার embedding PostgreSQL এ সংরক্ষণ করে"""
    sql = """
        INSERT INTO knowledge_base
            (category, crop, title_bn, title_en, content_bn, content_en, keywords, embedding)
        VALUES
            (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    values = (
        entry.get("category"),
        entry.get("crop"),
        entry.get("title_bn"),
        entry.get("title_en"),
        entry.get("content_bn"),
        entry.get("content_en"),
        entry.get("keywords", []),
        embedding,  # pgvector vector type
    )
    with conn.cursor() as cur:
        cur.execute(sql, values)
    conn.commit()


def embed_and_store(clear_first: bool = True) -> None:
    """
    সব knowledge entries embed করে PostgreSQL এ store করে।

    Args:
        clear_first: True হলে আগের ডেটা মুছে নতুন insert করে
    """
    start = time.time()

    # ডেটাবেস সংযোগ
    log.info("PostgreSQL এ সংযোগ হচ্ছে...")
    conn = get_db_connection()
    if conn is None:
        log.error("❌ ডেটাবেস সংযোগ ব্যর্থ। .env ফাইল চেক করুন।")
        sys.exit(1)

    # মডেল লোড
    model = load_model()

    # প্রয়োজনে পুরনো ডেটা মুছুন
    if clear_first:
        clear_existing_data(conn)

    # সব entry লোড করুন
    entries = get_all_entries()
    total = len(entries)
    log.info(f"মোট {total}টি entry embedding করা হবে...")

    success = 0
    errors = 0

    for i, entry in enumerate(entries, 1):
        try:
            # Embedding text তৈরি করুন
            embed_text = build_embed_text(entry)

            # Embedding তৈরি করুন
            embedding = model.encode(embed_text, normalize_embeddings=True).tolist()

            # ডেটাবেসে সংরক্ষণ করুন
            insert_entry(conn, entry, embedding)

            log.info(f"  [{i}/{total}] ✅ {entry['title_bn']}")
            success += 1

        except Exception as e:
            log.error(f"  [{i}/{total}] ❌ ত্রুটি — {entry.get('title_bn', 'Unknown')}: {e}")
            errors += 1

    # সংযোগ বন্ধ করুন
    conn.close()

    elapsed = time.time() - start
    log.info("=" * 60)
    log.info(f"✅ Embedding সম্পন্ন!")
    log.info(f"   সফল: {success}/{total}")
    log.info(f"   ত্রুটি: {errors}/{total}")
    log.info(f"   সময়: {elapsed:.1f} সেকেন্ড")
    log.info("=" * 60)


def verify_storage() -> None:
    """ডেটাবেসে সংরক্ষিত ডেটা যাচাই করে"""
    conn = get_db_connection()
    if conn is None:
        log.error("❌ যাচাই করতে ডেটাবেস সংযোগ লাগবে")
        return

    with conn.cursor() as cur:
        # মোট count
        cur.execute("SELECT COUNT(*) FROM knowledge_base")
        total = cur.fetchone()[0]

        # Category ভিত্তিক count
        cur.execute(
            "SELECT category, COUNT(*) FROM knowledge_base GROUP BY category ORDER BY COUNT(*) DESC"
        )
        cat_counts = cur.fetchall()

        # Embedding dimension চেক
        cur.execute("SELECT array_length(embedding::real[], 1) FROM knowledge_base LIMIT 1")
        dim = cur.fetchone()

    conn.close()

    log.info("\n📊 ডেটাবেস যাচাই:")
    log.info(f"   মোট entries: {total}")
    log.info(f"   Embedding মাত্রা: {dim[0] if dim else 'N/A'}")
    log.info("   ক্যাটাগরি অনুযায়ী:")
    for cat, count in cat_counts:
        log.info(f"     {cat}: {count}টি")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="কৃষি জ্ঞানভাণ্ডার embed ও store করুন")
    parser.add_argument(
        "--no-clear",
        action="store_true",
        help="আগের ডেটা না মুছে নতুন ডেটা যোগ করুন",
    )
    parser.add_argument(
        "--verify-only",
        action="store_true",
        help="শুধু ডেটাবেস যাচাই করুন (কোনো insert নয়)",
    )
    args = parser.parse_args()

    if args.verify_only:
        verify_storage()
    else:
        embed_and_store(clear_first=not args.no_clear)
        verify_storage()
