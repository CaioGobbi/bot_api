from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import whatsapp, auth  # certifique-se que "auth.py" existe
from app.routes import rule  # no topo


app = FastAPI(title="Bot WhatsApp API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui rotas
app.include_router(whatsapp.router, prefix="/api/whatsapp")
app.include_router(auth.router, prefix="/api/auth")  # só se o arquivo auth.py existir
app.include_router(rule.router)