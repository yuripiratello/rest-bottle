# coding: utf-8
import json
from bottle import response, request
import bottle
import requests
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
engine = create_engine('sqlite:///:memory:', echo=True)

app = bottle.Bottle()
plugin = sqlalchemy.Plugin(engine, Base.metadata, keyword='db', create=True,
                           commit=True, use_kwargs=False)

app.install(plugin)


class Person(Base):
    __tablename__ = 'person'
    id_person = Column(Integer, Sequence('id_seq'), primary_key=True)
    name = Column(String(50))
    username = Column(String(50))
    gender = Column(String(10))
    facebook_id = Column(Integer)

    def __init__(self, facebook_id):
        self.facebook_id = facebook_id

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.get('/person')
def show(db):
    facebookId = request.GET.get('facebookId', None)
    if facebookId:
        entity = db.query(Person).filter_by(facebook_id=facebookId).first()
        if entity:
            response.content_type = 'application/json'
            return json.dumps(entity.as_dict())
        else:
            return bottle.HTTPError('404', 'Person not found')
    response.content_type = 'application/json'
    entities = db.query(Person)
    if request.GET.get('limit', None):
        entities = entities.limit(int(request.GET.get('limit', None)))
    response.status = 200
    return json.dumps([e.as_dict() for e in entities.all()])


@app.post('/person')
def new_person(db):
    facebookId = request.POST.get('facebookId', None)
    if not facebookId:
        return bottle.HTTPError('404', 'Parameters not found')
    entity = db.query(Person).filter_by(facebook_id=facebookId).first()
    if entity:
        return bottle.HTTPError('409', 'Person already exists')
    rqf = requests.get('https://graph.facebook.com/{}'.format(facebookId))
    user_face = json.loads(rqf.text)
    entity = Person(facebookId)
    entity.name = user_face.get('name')
    entity.username = user_face.get('username')
    entity.gender = user_face.get('gender')
    db.add(entity)
    response.status = 201
    return 'HTTP 201'


bottle.debug(True)
bottle.run(app, host='localhost', port=8388, reloader=True, debug=True)