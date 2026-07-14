from sqlalchemy.orm import Session

from app.models.source import Information


def list_information(db: Session, skip: int = 0, limit: int = 20) -> tuple[list[Information], int]:
    query = db.query(Information).order_by(Information.collected_at.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total
