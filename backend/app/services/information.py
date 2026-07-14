from sqlalchemy.orm import Session

from app.models.source import Information


def list_information(
    db: Session,
    skip: int = 0,
    limit: int = 20,
    source_id: int | None = None,
    keyword: str | None = None,
) -> tuple[list[Information], int]:
    query = db.query(Information)

    if source_id is not None:
        query = query.filter(Information.source_id == source_id)

    if keyword:
        pattern = f"%{keyword.strip()}%"
        query = query.filter(Information.title.ilike(pattern))

    query = query.order_by(Information.collected_at.desc())
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return items, total
