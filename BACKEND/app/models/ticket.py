from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from models.database import Base

class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    tg_user_id = Column(Integer, ForeignKey('tg_user_id.id')) # !
    issue_id = Column(String, nullable=False)
    issue_type = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    status = Column(String, default='open')
    created_at = Column(DateTime, default=datetime.now)

    user = relationship('User', backref='tickets')

