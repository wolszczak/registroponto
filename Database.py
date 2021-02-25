
from sqlalchemy import create_engine, desc
from sqlalchemy.orm import sessionmaker
from DBClasses_sqlite import Registro, engine

DBSession = sessionmaker(bind=engine)


def insert(nome, data):
    session = DBSession()
    r = Registro(nome=nome, data=data)
    session.add(r)
    session.commit()
    return r.id


def list():
    session = DBSession()
    registros = session.query(Registro).order_by(Registro.data.desc()).all()
    session.close()
    return registros


def isNullOrEmpty(item):
    if item == None or item == "":
        return True
    else:
        return False
