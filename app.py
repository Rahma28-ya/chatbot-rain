from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
import httpx

app = FastAPI()

# Serve static files + templates
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

MODEL_NAME = "llama3.2"
OLLAMA_URL = "https://YOUR_TUNNEL_DOMAIN/api/generate"

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


#  UI ROUTE (INDEX.HTML)
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

#  CHAT API ROUTE (FASTAPI -> OLLAMA)
@app.post("/chat")
async def chat(req: ChatRequest):

    prompt = (
        SYSTEM_PROMPT
        + "\nUser: " + req.message
        + "\nBot:"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
    }

    async with httpx.AsyncClient(timeout=60.0) as client:
        response = await client.post(OLLAMA_URL, json=payload)

    data = response.json()
    reply = data.get("response", "⚠ Tidak ada respons dari model.")

    return {"reply": reply}
