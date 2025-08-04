from sqlalchemy import Column, Integer, String
from app.database import Base

class Rule(Base):
    __tablename__ = "rules"
    id = Column(Integer, primary_key=True, index=True)
    palavra_chave = Column(String, unique=True, index=True)
    resposta = Column(String)