from typing import Optional, List
from os import getenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from . import models


db_ip = getenv("DATABASE_IP")
if db_ip:
    SQLALCHEMY_DATABASE_URL = db_ip
else:
    SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# temporary, for testing
def initBase(db: Session):
    engine = db.get_bind()
    try:
        models.CardModel.__table__.drop(engine)
    except:
        pass
    models.CardModel.__table__.create(engine)
    db_cards = [models.CardModel(
        id = 0,
        title = "A card",
        series = "Cardos",
        manufacturer = "Buraz Ltd.",
        serial_num = None,
    ),
    models.CardModel(
        id = 1,
        title = "Another card",
        series = "Cardos",
        manufacturer = "Buraz Ltd.",
        serial_num = None,
    ),
    models.CardModel(
        id = 2,
        title = "Superfastinsanekebab",
        series = "Čokolešnik",
        manufacturer = "A",
        serial_num = None,
    )]
    db.add_all(db_cards)
    db.commit()
    db.close()



def get_card_by_id(db: Session, cid: int) -> Optional[models.Card]:
    card = db.query(models.CardModel).filter(models.CardModel.id == cid).first()
    if card:
        return models.Card(**card.__dict__)
    return None


def get_all_cards(db: Session) -> List[models.Card]:
    return [models.Card(**card.__dict__) for card in db.query(models.CardModel).all()]
