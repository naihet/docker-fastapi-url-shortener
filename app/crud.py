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