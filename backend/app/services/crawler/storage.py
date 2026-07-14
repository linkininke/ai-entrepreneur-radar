from datetime import datetime

from sqlalchemy.orm import Session

from app.models.source import Information, Source


def get_or_create_source(
    db: Session,
    *,
    name: str,
    source_type: str,
    url: str,
    enabled: bool = True,
) -> Source:
    source = db.query(Source).filter(Source.name == name).first()
    if source:
        return source

    source = Source(
        name=name,
        source_type=source_type,
        url=url,
        enabled=enabled,
    )
    db.add(source)
    db.commit()
    db.refresh(source)
    return source


def upsert_information(
    db: Session,
    *,
    source: Source,
    external_id: str,
    title: str,
    url: str | None = None,
    summary: str | None = None,
    content: str | None = None,
    published_at: datetime | None = None,
    raw_data: dict | None = None,
) -> str:
    existing = (
        db.query(Information)
        .filter(
            Information.source_id == source.id,
            Information.external_id == external_id,
        )
        .first()
    )

    payload = {
        "source_id": source.id,
        "external_id": external_id,
        "title": title,
        "url": url,
        "summary": summary,
        "content": content,
        "published_at": published_at,
        "raw_data": raw_data,
    }

    if existing:
        for key, value in payload.items():
            setattr(existing, key, value)
        return "updated"

    db.add(Information(**payload))
    return "created"
