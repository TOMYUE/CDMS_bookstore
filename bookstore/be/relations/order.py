from sqlalchemy import Column, Integer, String, Text, Date, PrimaryKeyConstraint, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from .store import Store
from .user import Buyer
from .init import Base


class Order(Base):
    """
    The Order relation object including six attributes.
    oid: the id of the orders
    uid: the id of the buyers
    sid: the id of the stores
    order_time: timestamp of the order
    status: status of the order, including four status: __, __, __, __
    money: the total amount of the order
    """

    # relation name
    __tablename__ = 'Order'

    # attributes
    oid = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=True)
    uid = Column(Integer, ForeignKey(Buyer.uid))
    sid = Column(Integer, ForeignKey(Store.sid))
    order_time = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)

def create_table():
    Base.metadata.create_all()