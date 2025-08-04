from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.message import MessageIn
from app.models.message import Message

async def responder_mensagem(msg: MessageIn, db: AsyncSession) -> str:
    if "preço" in msg.mensagem.lower():
        resposta = "Nosso produto custa R$ 37!"
    else:
        resposta = "Mensagem recebida com sucesso."

    mensagem = Message(
        telefone=msg.telefone,
        mensagem=msg.mensagem,
        resposta=resposta,
    )

    db.add(mensagem)
    await db.commit()
    await db.refresh(mensagem)

    return resposta
