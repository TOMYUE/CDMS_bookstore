import sqlalchemy
from sqlalchemy import Column, Integer, String, Text, Date, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .init import Base, engine


class Buyer(Base):
    """
    The buyer relation object including five attributes.

    uid: the identifier id of the buyers, primary key
    uname: the name of the buyers
    pwd: the password of the buyers
    account: the account of the buyers' bank or other account using for deals
    balance: the total balance of the buyers account
    """

    # relation name
    __tablename__ = 'Buyer'

    # attributes
    uid = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=True)
    uname = Column(String)
    pwd = Column(String)
    account = Column(String)
    balance = Column(Integer)


class Seller(Base):
    """
    The seller relation object including six attributes

    uid: the id of the salers, primary key
    sid: the id of the buyers' stores, foreign key
    uname: the name of the buyers
    pwd: the password of the buyers
    account: the account of the buyers' bank or other account using for deals
    balance: the total balance of the buyers account
    """

    # relation name
    __tablename__ = 'Seller'

    # attributes
    uid = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=True)
    uname = Column(String)
    pwd = Column(String)
    account = Column(String)
    balance = Column(Integer)
