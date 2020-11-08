from typing import Optional

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from . import models


SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"
# SQLALCHEMY_DATABASE_URL = "postgresql://user:password@postgresserver/db"
# TODO: make selection using environment vars

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
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