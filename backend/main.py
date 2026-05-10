"""
main.py
স্মার্ট কৃষি সহকারী — FastAPI Backend
Smart Agriculture Assistant — FastAPI Backend integrating all services
"""

import os
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

# সার্ভিস import
from backend.database import get_db_connection
from backend.rag_service import RAGService
from backend.ollama_service import OllamaService, OLLAMA_MODEL
from backend.prompt_builder import PromptBuilder
from backend.vision_service import detect_crop_disease
from backend.weather_service import get_weather, get_all_districts

# Service instances
_rag    = RAGService()
_ollama = OllamaService()
_prompt = PromptBuilder()


# ===== Lifespan =====

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("✅ Krishi AI সার্ভার চালু হচ্ছে...")
    yield
    print("🔴 Krishi AI সার্ভার বন্ধ হচ্ছে...")


# ===== App =====

app = FastAPI(
    title="স্মার্ট কৃষি সহকারী API",
    description="AI-powered crop disease detection and farming advisory for Bangladesh",
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Frontend serve করার জন্য
frontend_path = os.path.join(os.path.dirname(__file__), "..", "frontend")
if os.path.exists(frontend_path):
    app.mount("/static", StaticFiles(directory=frontend_path), name="static")

    @app.get("/")
    async def serve_frontend():
        return FileResponse(os.path.join(frontend_path, "index.html"))


# ===== Models =====

class AnalyzeRequest(BaseModel):
    image_base64: Optional[str] = None
    question: Optional[str] = None
    district: Optional[str] = "ঢাকা"
    crop_type: Optional[str] = None
    language: str = "bn"
    model_provider: str = "ollama"          # "ollama" বা "ollama_cloud"
    model_name: Optional[str] = None        # নির্দিষ্ট মডেল (None হলে default)


class AnalyzeResponse(BaseModel):
    disease_name: str
    severity: str
    confidence: int
    treatment: str
    fertilizer: str
    weather_advice: str
    rag_sources: list[str]
    error: Optional[str] = None


class ChatRequest(BaseModel):
    message: str
    district: Optional[str] = "ঢাকা"
    language: str = "bn"
    model_provider: str = "ollama"          # "ollama" বা "ollama_cloud"
    model_name: Optional[str] = None        # নির্দিষ্ট মডেল (None হলে default)


class ChatResponse(BaseModel):
    response: str
    error: Optional[str] = None


# ===== Routes =====


# ===== Ollama Cloud Models (ollama.com hosted) =====
# model name এর শেষে "-cloud" থাকে — এটাই সঠিক format
OLLAMA_CLOUD_MODELS = [
    {"id": "gpt-oss:20b-cloud",        "name": "GPT-OSS 20B",        "provider": "ollama_cloud", "description": "OpenAI • দ্রুত"},
    {"id": "gpt-oss:120b-cloud",       "name": "GPT-OSS 120B",       "provider": "ollama_cloud", "description": "OpenAI • শক্তিশালী"},
    {"id": "deepseek-v3.1:671b-cloud", "name": "DeepSeek V3.1 671B", "provider": "ollama_cloud", "description": "DeepSeek • শক্তিশালী"},
    {"id": "deepseek-r1:671b-cloud",   "name": "DeepSeek R1 671B",   "provider": "ollama_cloud", "description": "Reasoning মডেল"},
    {"id": "qwen3-coder:480b-cloud",   "name": "Qwen3 Coder 480B",   "provider": "ollama_cloud", "description": "Alibaba • কোডিং"},
    {"id": "glm-4.6:cloud",            "name": "GLM 4.6",             "provider": "ollama_cloud", "description": "Zhipu AI • দ্রুত"},
]


async def _call_ollama_cloud(prompt: str, model: str = "gpt-oss:20b-cloud") -> str:
    """
    Ollama Cloud API (ollama.com) দিয়ে text generate করে।
    API key: ollama.com → Settings → Keys
    OpenAI-compatible endpoint ব্যবহার করে।
    """
    import os, httpx
    api_key = os.getenv("OLLAMA_API_KEY", "")
    if not api_key:
        raise ValueError("OLLAMA_API_KEY সেট করা নেই। ollama.com → Settings → Keys থেকে নিন।")

    async with httpx.AsyncClient(timeout=120.0) as client:
        resp = await client.post(
            "https://ollama.com/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json={
                "model": model,
                "stream": False,
                "messages": [{"role": "user", "content": prompt}],
            },
        )
        resp.raise_for_status()
        data = resp.json()
        # OpenAI-compatible format
        return data["choices"][0]["message"]["content"].strip()


@app.get("/health")
async def health_check():
    ollama_ok = await _ollama.is_available()
    db_conn   = get_db_connection()
    db_ok     = db_conn is not None
    if db_conn:
        db_conn.close()

    return {
        "status": "ok",
        "ollama": "connected" if ollama_ok else "disconnected",
        "db":     "connected" if db_ok     else "disconnected",
    }


@app.get("/models")
async def list_models():
    """
    উপলব্ধ সব মডেলের তালিকা রিটার্ন করে।
    - ollama_models: লোকাল Ollama মডেল
    """
    # Ollama local models
    ollama_models = []
    try:
        raw = await _ollama.list_models()
        ollama_models = [
            {"id": m, "name": m, "provider": "ollama"}
            for m in raw
        ]
    except Exception:
        pass

    return {
        "ollama_models": ollama_models,
        "ollama_cloud_models": OLLAMA_CLOUD_MODELS,
        "default_ollama": OLLAMA_MODEL,
    }


