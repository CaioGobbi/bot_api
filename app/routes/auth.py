from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin
from app.core.security import hash_senha, verificar_senha, criar_token
from app.database import get_db
from fastapi.security import OAuth2PasswordRequestForm
from app.core import security
from fastapi import Depends
from app.core.security import oauth2_scheme
from app.core.security import verificar_token
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

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
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not security.verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = security.criar_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.post("/token")
async def login_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()

    if not user or not security.verificar_senha(form_data.password, user.senha_hash):
        raise HTTPException(status_code=400, detail="Credenciais inválidas")

    token = security.criar_token({"sub": user.email})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/protegido")
async def rota_protegida(token: str = Depends(oauth2_scheme)):
    email = security.verificar_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido")
    return {"mensagem": "Autenticado como", "email": email}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    email = verificar_token(token)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido ou expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return email