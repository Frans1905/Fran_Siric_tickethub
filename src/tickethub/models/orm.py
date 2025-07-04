from sqlalchemy import Column, Integer, String, JSON, ForeignKey
from sqlalchemy.orm import relationship
from tickethub.db.db import Base


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)

    tickets = relationship('Ticket', back_populates='assignee')


class Ticket(Base):
    __tablename__ = 'tickets'

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    status = Column(String, nullable=False)
    priority = Column(String, nullable=False)
    assignee_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    raw_json = Column(JSON, nullable=False)

    assignee = relationship('User', back_populates='tickets')
