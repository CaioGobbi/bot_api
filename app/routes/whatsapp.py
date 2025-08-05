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

from app.models.rule import Rule
from app.schemas.message import IncomingMessage
from sqlalchemy import select

from sqlalchemy import func

from app.schemas.rule import RuleCreate

from fastapi import HTTPException



router = APIRouter(prefix="/api/whatsapp")

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


@router.post("/mensagem")
async def receber_mensagem(dados: IncomingMessage, db: AsyncSession = Depends(get_db)):
    # 1. Salva a mensagem recebida
    nova_msg = Message(telefone=dados.telefone, mensagem=dados.mensagem)
    db.add(nova_msg)
    await db.commit()

    # 2. Busca TODAS as regras cadastradas
    result = await db.execute(select(Rule))
    regras = result.scalars().all()

    # 3. Verifica se alguma palavra-chave está contida na mensagem recebida
    resposta = "Mensagem recebida, em breve responderemos."
    for regra in regras:
        if regra.palavra_chave.lower() in dados.mensagem.lower():
            resposta = regra.resposta
            break

    # 4. Atualiza a resposta da mensagem
    nova_msg.resposta = resposta
    await db.commit()

    return {
        "telefone": dados.telefone,
        "mensagem_recebida": dados.mensagem,
        "resposta": resposta
    }

@router.get("/regras")
async def listar_regras(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule))
    regras = result.scalars().all()
    return regras

@router.post("/regras")
async def criar_regra(rule: RuleCreate, db: AsyncSession = Depends(get_db)):
    nova_regra = Rule(**rule.dict())
    db.add(nova_regra)
    await db.commit()
    await db.refresh(nova_regra)
    return nova_regra

@router.put("/regras/{regra_id}")
async def atualizar_regra(regra_id: int, dados: RuleCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule).where(Rule.id == regra_id))
    regra = result.scalars().first()
    if not regra:
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    
    regra.palavra_chave = dados.palavra_chave
    regra.resposta = dados.resposta
    await db.commit()
    return regra

@router.delete("/regras/{regra_id}")
async def deletar_regra(regra_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Rule).where(Rule.id == regra_id))
    regra = result.scalars().first()
    if not regra:
        raise HTTPException(status_code=404, detail="Regra não encontrada")
    
    await db.delete(regra)
    await db.commit()
    return {"msg": "Regra deletada com sucesso"}
