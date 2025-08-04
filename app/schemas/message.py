from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel


class MessageIn(BaseModel):
    telefone: str
    mensagem: str

class MessageOut(BaseModel):
    id: int
    telefone: str
    mensagem: str
    resposta: str
    criado_em: datetime

    model_config = {
    "from_attributes": True
}

class IncomingMessage(BaseModel):
    telefone: str
    mensagem: str