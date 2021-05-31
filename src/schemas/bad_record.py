from marshmallow_sqlalchemy import SQLAlchemySchema, auto_field

from src.models.bad_record import BadRecord


class BadRecordSchema(SQLAlchemySchema):
    class Meta:
        model = BadRecord
        include_relationships = True
        load_instance = True

    id = auto_field()
    merchant_identifier = auto_field()
    reason = auto_field()
    created_at = auto_field()
    updated_at = auto_field()
