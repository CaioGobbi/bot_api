from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import get_db
from app.models.rule import Rule
from app.schemas.rule import RuleCreate

router = APIRouter(prefix="/api/regras", tags=["Regras"])

@router.post("/")
async def criar_regra(rule: RuleCreate, db: AsyncSession = Depends(get_db)):
    # Verificar se já existe uma regra com essa palavra
    result = await db.execute(select(Rule).where(Rule.palavra_chave == rule.palavra_chave))
    regra_existente = result.scalars().first()

    if regra_existente:
        raise HTTPException(status_code=400, detail="Regra já existe")

    nova_regra = Rule(palavra_chave=rule.palavra_chave.lower(), resposta=rule.resposta)
    db.add(nova_regra)
    await db.commit()
    return {"msg": "Regra criada com sucesso!"}
