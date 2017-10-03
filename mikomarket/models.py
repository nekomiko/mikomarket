# import sys
from sqlalchemy import Column, \
    Integer, String
from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker
import json

Base = declarative_base()


class Product(Base):
    __tablename__ = "product"
    name = Column(String(100), nullable=False)
    id = Column(Integer, primary_key=True)
    spec_list = Column(String(500))
    price = Column(Integer)

    def __repr__(self):
        return "<Product '{}'>".format(self.name)

    def get_spec_list(self):
        return json.loads(self.spec_list)

    def get_price_print(self):
        return "{} {}".format(self.price // 1000, str(self.price % 1000).rjust(3, "0"))


# def get_products(session):
#    return session.query(Product).all()
