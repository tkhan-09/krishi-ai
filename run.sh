#!/bin/bash
# =====================================================
# স্মার্ট কৃষি সহকারী — One-Command Startup Script
# Smart Agriculture Assistant — run.sh
# =====================================================
# ব্যবহার: chmod +x run.sh && ./run.sh
# Usage:   chmod +x run.sh && ./run.sh
# =====================================================

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

echo ""
echo -e "${GREEN}🌾 স্মার্ট কৃষি সহকারী — Starting...${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""

# ===== Step 1: Check .env file =====
if [ ! -f ".env" ]; then
  if [ -f ".env.example" ]; then
    echo -e "${YELLOW}⚠️  .env file পাওয়া যায়নি। .env.example থেকে কপি করা হচ্ছে...${NC}"
    cp .env.example .env
    echo -e "${YELLOW}   .env ফাইলটি খুলে DB_PASSWORD ও ANTHROPIC_API_KEY সেট করুন।${NC}"
    echo ""
  else
    echo -e "${RED}❌ .env ও .env.example কোনোটাই নেই! Setup গাইড দেখুন।${NC}"
    exit 1
  fi
fi

# Load .env
export $(grep -v '^#' .env | grep -v '^$' | xargs)

APP_PORT=${APP_PORT:-8000}

# ===== Step 2: Check Python =====
echo -e "${BLUE}🐍 Python চেক করা হচ্ছে...${NC}"
if ! command -v python3 &>/dev/null; then
  echo -e "${RED}❌ Python 3 ইনস্টল করা নেই। https://python.org থেকে ইনস্টল করুন।${NC}"
  exit 1
