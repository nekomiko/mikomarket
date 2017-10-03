import os
import json

import requests
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

from .models import Base, Product


def get_script_dir():
    return os.path.dirname(os.path.realpath(__file__))


DBSession = None


def init_sessionmaker():
    global DBSession
    if DBSession is not None:
        return DBSession
    script_dir = get_script_dir()
    db_file = os.path.join(script_dir, "market.db")
    engine = create_engine("sqlite:///{}".format(db_file))

    Base.metadata.bind = engine
    DBSession = scoped_session(sessionmaker(bind=engine))
    return DBSession


def create_session():
    DBSession = init_sessionmaker()
    session = DBSession()
    return session


def init_db():
    session = create_session()
    engine = session.get_bind()
    Base.metadata.create_all(engine)
    session.close()


r_session = requests.Session()


def download_img(url: str, id: int):
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:55.0) Gecko/20100101 Firefox/55.0"
    }
    if url.startswith("//"):
        url = url.replace("//", "https://")
    path_dir = os.path.join(get_script_dir(), "static/img/full")
    try:
        os.makedirs(path_dir)
    except FileExistsError:
        pass
    path_img = os.path.join(path_dir, "{}.jpg".format(id))
    if not os.path.exists(path_img):
        response = r_session.get(url, headers=headers)
        with open(path_img, "wb") as f:
            f.write(response.content)
    url = url.replace("9hq", "5hq")
    path_dir = path_dir.replace("full", "mini")
    try:
        os.makedirs(path_dir)
    except FileExistsError:
        pass
    path_img = path_img.replace("full", "mini")
    if not os.path.exists(path_img):
        response = r_session.get(url, headers=headers)
        with open(path_img, "wb") as f:
            f.write(response.content)


def populate_db():
    def str_to_int(s):
        s2 = ''.join(list(filter(lambda c: ord(c) >= ord('0') and ord(c) <= ord('9'), s)))
        return int(s2)
    session = create_session()
    script_dir = get_script_dir()
    j_file_path = os.path.join(script_dir, "data.json")
    with open(j_file_path, "r") as j_f:
        data = json.loads(j_f.read())
    for p in data:
        pr = Product(name=p[0], spec_list=json.dumps(p[1]), price=str_to_int(p[2]))
        session.add(pr)
        session.commit()
        download_img(p[3], pr.id)


def initial_setup():
    init_db()
    populate_db()
