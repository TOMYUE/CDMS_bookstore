from sqlalchemy import Column, Integer, String, ForeignKey
from .user import Seller
from .init import Base


class Store(Base):
    """
    The Order relation object including nineteen attributes.

    sid: the id of the store
    uid: the owner id of the store
    bid: the id of the book
    inventory_quantity: the inventory quantity of the book in the sid store,
                        -1 means it has been removed from the shelves

    title,author,publisher,original_title,translator,pub_year,pages,
    price,currency_unit,isbn,author_intro,book_intro,content,tags
    """

    # relation name
    __tablename__ = 'Store'

    # attributes
    sid = Column(Integer, primary_key=True, unique=True)
    uid = Column(Integer, ForeignKey(Seller.uid))
    bid = Column(String,  primary_key=True, unique=True, nullable=False)
    inventory_quantity = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    author = Column(String)
    publisher = Column(String, nullable=True)
    original_title = Column(String)
    translator = Column(String)
    pub_year = Column(String, nullable=True)
    pages = Column(Integer, nullable=True)
    price = Column(Integer, nullable=True)
    currency_unit = Column(String)
    binding = Column(String)
    isbn = Column(String, unique=True)
    author_intro = Column(String)
    book_intro = Column(String)
    content = Column(String)
    tags = Column(String)


class StoreOwner(Base):
    """
    The store and onwer relation contain two attributes
    """

    sid = Column(Integer, ForeignKey(Store.sid))
    uid = Column(Integer, ForeignKey(Seller.uid))