fi
PYTHON_VER=$(python3 -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')")
echo -e "${GREEN}   ✅ Python ${PYTHON_VER} পাওয়া গেছে।${NC}"

# ===== Step 3: Install Python dependencies =====
echo ""
echo -e "${BLUE}📦 Python dependencies ইনস্টল করা হচ্ছে...${NC}"
if [ -f "requirements.txt" ]; then
  pip3 install -r requirements.txt -q --disable-pip-version-check
  echo -e "${GREEN}   ✅ Dependencies ইনস্টল হয়েছে।${NC}"
else
  echo -e "${YELLOW}   ⚠️  requirements.txt নেই, skip করা হচ্ছে।${NC}"
fi

# ===== Step 4: Check PostgreSQL =====
echo ""
echo -e "${BLUE}🐘 PostgreSQL চেক করা হচ্ছে...${NC}"
if command -v pg_isready &>/dev/null; then
  if pg_isready -h "${DB_HOST:-localhost}" -p "${DB_PORT:-5432}" -q 2>/dev/null; then
    echo -e "${GREEN}   ✅ PostgreSQL চলছে।${NC}"
  else
    echo -e "${YELLOW}   ⚠️  PostgreSQL সংযোগ করা যাচ্ছে না।${NC}"
    echo -e "${YELLOW}      চালু করুন: sudo service postgresql start${NC}"
  fi
else
  echo -e "${YELLOW}   ⚠️  pg_isready পাওয়া যায়নি — PostgreSQL manually চেক করুন।${NC}"
fi

# Database setup (প্রথমবার চালালে)
if command -v psql &>/dev/null; then
  DB_EXISTS=$(psql -U "${DB_USER:-postgres}" -h "${DB_HOST:-localhost}" \
    -tc "SELECT 1 FROM pg_database WHERE datname='${DB_NAME:-krishi_db}'" 2>/dev/null | tr -d ' ')
  if [ "$DB_EXISTS" != "1" ]; then
    echo -e "${BLUE}   🔧 Database '${DB_NAME:-krishi_db}' তৈরি করা হচ্ছে...${NC}"
    createdb -U "${DB_USER:-postgres}" -h "${DB_HOST:-localhost}" "${DB_NAME:-krishi_db}" 2>/dev/null || true
    if [ -f "scripts/setup_db.sql" ]; then
      psql -U "${DB_USER:-postgres}" -h "${DB_HOST:-localhost}" \
        -d "${DB_NAME:-krishi_db}" -f scripts/setup_db.sql -q 2>/dev/null || true
      echo -e "${GREEN}   ✅ Database schema তৈরি হয়েছে।${NC}"
    fi
  fi
fi

# Knowledge base embedding (প্রথমবার)
if [ -f "backend/knowledge_base/embed_knowledge.py" ]; then
  echo -e "${BLUE}   📚 Knowledge base embed করা হচ্ছে (প্রথমবার কিছুক্ষণ লাগবে)...${NC}"
  python3 backend/knowledge_base/embed_knowledge.py --check-first 2>/dev/null || true
fi

# ===== Step 5: Check & Start Ollama =====
echo ""
echo -e "${BLUE}🤖 Ollama চেক করা হচ্ছে...${NC}"
OLLAMA_URL=${OLLAMA_URL:-http://localhost:11434}

if command -v ollama &>/dev/null; then
  # Check if Ollama server is running
  if curl -s "${OLLAMA_URL}/api/tags" -o /dev/null 2>/dev/null; then
    echo -e "${GREEN}   ✅ Ollama চলছে।${NC}"
  else
    echo -e "${BLUE}   🚀 Ollama server চালু করা হচ্ছে...${NC}"
    ollama serve &>/dev/null &
    OLLAMA_PID=$!
    sleep 3
    echo -e "${GREEN}   ✅ Ollama চালু হয়েছে (PID: ${OLLAMA_PID})${NC}"
  fi

  # Check if model is available
  OLLAMA_MODEL=${OLLAMA_MODEL:-qwen3:0.6b}
  if ollama list 2>/dev/null | grep -q "${OLLAMA_MODEL}"; then
    echo -e "${GREEN}   ✅ Model '${OLLAMA_MODEL}' পাওয়া গেছে।${NC}"
  else
    echo -e "${YELLOW}   📥 Model '${OLLAMA_MODEL}' ডাউনলোড করা হচ্ছে (একবারই লাগবে)...${NC}"
    ollama pull "${OLLAMA_MODEL}"
    echo -e "${GREEN}   ✅ Model ডাউনলোড সম্পন্ন।${NC}"
  fi
else
  echo -e "${YELLOW}   ⚠️  Ollama ইনস্টল নেই। https://ollama.com থেকে ইনস্টল করুন।${NC}"
  echo -e "${YELLOW}      ইনস্টলের পর: ollama pull qwen3:0.6b${NC}"
fi

# ===== Step 6: Start FastAPI =====
echo ""
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}🚀 FastAPI Server চালু হচ্ছে...${NC}"
echo ""
echo -e "${GREEN}   🌐 App URL:    http://localhost:${APP_PORT}${NC}"
echo -e "${GREEN}   📖 API Docs:   http://localhost:${APP_PORT}/docs${NC}"
echo -e "${CYAN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo ""
echo -e "${YELLOW}   Frontend চালু করতে: frontend/index.html ব্রাউজারে খুলুন${NC}"
echo -e "${YELLOW}   বন্ধ করতে: Ctrl+C${NC}"
echo ""

# Trap to cleanup on exit
cleanup() {
  echo ""
  echo -e "${YELLOW}🛑 Server বন্ধ করা হচ্ছে...${NC}"
  if [ -n "$OLLAMA_PID" ]; then
    kill $OLLAMA_PID 2>/dev/null || true
  fi
  echo -e "${GREEN}   বিদায়! আবার আসবেন। 🌾${NC}"
  exit 0
}
trap cleanup INT TERM

# Start server
cd backend
python3 -m uvicorn main:app \
  --host 0.0.0.0 \
  --port "${APP_PORT}" \
  --reload \
  --reload-dir . \
  --log-level info
