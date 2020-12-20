# pylint: disable=no-name-in-module

from datetime import datetime, timedelta
from typing import Optional, List
from os import getenv

from fastapi import Depends, FastAPI, Form, HTTPException, Path, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from sqlalchemy.orm import Session

from . import models, database


SECRET_KEY = getenv("OAUTH_SIGN_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

if (SECRET_KEY == None):
    print("Please define OAuth signing key!")
    exit(-1)

# fastAPI dependecy magic
def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

# init testing DB
# database.initBase(database.SessionLocal())

if (getenv("OAUTH_TOKEN_PROVIDER") == None):
    print("Please provide token provider URL!")
    exit(-1)

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = getenv("OAUTH_TOKEN_PROVIDER") + "/tokens")

app = FastAPI()



async def get_current_user_from_token(token: str = Depends(oauth2_scheme)) -> int:
    credentials_exception = HTTPException(
        status_code = status.HTTP_401_UNAUTHORIZED,
        detail = "Could not validate credentials",
        headers = {"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        uid: Optional[int] = int(payload.get("sub"))
        if uid is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    return uid



@app.get("/v1/cards", response_model = List[models.Card])
async def return_all_cards(current_user: int = Depends(get_current_user_from_token),
    db: Session = Depends(get_db)):
    return database.get_all_cards(db)


@app.get("/v1/cards/noauth", response_model = List[models.Card])
async def return_all_cards_noauth(db: Session = Depends(get_db)):
    return database.get_all_cards(db)


@app.get("/v1/cards/{card_id}", response_model = models.Card)
async def return_specific_card(current_user: int = Depends(get_current_user_from_token),
    card_id: int = Path(...),
    db: Session = Depends(get_db)):
    ret = database.get_card_by_id(db, card_id)
    if (ret == None):
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = "Card with given ID not found",
        )
    return ret


@app.get("/health/live", response_model = str)
async def liveness_check():
    return "OK"


@app.get("/health/ready", response_model = str)
async def readiness_check():
    return "OK"  # TODO: čekiranje baze or sth?
