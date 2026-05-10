"""
vision_service.py
ফসলের রোগ সনাক্তকরণ সার্ভিস — Google Gemini API ব্যবহার করে (বিনামূল্যে)
Crop disease detection service using Google Gemini Vision API (free tier)

Free API key: https://aistudio.google.com → Get API Key
"""

import os
import base64
import json
import httpx
from typing import Optional

# Gemini API configuration
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL   = "gemini-2.5-flash"   # ফ্রি tier এ সবচেয়ে ভালো vision মডেল
GEMINI_API_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    f"{GEMINI_MODEL}:generateContent"
)

# ভাষা অনুযায়ী error messages
ERROR_MESSAGES = {
    "bn": {
        "no_image":    "কোনো ছবি দেওয়া হয়নি।",
        "no_api_key":  "Gemini API key সেট করা নেই। GEMINI_API_KEY পরিবেশ চলক সেট করুন।",
        "api_error":   "ছবি বিশ্লেষণে সমস্যা হয়েছে। পরে আবার চেষ্টা করুন।",
        "invalid_image": "ছবিটি সঠিকভাবে পড়া যাচ্ছে না।",
        "no_disease":  "ছবিতে কোনো রোগের লক্ষণ দেখা যাচ্ছে না।",
    },
    "en": {
        "no_image":    "No image provided.",
        "no_api_key":  "Gemini API key is not configured. Set the GEMINI_API_KEY environment variable.",
        "api_error":   "Error analyzing image. Please try again later.",
        "invalid_image": "Unable to read the image properly.",
        "no_disease":  "No disease symptoms detected in the image.",
    },
}

# Bengali prompt
VISION_PROMPT_BN = """তুমি একজন বাংলাদেশের অভিজ্ঞ কৃষি বিশেষজ্ঞ। এই ফসলের ছবিটি বিশ্লেষণ করো।

নিচের JSON format এ উত্তর দাও (শুধু JSON, কোনো extra text নয়):

{
  "disease_name": "রোগের নাম বাংলায়",
  "disease_name_en": "Disease name in English",
  "severity": "হালকা/মাঝারি/গুরুতর",
  "confidence": 85,
  "affected_parts": "আক্রান্ত অংশ (যেমন: পাতা, কান্ড, শিকড়)",
  "symptoms": "দৃশ্যমান লক্ষণের বিবরণ বাংলায়",
  "treatment": "তাৎক্ষণিক চিকিৎসা পরামর্শ বাংলায়",
  "prevention": "ভবিষ্যতে প্রতিরোধের উপায় বাংলায়",
  "is_diseased": true
}

যদি ছবিতে ফসল না থাকে বা রোগ সনাক্ত না হয়:
{
  "disease_name": "সুস্থ ফসল",
  "disease_name_en": "Healthy crop",
  "severity": "নেই",
  "confidence": 90,
  "affected_parts": "নেই",
  "symptoms": "কোনো রোগের লক্ষণ নেই",
  "treatment": "নিয়মিত পরিচর্যা চালিয়ে যান",
  "prevention": "সুষম সার ও সেচ ব্যবস্থাপনা বজায় রাখুন",
  "is_diseased": false
}"""

# English prompt
VISION_PROMPT_EN = """You are an experienced agricultural expert specializing in Bangladesh crops. Analyze this crop image.

Respond ONLY in this JSON format (no extra text):

{
  "disease_name": "Disease name in English",
  "disease_name_en": "Disease name in English",
  "severity": "mild/moderate/severe",
  "confidence": 85,
  "affected_parts": "Affected parts (e.g., leaves, stem, roots)",
  "symptoms": "Description of visible symptoms",
  "treatment": "Immediate treatment recommendation",
  "prevention": "Future prevention methods",
  "is_diseased": true
}

If no crop or disease is detected:
{
  "disease_name": "Healthy crop",
  "disease_name_en": "Healthy crop",
  "severity": "none",
  "confidence": 90,
  "affected_parts": "none",
  "symptoms": "No disease symptoms detected",
  "treatment": "Continue regular maintenance",
  "prevention": "Maintain balanced fertilization and irrigation",
  "is_diseased": false
}"""


