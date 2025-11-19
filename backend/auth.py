from datetime import datetime, timedelta
from typing import Optional
import os

from fastapi import APIRouter, Depends, HTTPException, status, Response, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

# local imports
from database import get_db
from users.crud import UserCRUD

router = APIRouter()

# Configuration (use env vars in production)
SECRET_KEY = os.environ.get("SECRET_KEY", "CHANGE_THIS_SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES", 60 * 24))

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/users/login")


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    payload = decode_token(token)
    user_id = payload.get("sub")
    if user_id is None:
        raise HTTPException(status_code=401, detail="Invalid token payload")
    user = UserCRUD.get_by_id(db, int(user_id))
    if user is None:
        raise HTTPException(status_code=401, detail="User not found")
    return user


# Optional: keep cookie-based simple endpoints under /auth for apps that prefer cookies
@router.post("/login")
def cookie_login(response: Response, data: dict):
    # Placeholder login — prefer using /users/login which returns JSON token
    email = data.get("email")
    password = data.get("password")
    # For now keep a simple check; replace with DB auth if desired
    if email != "admin@test.com" or password != "123":
        raise HTTPException(status_code=401, detail="Identifiants invalides")

    token = create_access_token({"sub": email}, expires_delta=timedelta(hours=2))
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=2 * 3600,
    )
    return {"message": "Connexion réussie"}


@router.get("/me")
def me(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        raise HTTPException(status_code=401, detail="Non authentifié")
    payload = decode_token(token)
    return {"sub": payload.get("sub")}


@router.post("/logout")
def logout(response: Response):
    response.delete_cookie("access_token")
    return {"message": "Déconnecté"}
