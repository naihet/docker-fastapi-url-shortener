from fastapi import FastAPI
from fastapi import Depends
from fastapi import HTTPException
from fastapi.responses import RedirectResponse

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database import engine
from app.database import get_db

from app.models import Base

from app.schemas import URLCreate
from app.schemas import URLResponse

from app.crud import create_url
from app.crud import get_urls
from app.crud import get_url
from app.crud import delete_url
from app.crud import get_url_by_code
from app.crud import increment_click

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
def home():

    return {
        "message": "Hello Docker FastAPI"
    }


@app.post("/urls", response_model=URLResponse)
def create(
    url: URLCreate,
    db: Session = Depends(get_db)
):
    try:

        return create_url(db, url)

    except IntegrityError:

        raise HTTPException(

            status_code=409,

            detail="Short code already exists"

        )

@app.get("/urls", response_model=list[URLResponse])
def read_urls(
    db: Session = Depends(get_db)
):

    return get_urls(db)


@app.get("/urls/{url_id}", response_model=URLResponse)
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


@app.get("/{short_code}")
def redirect_url(
    short_code: str,
    db: Session = Depends(get_db)
):

    url = get_url_by_code(
        db,
        short_code
    )

    if url is None:

        raise HTTPException(
            status_code=404,
            detail="Short URL not found"
        )

    increment_click(
        db,
        url
    )

    return RedirectResponse(
        url.original_url
    )