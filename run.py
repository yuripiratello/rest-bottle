# coding: utf-8
import json
import logging
import bottle
import requests
from bottle import response, request
from bottle.ext import sqlalchemy
from sqlalchemy import create_engine, Column, Integer, Sequence, String
from sqlalchemy.exc import ArgumentError
from sqlalchemy.ext.declarative import declarative_base

logging.basicConfig(filename='rest.log', level=logging.INFO,
                    format='%(asctime)s %(message)s')
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
        rqf = requests.get('https://graph.facebook.com/{}'.format(facebook_id))
        user_face = json.loads(rqf.text)
        if user_face.get('error', None):
            raise ArgumentError
        self.name = user_face.get('name')
        self.username = user_face.get('username')
        self.gender = user_face.get('gender')


    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


@app.get('/person/')
@app.get('/person')
def show(db):
    logging.info('GET /person')
    facebookId = request.GET.get('facebookId', None)
    if facebookId:
        entity = db.query(Person).filter_by(facebook_id=facebookId).first()
        if entity:
            logging.info('Person found: {}'.format(entity.facebook_id))
            response.content_type = 'application/json'
            response.status = 200
            return json.dumps(entity.as_dict())
        else:
            logging.info('Person not found: {}'.format(facebookId))
            response.status = 404
            return bottle.HTTPResponse('Person not found', 404)
    response.content_type = 'application/json'
    entities = db.query(Person)
    logging.info('Get all persons')
    if request.GET.get('limit', None):
        logging.info('Get all persons with limit ({})'.format(
            request.GET.get('limit', None)))
        entities = entities.limit(int(request.GET.get('limit', None)))
    response.status = 200
    return json.dumps([e.as_dict() for e in entities.all()])


@app.post('/person/')
@app.post('/person')
def new_person(db):
    logging.info('POST /person')
    facebookId = request.POST.get('facebookId', None)
    if not facebookId:
        logging.info('Param FacebookId not found')
        response.status = 404
        return bottle.HTTPResponse('Parameters not found', 404)
    entity = db.query(Person).filter_by(facebook_id=facebookId).first()
    if entity:
        logging.info('Person already exists: {}'.format(facebookId))
        response.status = 409
        return bottle.HTTPResponse('Person already exists', 409)
    try:
        logging.info('Person created: {}'.format(facebookId))
        entity = Person(facebookId)
        db.add(entity)
        response.status = 201
    except ArgumentError:
        logging.info('Invalid facebookId: {}'.format(facebookId))
        response.status = 412
        return bottle.HTTPResponse('Invalid facebookId', 412)


@app.delete('/person/<facebook_id>/')
def delete_person(facebook_id, db):
    logging.info('DELETE /person')
    entity = db.query(Person).filter_by(facebook_id=facebook_id).first()
    if not entity:
        logging.info('Person not found: {}'.format(facebook_id))
        response.status = 404
        return bottle.HTTPResponse('Person not found', 404)
    logging.info('Deleted person: {}'.format(facebook_id))
    db.delete(entity)
    response.status = 204


if __name__ == '__main__':
    bottle.debug(True)
    bottle.run(app, host='localhost', port=8388, reloader=True, debug=True)