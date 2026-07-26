from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException

from sqlalchemy.orm import Session

from app.database import engine
from app.database import get_db

from app.models import Base

from app.schemas import URLCreate

from app.crud import create_url
from app.crud import get_urls
from app.crud import get_url
from app.crud import delete_url

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


@app.get("/urls")
def read_urls(
    db: Session = Depends(get_db)
):

    return get_urls(db)


@app.get("/urls/{url_id}")
def read_url(
    url_id: int,
    db: Session = Depends(get_db)
):

    url = get_url(
        db,
        url_id
    )

    if url is None:

        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    return url

@app.delete("/urls/{url_id}")
def remove_url(
    url_id: int,
    db: Session = Depends(get_db)
):

    url = delete_url(
        db,
        url_id
    )

    if url is None:

        raise HTTPException(
            status_code=404,
            detail="URL not found"
        )

    return {
        "message": "URL deleted successfully"
    }