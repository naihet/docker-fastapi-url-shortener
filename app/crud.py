from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.models import URL
from app.schemas import URLCreate
from app.utils import generate_short_code

def create_url(
    db: Session,
    url: URLCreate
):

    new_url = URL(
        original_url=url.original_url,
        short_code=generate_short_code()
    )

    db.add(new_url)

    try:

        db.commit()

    except IntegrityError:

        db.rollback()

        raise

    db.refresh(new_url)

    return new_url


def get_urls(
    db: Session
):

    return db.query(URL).all()


def get_url(
    db: Session,
    url_id: int
):

    return (
        db.query(URL)
        .filter(URL.id == url_id)
        .first()
    )

def delete_url(
    db: Session,
    url_id: int
):

    url = (
        db.query(URL)
        .filter(URL.id == url_id)
        .first()
    )

    if url is None:
        return None

    db.delete(url)

    db.commit()

    return url

def get_url_by_code(
    db: Session,
    short_code: str
):

    return (
        db.query(URL)
        .filter(URL.short_code == short_code)
        .first()
    )

def increment_click(
    db: Session,
    url: URL
):

    url.clicks += 1

    db.commit()

    db.refresh(url)

    return url