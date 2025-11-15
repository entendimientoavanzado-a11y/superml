from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()
templates = Jinja2Templates(directory="templates")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_KEY"))

class Transacao(BaseModel):
    nome_cliente: str
    cpf: str
    idade_cliente: int
    produto: str
    valor_compra: float
    quantidade_itens: int
    forma_pagamento: str

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/transacoes")
async def criar(transacao: Transacao):
    try:
        data = supabase.table("transacoes").insert(transacao.dict()).execute()
        return data.data[0]
    except Exception as e:
        raise HTTPException(400, str(e))

@app.get("/transacoes")
async def listar():
    data = supabase.table("transacoes").select("*").execute()
    return data.data