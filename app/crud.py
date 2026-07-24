from sqlalchemy.orm import Session

from app.models import URL
from app.schemas import URLCreate


def create_url(
    db: Session,
    url: URLCreate
):

    new_url = URL(
        original_url=url.original_url,
        short_code=url.short_code
    )

    db.add(new_url)
    db.commit()
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