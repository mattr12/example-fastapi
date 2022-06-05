from jose import JWTError, jwt
from datetime import datetime, timedelta
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app import database, models

from . import schemas
from .config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


def create_access_token(data: dict):
    dict_to_encode = data.copy()

    expiration_time = datetime.utcnow() + timedelta(
        minutes=settings.auth_expiration_in_minutes
    )

    dict_to_encode.update({"exp": expiration_time})

    encoded_jwt = jwt.encode(
        dict_to_encode,
        settings.auth_secret_key,
        algorithm=settings.auth_algorithm_type,
    )

    return encoded_jwt


def verify_access_token(token: str, credentials_exceptions):
    try:
        payload = jwt.decode(
            token, settings.auth_secret_key, algorithms=[settings.auth_algorithm_type]
        )

        id: str = payload.get("user_id")

        if id is None:
            raise credentials_exceptions

        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credentials_exceptions

    return token_data


def get_current_user(
    token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail="Could not validate credentials.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    verified_token = verify_access_token(token, credentials_exception)

    user = db.query(models.User).filter(models.User.id == verified_token.id).first()

    return user
