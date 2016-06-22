import os
import sys
from sqlalchemy import create_engine, Column, String, Integer, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Contact(Base):
    __tablename__ = 'contact'
    id = Column(Integer, primary_key=True)
    first_name = Column(String(32))
    last_name = Column(String(32))
    last_name = Column(String(32))
    phone = Column(String(32))
    email = Column(String(64))


class Business(Base):
    __tablename__ = 'business'
    id = Column(Integer, primary_key=True)
    name = Column(String(128), nullable=False)
    mailing_address = Column(String(256))
    physical_address = Column(String(256))
    website = Column(String(64))
    contact_id = Column(Integer, ForeignKey('contact.id'))
    contact = relationship(Contact, foreign_keys=[contact_id])


if __name__ == '__main__':
    engine = create_engine('sqlite:///businesses.db')
    Base.metadata.create_all(engine)
