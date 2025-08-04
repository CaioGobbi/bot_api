from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.schemas.message import MessageIn, MessageOut
from app.services.whatsapp_service import responder_mensagem
from app.database import SessionLocal
from app.models.message import Message
from app.core.deps import usuario_autenticado

from fastapi import APIRouter, Depends
from app.routes.auth import get_current_user

router = APIRouter()

async def get_db():
    async with SessionLocal() as session:
        yield session

@router.post("/mensagem")
async def receber_mensagem(mensagem: MessageIn, db: AsyncSession = Depends(get_db)):
    resposta = await responder_mensagem(mensagem, db)
    return {"resposta": resposta}

@router.get("/mensagens", response_model=List[MessageOut])
async def listar_mensagens(
    db: AsyncSession = Depends(get_db),
    usuario: str = Depends(usuario_autenticado)
):
    result = await db.execute(select(Message).order_by(Message.criado_em.desc()))
    mensagens = result.scalars().all()
    return mensagens

@router.get("/mensagens")
async def listar_mensagens(user_email: str = Depends(get_current_user)):
    return {"mensagens": f"Estas são as mensagens do usuário: {user_email}"}