@app.post("/analyze", response_model=AnalyzeResponse)
async def analyze_crop(request: AnalyzeRequest):
    language   = request.language if request.language in ["bn", "en"] else "bn"
    district   = request.district or "ঢাকা"
    crop_type  = request.crop_type or ("ধান" if language == "bn" else "rice")

    # ── Validation ──────────────────────────────
    question_text = (request.question or "").strip()
    has_question  = bool(question_text)
    has_crop      = bool(request.crop_type and request.crop_type.strip())

    has_image = bool(request.image_base64 and request.image_base64.strip())

    errors = []
    if not has_crop:
        errors.append("ফসল সিলেক্ট করা আবশ্যক।" if language == "bn" else "Crop selection is required.")
    # ছবি না থাকলে question mandatory
    if not has_question and not has_image:
        errors.append("প্রশ্ন বা সমস্যার বিবরণ লেখা আবশ্যক।" if language == "bn" else "Please describe the problem or question.")

    if errors:
        raise HTTPException(status_code=422, detail=" | ".join(errors))
    # ────────────────────────────────────────────

    # ১. Vision analysis (ছবি থাকলে)
    disease_info = {
        "disease_name": "",
        "severity": "",
        "confidence": 0,
        "treatment": "",
        "is_diseased": False,
        "error": None,
    }
    if request.image_base64:
        disease_info = await detect_crop_disease(
            image_base64=request.image_base64,
            crop_type=request.crop_type,
            language=language,
        )

    # ২. Weather
    weather_data = await get_weather(district=district, language=language)
    weather_advice_text = (
        weather_data["farming_advice"][0]
        if weather_data.get("farming_advice")
        else ""
    )

    # ৩. RAG retrieval
    query = request.question or disease_info.get("disease_name", "")
    if request.crop_type:
        query = f"{request.crop_type} {query}"

    rag_results = []
    rag_sources = []
    if query:
        rag_results = await _rag.retrieve(query=query, top_k=3)
        rag_sources = _rag.get_source_titles(rag_results, language=language)

    # RAG context string তৈরি করো (PromptBuilder এর জন্য)
    rag_context = _rag.format_context(rag_results, language=language)

    # ৪. Prompt + LLM (Ollama বা Ollama Cloud)
    prompt = _prompt.build_analyze_prompt(
        question=request.question or "",
        rag_context=rag_context,
        district=district,
        crop_type=crop_type,
        language=language,
    )

    if request.model_provider == "ollama_cloud":
        model = request.model_name or "meta-llama/llama-3.3-8b-instruct:free"
        ollama_response = await _call_ollama_cloud(prompt=prompt, model=model)
    else:
        if request.model_name:
            _ollama.model = request.model_name
        ollama_response = await _ollama.generate(prompt=prompt)

    # ৫. Response assemble
    disease_label = (
        disease_info.get("disease_name", "")
        or ("কোনো রোগ নেই" if language == "bn" else "No disease detected")
    )
    severity_label = (
        disease_info.get("severity", "")
        or ("নেই" if language == "bn" else "None")
    )

    # Ollama response parse করার চেষ্টা (JSON হলে fertilizer নাও)
    parsed = _prompt.parse_analyze_response(ollama_response, language=language)
    fertilizer_text = parsed.get("fertilizer", ollama_response)

    # Gemini treatment আছে কিনা দেখো, না থাকলে Ollama parsed থেকে নাও
    treatment_text = (
        disease_info.get("treatment", "")
        or parsed.get("treatment", "")
    )
    # fertilizer Ollama থেকে, না হলে Gemini prevention
    if not fertilizer_text or fertilizer_text == ollama_response:
        fertilizer_text = (
            parsed.get("fertilizer", "")
            or disease_info.get("prevention", "")
            or ollama_response
        )

    print(f"[ANALYZE] disease={disease_label}, confidence={disease_info.get('confidence',0)}, treatment_len={len(treatment_text)}")

    return AnalyzeResponse(
        disease_name=disease_label,
        severity=severity_label,
        confidence=disease_info.get("confidence", 0),
        treatment=treatment_text,
        fertilizer=fertilizer_text,
        weather_advice=weather_advice_text,
        rag_sources=rag_sources,
        error=disease_info.get("error"),
    )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    language = request.language if request.language in ["bn", "en"] else "bn"
    district = request.district or "ঢাকা"

    if not request.message or not request.message.strip():
        raise HTTPException(
            status_code=422,
            detail=(
                "প্রশ্ন খালি রাখা যাবে না।"
                if language == "bn"
                else "Message cannot be empty."
            ),
        )

    # RAG retrieval
    rag_results = await _rag.retrieve(query=request.message, top_k=3)
    rag_context = _rag.format_context(rag_results, language=language)

    # Prompt তৈরি
    prompt = _prompt.build_chat_prompt(
        message=request.message,
        rag_context=rag_context,
        district=district,
        language=language,
    )

    if request.model_provider == "ollama_cloud":
        model = request.model_name or "meta-llama/llama-3.3-8b-instruct:free"
        response_text = await _call_ollama_cloud(prompt=prompt, model=model)
    else:
        if request.model_name:
            _ollama.model = request.model_name
        response_text = await _ollama.generate(prompt=prompt)

    return ChatResponse(response=response_text)


@app.get("/weather/{district}")
async def get_district_weather(district: str, language: str = "bn"):
    language = language if language in ["bn", "en"] else "bn"
    weather  = await get_weather(district=district, language=language)

    if weather.get("error") and weather.get("temperature") == 0:
        raise HTTPException(status_code=404, detail=weather["error"])

    return weather


@app.get("/districts")
async def list_districts():
    return {"districts": get_all_districts()}