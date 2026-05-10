"""
prompt_builder.py
=================
Prompt Engineering টেমপ্লেট মডিউল।
4টি template: analyze, chat, vision, weather
বাংলা ও English উভয় ভাষায় কাজ করে।
"""

import json
import logging
import re

log = logging.getLogger(__name__)


# ============================================================
# ভাষা নির্দেশনা
# ============================================================
def _lang_instruction(language: str) -> str:
    if language == "bn":
        return "সম্পূর্ণ উত্তর বাংলায় দিন। সহজ ও স্পষ্ট ভাষা ব্যবহার করুন যা সাধারণ কৃষক বুঝতে পারবেন।"
    return "Answer completely in English. Use simple, clear language suitable for farmers."


class PromptBuilder:
    """Ollama এর জন্য prompt তৈরি করার ক্লাস"""

    # ============================================================
    # Template 1: /analyze endpoint এর জন্য
    # ============================================================
    def build_analyze_prompt(
        self,
        question: str,
        rag_context: str,
        district: str = "ঢাকা",
        crop_type: str = "ধান",
        language: str = "bn",
    ) -> str:
        """
        ফসলের রোগ বিশ্লেষণ ও পরামর্শের জন্য prompt তৈরি করে।
        Output একটি JSON object হবে।
        """
        lang_inst = _lang_instruction(language)

        if language == "bn":
            return f"""তুমি বাংলাদেশের একজন অভিজ্ঞ কৃষি বিশেষজ্ঞ।

{lang_inst}

কৃষকের তথ্য:
- জেলা: {district}
- ফসল: {crop_type}
- প্রশ্ন: {question}

প্রাসঙ্গিক কৃষি জ্ঞান:
{rag_context}

উপরের তথ্যের ভিত্তিতে নিচের JSON format এ উত্তর দাও (শুধু JSON, অন্য কিছু না):
{{
  "disease_name": "রোগের নাম বা সমস্যার নাম",
  "severity": "হালকা/মাঝারি/গুরুতর",
  "confidence": 75,
  "treatment": "বিস্তারিত চিকিৎসা পরামর্শ",
  "fertilizer": "সার বা পুষ্টি সংক্রান্ত পরামর্শ",
  "weather_advice": "আবহাওয়া অনুযায়ী পরামর্শ"
}}"""
        else:
            return f"""You are an experienced agricultural expert for Bangladesh.

{lang_inst}

Farmer's information:
- District: {district}
- Crop: {crop_type}
- Question: {question}

Relevant agricultural knowledge:
{rag_context}

Based on the above, respond ONLY with this JSON format:
{{
  "disease_name": "Name of the disease or problem",
  "severity": "mild/moderate/severe",
  "confidence": 75,
  "treatment": "Detailed treatment advice",
  "fertilizer": "Fertilizer or nutrition advice",
  "weather_advice": "Weather-based farming advice"
}}"""

    # ============================================================
    # Template 2: /chat endpoint এর জন্য
    # ============================================================
    def build_chat_prompt(
        self,
        message: str,
        rag_context: str,
        district: str = "ঢাকা",
        language: str = "bn",
    ) -> str:
        """
        সাধারণ কৃষি প্রশ্নের উত্তরের জন্য prompt তৈরি করে।
        """
        lang_inst = _lang_instruction(language)

        if language == "bn":
            return f"""তুমি বাংলাদেশের একজন বন্ধুত্বপূর্ণ কৃষি পরামর্শদাতা।
কৃষকের সাথে সহজ বাংলায় কথা বলো।

{lang_inst}

কৃষকের জেলা: {district}

প্রাসঙ্গিক তথ্য:
{rag_context}

কৃষকের প্রশ্ন: {message}

সংক্ষিপ্ত ও কার্যকর উত্তর দাও:"""
        else:
            return f"""You are a friendly agricultural advisor for Bangladesh.
Speak simply and helpfully with farmers.

{lang_inst}

Farmer's district: {district}

Relevant information:
{rag_context}

Farmer's question: {message}

Give a concise, practical answer:"""

    # ============================================================
    # Template 3: Vision analysis (SESSION 3 এ ব্যবহার হবে)
    # ============================================================
    def build_vision_prompt(
        self,
        crop_type: str = "ধান",
        language: str = "bn",
    ) -> str:
        """
        Claude Vision API এর জন্য ছবি বিশ্লেষণের prompt।
        """
        if language == "bn":
            return f"""এই ছবিতে {crop_type} গাছের কোনো রোগ বা সমস্যা আছে কিনা দেখো।

নিচের JSON format এ উত্তর দাও (শুধু JSON):
{{
  "disease_name": "রোগের নাম (বাংলায়)",
  "severity": "হালকা/মাঝারি/গুরুতর",
  "confidence": 80,
  "symptoms": "দৃশ্যমান লক্ষণের বিবরণ",
  "immediate_action": "তাৎক্ষণিক করণীয়"
}}

যদি কোনো রোগ না দেখা যায়: disease_name = "সুস্থ", confidence = 95"""
        else:
            return f"""Examine this image for any disease or problem in the {crop_type} plant.

Respond ONLY with this JSON:
{{
  "disease_name": "Name of disease",
  "severity": "mild/moderate/severe",
  "confidence": 80,
  "symptoms": "Description of visible symptoms",
  "immediate_action": "Immediate action to take"
}}

If no disease found: disease_name = "Healthy", confidence = 95"""

    # ============================================================
    # Template 4: Weather-based farming advice
    # ============================================================
    def build_weather_prompt(
        self,
        district: str,
        temperature: float,
        humidity: float,
        rain_probability: float,
        language: str = "bn",
    ) -> str:
        """
        আবহাওয়া ডেটার ভিত্তিতে কৃষি পরামর্শের prompt।
        """
        lang_inst = _lang_instruction(language)

        if language == "bn":
            return f"""তুমি একজন কৃষি আবহাওয়া বিশেষজ্ঞ।

{lang_inst}

{district} জেলার আজকের আবহাওয়া:
- তাপমাত্রা: {temperature}°C
- আর্দ্রতা: {humidity}%
- বৃষ্টির সম্ভাবনা: {rain_probability}%

এই আবহাওয়ায় কৃষকের জন্য সংক্ষিপ্ত পরামর্শ দাও (২-৩ বাক্যে):"""
        else:
            return f"""You are an agricultural weather specialist.

{lang_inst}

Today's weather in {district}:
- Temperature: {temperature}°C
- Humidity: {humidity}%
- Rain probability: {rain_probability}%

Give brief farming advice for this weather (2-3 sentences):"""

    # ============================================================
    # Response Parser
    # ============================================================
    def parse_analyze_response(self, raw: str, language: str = "bn") -> dict:
        """
        Ollama এর raw text response থেকে JSON parse করে।
        JSON না পেলে fallback dict রিটার্ন করে।
        """
        # JSON block খুঁজুন
        try:
            # সরাসরি parse করার চেষ্টা
            cleaned = raw.strip()
            # markdown code block বাদ দিন
            cleaned = re.sub(r"```json\s*", "", cleaned)
            cleaned = re.sub(r"```\s*", "", cleaned)
            # প্রথম { থেকে শেষ } পর্যন্ত নিন
            start = cleaned.find("{")
            end   = cleaned.rfind("}") + 1
            if start >= 0 and end > start:
                json_str = cleaned[start:end]
                return json.loads(json_str)
        except (json.JSONDecodeError, ValueError):
            pass

        # JSON parse ব্যর্থ হলে — raw text কে treatment এ রাখুন
        log.warning("Analyze response JSON parse ব্যর্থ — fallback ব্যবহার করা হচ্ছে")
        if language == "bn":
            return {
                "disease_name": "বিশ্লেষণ সম্পন্ন",
                "severity": "অজানা",
                "confidence": 0,
                "treatment": raw.strip(),
                "fertilizer": "আরও তথ্যের জন্য স্থানীয় কৃষি অফিসে যোগাযোগ করুন।",
                "weather_advice": "আবহাওয়া অনুযায়ী সতর্ক থাকুন।",
            }
        else:
            return {
                "disease_name": "Analysis complete",
                "severity": "Unknown",
                "confidence": 0,
                "treatment": raw.strip(),
                "fertilizer": "Contact your local agriculture office for more information.",
                "weather_advice": "Stay alert to weather conditions.",
            }
