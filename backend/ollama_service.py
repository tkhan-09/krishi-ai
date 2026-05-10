"""
ollama_service.py
=================
Ollama (qwen3:0.6b) LLM integration।
বাংলা ও English উভয় ভাষায় কৃষি পরামর্শ তৈরি করে।
"""

import logging
import os
import httpx
from dotenv import load_dotenv

load_dotenv()
log = logging.getLogger(__name__)

OLLAMA_URL   = os.getenv("OLLAMA_URL", "http://localhost:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "qwen3:0.6b")

# Timeout সেটিংস (qwen3:0.6b ছোট মডেল — দ্রুত)
CONNECT_TIMEOUT  = 5.0
RESPONSE_TIMEOUT = 60.0


class OllamaService:
    """Ollama local LLM এর সাথে কথা বলার সার্ভিস"""

    def __init__(self):
        self.base_url = OLLAMA_URL.rstrip("/")
        self.model    = OLLAMA_MODEL
        log.info(f"OllamaService চালু: {self.base_url}, model={self.model}")

    async def is_available(self) -> bool:
        """Ollama সার্ভার চালু আছে কিনা পরীক্ষা করে"""
        try:
            async with httpx.AsyncClient(timeout=CONNECT_TIMEOUT) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                return resp.status_code == 200
        except Exception:
            return False

    async def generate(self, prompt: str, system: str = None) -> str:
        """
        Ollama দিয়ে text generate করে।

        Args:
            prompt: user prompt
            system: optional system message

        Returns:
            Generated text string
        """
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 512,
            },
        }
        if system:
            payload["system"] = system

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(RESPONSE_TIMEOUT, connect=CONNECT_TIMEOUT)
            ) as client:
                resp = await client.post(
                    f"{self.base_url}/api/generate",
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                text = data.get("response", "").strip()
                log.debug(f"Ollama response ({len(text)} chars)")
                return text

        except httpx.ConnectError:
            log.error("Ollama সংযোগ ব্যর্থ। 'ollama serve' চালু আছে কিনা দেখুন।")
            raise ConnectionError(
                "Ollama সার্ভার পাওয়া যাচ্ছে না। "
                "টার্মিনালে 'ollama serve' চালান।"
            )
        except httpx.TimeoutException:
            log.error("Ollama response timeout")
            raise TimeoutError("Ollama response দিতে বেশি সময় নিচ্ছে। আবার চেষ্টা করুন।")
        except Exception as e:
            log.error(f"Ollama generate ত্রুটি: {e}")
            raise

    async def chat(self, messages: list[dict], system: str = None) -> str:
        """
        Multi-turn chat format এ Ollama কে জিজ্ঞেস করে।

        Args:
            messages: [{"role": "user"|"assistant", "content": "..."}]
            system:   optional system message

        Returns:
            Assistant response string
        """
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": False,
            "options": {
                "temperature": 0.7,
                "top_p": 0.9,
                "num_predict": 512,
            },
        }
        if system:
            payload["system"] = system

        try:
            async with httpx.AsyncClient(
                timeout=httpx.Timeout(RESPONSE_TIMEOUT, connect=CONNECT_TIMEOUT)
            ) as client:
                resp = await client.post(
                    f"{self.base_url}/api/chat",
                    json=payload,
                )
                resp.raise_for_status()
                data = resp.json()
                return data.get("message", {}).get("content", "").strip()

        except httpx.ConnectError:
            raise ConnectionError("Ollama সার্ভার পাওয়া যাচ্ছে না। 'ollama serve' চালান।")
        except Exception as e:
            log.error(f"Ollama chat ত্রুটি: {e}")
            raise

    async def list_models(self) -> list[str]:
        """Ollama তে ডাউনলোড করা মডেলের তালিকা"""
        try:
            async with httpx.AsyncClient(timeout=CONNECT_TIMEOUT) as client:
                resp = await client.get(f"{self.base_url}/api/tags")
                resp.raise_for_status()
                models = resp.json().get("models", [])
                return [m["name"] for m in models]
        except Exception:
            return []