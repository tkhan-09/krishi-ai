"""
rag_service.py
==============
RAG (Retrieval-Augmented Generation) সার্ভিস।
কৃষকের প্রশ্ন embed করে pgvector দিয়ে
knowledge_base থেকে সবচেয়ে প্রাসঙ্গিক তথ্য খুঁজে বের করে।
"""

import logging
from typing import Optional

from sentence_transformers import SentenceTransformer
from backend.database import execute_vector_query

log = logging.getLogger(__name__)

MODEL_NAME = "all-MiniLM-L6-v2"
MIN_SIMILARITY = 0.25  # এর নিচে হলে ফলাফল বাদ দেওয়া হবে


class RAGService:
    """Vector similarity দিয়ে knowledge base থেকে তথ্য retrieve করে"""

    def __init__(self):
        log.info(f"RAGService: embedding model লোড হচ্ছে ({MODEL_NAME})...")
        self._model = SentenceTransformer(MODEL_NAME)
        log.info("✅ RAGService প্রস্তুত")

    def _embed(self, text: str) -> list[float]:
        """Text কে 384-মাত্রার vector এ রূপান্তর করে"""
        return self._model.encode(text, normalize_embeddings=True).tolist()

    async def retrieve(
        self,
        query: str,
        crop: Optional[str] = None,
        top_k: int = 3,
    ) -> list[dict]:
        """
        প্রশ্নের সাথে সবচেয়ে মিলে যাওয়া knowledge entries খুঁজে বের করে।

        Args:
            query:  কৃষকের প্রশ্ন বা বিষয়
            crop:   নির্দিষ্ট ফসল (যেমন "ধান") — ঐচ্ছিক
            top_k:  কতটি ফলাফল চাই

        Returns:
            list of dicts — প্রতিটিতে title, content, similarity আছে
        """
        try:
            # প্রশ্নটি embed করুন
            embedding = self._embed(query)

            # pgvector দিয়ে cosine similarity search করুন
            results = execute_vector_query(embedding, top_k=top_k, crop=crop)

            # খুব কম similarity এর ফলাফল বাদ দিন
            filtered = [r for r in results if r.get("similarity", 0) >= MIN_SIMILARITY]

            log.info(f"RAG: '{query[:40]}...' → {len(filtered)}/{len(results)} ফলাফল")
            return filtered

        except Exception as e:
            log.error(f"RAG retrieve ত্রুটি: {e}")
            return []  # ত্রুটি হলে খালি list — LLM তবুও উত্তর দেবে

    def format_context(self, results: list[dict], language: str = "bn") -> str:
        """
        RAG ফলাফলগুলো prompt এ দেওয়ার জন্য formatted text এ রূপান্তর করে।

        Args:
            results:  retrieve() এর ফলাফল
            language: "bn" বা "en"

        Returns:
            Formatted context string
        """
        if not results:
            return (
                "প্রাসঙ্গিক তথ্য পাওয়া যায়নি।"
                if language == "bn"
                else "No relevant information found."
            )

        lines = []
        for i, r in enumerate(results, 1):
            if language == "bn":
                title   = r.get("title_bn") or r.get("title_en", "")
                content = r.get("content_bn") or r.get("content_en", "")
            else:
                title   = r.get("title_en") or r.get("title_bn", "")
                content = r.get("content_en") or r.get("content_bn", "")

            sim = r.get("similarity", 0)
            lines.append(f"[{i}] {title} (প্রাসঙ্গিকতা: {sim:.0%})\n{content}")

        separator = "\n\n---\n\n"
        return separator.join(lines)

    def get_source_titles(self, results: list[dict], language: str = "bn") -> list[str]:
        """RAG ফলাফলের শিরোনামগুলো list আকারে রিটার্ন করে"""
        key = "title_bn" if language == "bn" else "title_en"
        return [r.get(key) or r.get("title_bn", "") for r in results]
