from datetime import datetime

from sqlalchemy import Integer, String, Boolean, Float

from config.database import db


class BadRecord(db.Model):
    """
        This is a base user Model
        """
    __tablename__ = 'bad_records'

    id = db.Column(Integer, primary_key=True)
    merchant_identifier = db.Column(String(100), nullable=False, index=True)
    reason = db.Column(String(100), nullable=False)
    fullname = db.Column(String(255), nullable=False, index=True)
    card_type = db.Column(String(100), nullable=False)
    amount = db.Column(Float(), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now(), onupdate=datetime.now())

    def __init__(self, merchant_identifier, reason, fullname, card_type, amount):
        self.merchant_identifier = merchant_identifier
        self.reason = reason
        self.card_type = card_type
        self.fullname = fullname
        self.amount = amount

    def __repr__(self):
        return "<BadRecord(id='{}', merchant_identifier='{}', card_type='{}', reason='{}', amount='{}', fullname='{}'>".format(
            self.id,
            self.merchant_identifier,
            self.card_type,
            self.reason,
            self.amount,
            self.fullname)

    def to_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
