# 🌾 স্মার্ট কৃষি সহকারী
### AI-চালিত ফসলের রোগ সনাক্তকরণ ও কৃষি পরামর্শ সেবা

বাংলাদেশের কৃষকদের জন্য একটি সম্পূর্ণ AI-চালিত সহকারী — ফসলের ছবি দিলে রোগ সনাক্ত করবে, সার পরামর্শ দেবে, এবং ৬৪ জেলার আবহাওয়া অনুযায়ী গাইডেন্স দেবে।

---

## ✨ বৈশিষ্ট্যসমূহ

- 🦠 **ফসলের রোগ সনাক্তকরণ** — ছবি আপলোড করলেই Claude AI রোগ চিহ্নিত করবে
- 💊 **চিকিৎসা পরামর্শ** — রোগ অনুযায়ী কার্যকর সমাধান
- 🌱 **সার সুপারিশ** — Ollama (qwen3) দিয়ে বাংলায় পরামর্শ
- 🌤️ **আবহাওয়া তথ্য** — বাংলাদেশের ৬৪ জেলার রিয়েল-টাইম আবহাওয়া
- 💬 **বাংলা চ্যাট** — যেকোনো কৃষি প্রশ্নের উত্তর
- 🌐 **ভাষা পরিবর্তন** — বাংলা ↔ English টগল

---

## 🛠️ প্রযুক্তি স্ট্যাক

| প্রযুক্তি | কাজ |
|-----------|-----|
| Python + FastAPI | Backend API |
| Ollama (qwen3:0.6b) | বাংলায় পরামর্শ (Local LLM) |
| PostgreSQL + pgvector | RAG Vector Database |
| Claude claude-haiku-4-5 | ছবি বিশ্লেষণ |
| Open-Meteo API | বিনামূল্যে আবহাওয়া তথ্য |
| HTML + CSS + JS | Frontend (Vanilla) |

---

## ⚡ দ্রুত শুরু

### ১. প্রয়োজনীয় সফটওয়্যার

```bash
# Python 3.10+
python3 --version

# PostgreSQL
sudo apt install postgresql postgresql-contrib  # Ubuntu
brew install postgresql  # macOS

# Ollama (https://ollama.com)
curl -fsSL https://ollama.com/install.sh | sh
```

### ২. প্রজেক্ট ক্লোন করুন

```bash
git clone <your-repo-url>
cd krishi_ai
```

### ৩. Environment সেটআপ

```bash
cp .env.example .env
nano .env  # DB_PASSWORD ও ANTHROPIC_API_KEY সেট করুন
```

### ৪. PostgreSQL সেটআপ

```bash
# PostgreSQL চালু করুন
sudo service postgresql start  # Linux
brew services start postgresql  # macOS

# Database তৈরি করুন
createdb -U postgres krishi_db

# pgvector extension ইনস্টল করুন
sudo apt install postgresql-15-pgvector  # Ubuntu
# অথবা: pip install pgvector

# Schema তৈরি করুন
psql -U postgres -d krishi_db -f scripts/setup_db.sql
```

### ৫. Python dependencies

```bash
pip3 install -r requirements.txt
```

### ৬. Knowledge Base সেটআপ (একবার)

```bash
cd backend
python3 knowledge_base/seed_data.py      # ডেটা তৈরি করুন
python3 knowledge_base/embed_knowledge.py  # Embed করুন
```

### ৭. সব একসাথে চালু করুন

```bash
chmod +x run.sh
./run.sh
```

**এটুকুই!** 🎉

- **API:** `http://localhost:8000`
- **API Docs:** `http://localhost:8000/docs`
- **Frontend:** `frontend/index.html` ব্রাউজারে খুলুন

---

## 📁 ফাইল স্ট্রাকচার

```
krishi_ai/
├── backend/
│   ├── main.py                  ← FastAPI app (সব routes)
│   ├── database.py              ← PostgreSQL connection
│   ├── rag_service.py           ← RAG retrieval logic
│   ├── ollama_service.py        ← Ollama LLM integration
│   ├── vision_service.py        ← Crop disease detection
│   ├── weather_service.py       ← Open-Meteo weather API
│   ├── prompt_builder.py        ← Prompt Engineering templates
│   └── knowledge_base/
│       ├── seed_data.py         ← Bengali agricultural data
│       └── embed_knowledge.py   ← Embed & store in PostgreSQL
├── frontend/
│   └── index.html               ← Single-page বাংলা UI
├── scripts/
│   └── setup_db.sql             ← PostgreSQL schema
├── .env                         ← API keys & config (গোপন রাখুন)
├── .env.example                 ← Template
├── requirements.txt             ← Python dependencies
├── run.sh                       ← One-command startup
└── README.md                    ← এই ফাইল
```

---

## 🔌 API Endpoints

### `POST /analyze` — ফসল বিশ্লেষণ
```json
{
  "image_base64": "...",
  "question": "আমার ধানে কী হয়েছে?",
  "district": "ঢাকা",
  "crop_type": "ধান",
  "language": "bn"
}
```

### `POST /chat` — সাধারণ প্রশ্ন
```json
{ "message": "সার কখন দেবো?", "district": "রাজশাহী", "language": "bn" }
```

### `GET /weather/{district}` — আবহাওয়া
```
GET /weather/ঢাকা?language=bn
```

### `GET /districts` — সব জেলার তালিকা
```
GET /districts
```

### `GET /health` — সার্ভিস স্ট্যাটাস
```json
{ "status": "ok", "ollama": "connected", "db": "connected" }
```

---

## ⚙️ Environment Variables

| Variable | বিবরণ | Default |
|----------|--------|---------|
| `DB_HOST` | PostgreSQL host | localhost |
| `DB_PORT` | PostgreSQL port | 5432 |
| `DB_NAME` | Database নাম | krishi_db |
| `DB_USER` | Database user | postgres |
| `DB_PASSWORD` | Database password | **সেট করুন** |
| `OLLAMA_URL` | Ollama server URL | http://localhost:11434 |
| `OLLAMA_MODEL` | Ollama model | qwen3:0.6b |
| `ANTHROPIC_API_KEY` | Claude API key | **সেট করুন** |
| `APP_PORT` | Server port | 8000 |
| `DEFAULT_LANGUAGE` | Default ভাষা | bn |

---

## 🐛 সমস্যা সমাধান

### Ollama সংযোগ হচ্ছে না
```bash
ollama serve  # আলাদা terminal এ
ollama pull qwen3:0.6b
```

### PostgreSQL connection error
```bash
sudo service postgresql start
psql -U postgres -c "\l"  # database list দেখুন
```

### pgvector ইনস্টল সমস্যা
```bash
# Ubuntu
sudo apt install postgresql-15-pgvector
# Python
pip install pgvector
```

### Claude API কাজ করছে না
- `.env` এ `ANTHROPIC_API_KEY` সঠিকভাবে সেট করুন
- API key free tier limit চেক করুন: https://console.anthropic.com

---

## 📝 লাইসেন্স

MIT License — বাংলাদেশের কৃষকদের জন্য মুক্তভাবে ব্যবহারযোগ্য।

---

*🌾 বাংলাদেশের কৃষিকে আধুনিক করতে তৈরি — কৃষকের বন্ধু, AI সহকারী।*
