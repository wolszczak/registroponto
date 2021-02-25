import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.sql.sqltypes import DATETIME, TIMESTAMP

Base = declarative_base()


class Registro(Base):
    __tablename__ = 'registro'
    id = Column(Integer, primary_key=True)
    nome = Column(String(250), nullable=False)
    data = Column(DATETIME, nullable=False)


engine = create_engine('sqlite:///RegistrosDB.db')
Base.metadata.create_all(engine)