async def detect_crop_disease(
    image_base64: str,
    crop_type: Optional[str] = None,
    language: str = "bn",
) -> dict:
    """Gemini Vision দিয়ে ফসলের রোগ সনাক্ত করে।"""
    print(f"[VISION] called — key: {bool(GEMINI_API_KEY)}, img: {len(image_base64) if image_base64 else 0}")
    errors = ERROR_MESSAGES.get(language, ERROR_MESSAGES["bn"])

    # API key check
    if not GEMINI_API_KEY:
        return _error_response(errors["no_api_key"], language)

    # Image validation
    if not image_base64:
        return _error_response(errors["no_image"], language)

    # data URL prefix সরিয়ে নাও
    if "," in image_base64:
        image_base64 = image_base64.split(",")[1]

    # Image type detect করো
    mime_type = _detect_mime_type(image_base64)

    # Prompt তৈরি করো
    base_prompt = VISION_PROMPT_BN if language == "bn" else VISION_PROMPT_EN
    if crop_type:
        crop_ctx = f"\nফসলের ধরন: {crop_type}" if language == "bn" else f"\nCrop type: {crop_type}"
        prompt = base_prompt + crop_ctx
    else:
        prompt = base_prompt

    # Gemini API payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": mime_type,
                            "data": image_base64,
                        }
                    },
                    {"text": prompt},
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.2,
            "maxOutputTokens": 2048,
            "responseMimeType": "application/json",
        },
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                f"{GEMINI_API_URL}?key={GEMINI_API_KEY}",
                json=payload,
                headers={"Content-Type": "application/json"},
            )

        if response.status_code != 200:
            print(f"Gemini API error: {response.status_code} — {response.text}")
            return _error_response(errors["api_error"], language)

        # Response parse করো
        result   = response.json()
        raw_text = (
            result["candidates"][0]["content"]["parts"][0]["text"].strip()
        )

        print(f"[VISION] Gemini raw: {raw_text[:300]}")
        disease_data = _parse_json_response(raw_text)
        if disease_data is None:
            print(f"[VISION] JSON parse failed, raw: {raw_text[:500]}")
            return _error_response(errors["api_error"], language)

        return _normalize_response(disease_data, language)

    except httpx.TimeoutException:
        return _error_response(errors["api_error"], language)
    except Exception as e:
        print(f"Vision service error: {e}")
        return _error_response(errors["api_error"], language)


# ─────────────────────────────────────────────────────
# Helper functions
# ─────────────────────────────────────────────────────

def _detect_mime_type(base64_str: str) -> str:
    """Base64 string এর প্রথম bytes দেখে image type বের করে।"""
    try:
        header = base64.b64decode(base64_str[:16] + "==")[:4]
        if header[:3] == b"\xff\xd8\xff":
            return "image/jpeg"
        elif header[:4] == b"\x89PNG":
            return "image/png"
        elif header[:4] == b"RIFF":
            return "image/webp"
        elif header[:4] == b"GIF8":
            return "image/gif"
        else:
            return "image/jpeg"  # default
    except Exception:
        return "image/jpeg"


def _parse_json_response(text: str) -> Optional[dict]:
    """Gemini response থেকে JSON extract করে।"""
    # সরাসরি parse
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # ```json ... ``` block থেকে বের করো
    if "```json" in text:
        try:
            start = text.index("```json") + 7
            end   = text.index("```", start)
            return json.loads(text[start:end].strip())
        except (ValueError, json.JSONDecodeError):
            pass

    # ``` ... ``` block (without json tag)
    if "```" in text:
        try:
            start = text.index("```") + 3
            end   = text.index("```", start)
            return json.loads(text[start:end].strip())
        except (ValueError, json.JSONDecodeError):
            pass

    # { ... } খুঁজে বের করো
    try:
        start = text.index("{")
        end   = text.rindex("}") + 1
        return json.loads(text[start:end])
    except (ValueError, json.JSONDecodeError):
        pass

    return None


def _normalize_response(data: dict, language: str) -> dict:
    """Response normalize করে consistent format এ রিটার্ন করে।"""
    return {
        "disease_name":    data.get("disease_name",    "অজানা" if language == "bn" else "Unknown"),
        "disease_name_en": data.get("disease_name_en", "Unknown"),
        "severity":        data.get("severity",        "অজানা" if language == "bn" else "Unknown"),
        "confidence":      int(data.get("confidence",  0)),
        "affected_parts":  data.get("affected_parts",  ""),
        "symptoms":        data.get("symptoms",        ""),
        "treatment":       data.get("treatment",       ""),
        "prevention":      data.get("prevention",      ""),
        "is_diseased":     bool(data.get("is_diseased", False)),
        "error":           None,
    }


def _error_response(message: str, language: str) -> dict:
    """Error response তৈরি করে।"""
    return {
        "disease_name":    "ত্রুটি" if language == "bn" else "Error",
        "disease_name_en": "Error",
        "severity":        "অজানা" if language == "bn" else "Unknown",
        "confidence":      0,
        "affected_parts":  "",
        "symptoms":        "",
        "treatment":       "",
        "prevention":      "",
        "is_diseased":     False,
        "error":           message,
    }