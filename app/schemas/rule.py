from pydantic import BaseModel

class RuleCreate(BaseModel):
    palavra_chave: str
    resposta: str
