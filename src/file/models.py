from datetime import datetime
from sqlalchemy import TIMESTAMP, String, Table, Column, Integer, ForeignKey, Boolean, JSON


from src.auth.models import user
from src.auth.database import metadata

file = Table(
    'file',
    metadata,
    Column('id', Integer, primary_key=True),
    Column("name", String, nullable=False),
    Column("download_at", TIMESTAMP, default=datetime.utcnow),
    Column("data", JSON, nullable=False),
    Column("user_id", Integer, ForeignKey(user.c.id)),
    Column("path", String, nullable=False)
)