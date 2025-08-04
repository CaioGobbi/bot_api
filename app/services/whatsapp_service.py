from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.schemas.message import MessageIn
from app.models.message import Message
from app.models.rule import Rule

async def responder_mensagem(msg: MessageIn, db: AsyncSession) -> str:
    # Busca todas as regras cadastradas
    result = await db.execute(select(Rule))
    regras = result.scalars().all()

    # Procura se alguma palavra-chave está contida na mensagem
    resposta = "Mensagem recebida com sucesso."
    for regra in regras:
        if regra.palavra_chave.lower() in msg.mensagem.lower():
            resposta = regra.resposta
            break

    # Salva a mensagem com a resposta no banco
    mensagem = Message(
        telefone=msg.telefone,
        mensagem=msg.mensagem,
        resposta=resposta,
    )

    db.add(mensagem)
    await db.commit()
    await db.refresh(mensagem)

    return resposta
