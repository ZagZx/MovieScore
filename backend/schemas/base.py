from pydantic import BaseModel, field_serializer
from datetime import datetime, timezone


class Base(BaseModel):
    @field_serializer(
        "data_criacao", "data_atualizacao", "data_adicao", 
        when_used="json-unless-none", 
        check_fields=False
    )
    def serialize_dates(self, value: datetime):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        return value.isoformat()
