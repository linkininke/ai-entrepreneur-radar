from sqlalchemy.orm import Session

from app.models.source import Source


def list_sources(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[Source], int]:
    query = db.query(Source).order_by(Source.created_at.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total
