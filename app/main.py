from fastapi import FastAPI
from fastapi import Depends

from sqlalchemy.orm import Session

from app.database import engine
from app.database import get_db

from app.models import Base

from app.schemas import URLCreate

from app.crud import create_url

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Hello Docker FastAPI"
    }


@app.post("/urls")
def create(
    url: URLCreate,
    db: Session = Depends(get_db)
):

    return create_url(db, url)