from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

# ====== CORS (INI YANG PENTING) ======
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],      # ganti domain frontend kalau mau lebih aman
    allow_credentials=True,
    allow_methods=["*"],      # IZINKAN OPTIONS
    allow_headers=["*"],
)

# ====== Static & Templates ======
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

# ====== Groq Config ======
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
client = Groq(api_key=GROQ_API_KEY)

MODEL_NAME = "llama-3.1-8b-instant"

SYSTEM_PROMPT = """
Kamu adalah Mining Safety & Operational Assistant (MSOA).

Fokus utama:
- keselamatan kerja tambang (K3)
- operasional tambang (hauling, loading, blasting, pit control)
- dampak cuaca terhadap aktivitas tambang
- kondisi jalan tambang
- rekomendasi mitigasi risiko dan SOP teknis

Cara menjawab:
- Jika pertanyaan tentang tambang/cuaca/operasional → jawab PANJANG, lengkap, teknis seperti laporan engineer tambang.
- Jika pertanyaan di luar tambang → tetap jawab, singkat, jelas, dan informatif seperti asisten umum.
- Jangan menolak pertanyaan apa pun.

Gaya bahasa:
- Profesional dan mudah dipahami.
- Untuk topik tambang → sangat teknis dan detail.
"""

class ChatRequest(BaseModel):
    message: str

# ====== UI Route ======
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# ====== Chat API ======
@app.post("/chat")
async def chat(req: ChatRequest):

    completion = client.chat.completions.create(
        model=MODEL_NAME,
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.message}
        ],
        temperature=0.5,
    )

    reply = completion.choices[0].message.content
    return {"reply": reply}
