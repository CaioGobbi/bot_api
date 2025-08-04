from sqlalchemy import Column, Integer, String, DateTime, func
from app.database import Base

class Message(Base):
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    telefone = Column(String, index=True)
    mensagem = Column(String)
    resposta = Column(String)
    criado_em = Column(DateTime(timezone=True), server_default=func.now())
