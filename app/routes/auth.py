from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_senha, verificar_senha, criar_token
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/register")
async def register(usuario: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == usuario.email))
    user_existente = result.scalar_one_or_none()

    if user_existente:
        raise HTTPException(status_code=400, detail="Email já registrado")

    novo_usuario = User(
        email=usuario.email,
        senha_hash=hash_senha(usuario.senha)
    )

    db.add(novo_usuario)
    await db.commit()
    return {"msg": "Usuário registrado com sucesso"}


@router.post("/login")
async def login(user_data: UserLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == user_data.email))
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=400, detail="Usuário não encontrado")

    if not verificar_senha(user_data.senha, user.senha_hash):
        raise HTTPException(status_code=400, detail="Senha incorreta")

    token = criar_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token")
async def token(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not security.verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = security.criar_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}