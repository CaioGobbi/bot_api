from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from app.core.security import verificar_token

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

def usuario_autenticado(token: str = Depends(oauth2_scheme)):
    email = verificar_token(token)
    if not email:
        raise HTTPException(status_code=401, detail="Token inválido ou expirado.")
    return email
