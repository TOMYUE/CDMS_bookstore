from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from be.model.error import *

# SQLALCHEMY_DATABASE_URL = "postgresql://postgres:123456@localhost:5432/tangyue"
SQLALCHEMY_DATABASE_URL = "postgresql://stu10205501461:" \
                          "Stu10205501461@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501461"

# initialization
engine = create_engine(SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=8,
    pool_recycle=60*30
)
# connect to local database
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# create declarative_base instance
Base = declarative_base()
# create a metadata object
meta = MetaData()
# create inspector
insp = inspect(engine)


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
    uid = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    uname = Column(String, nullable=False)
    pwd = Column(String, nullable=False)
    account = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    terminal = Column(String, nullable=False)


class Seller(Base):
    """
    The seller relation object including six attributes

    uid: the id of the sellers, primary key
    sid: the id of the sellers' stores, foreign key
    uname: the name of the sellersx
    pwd: the password of the sellers
    account: the account of the sellers' bank or other account using for deals
    balance: the total balance of the sellers account
    """

    # relation name
    __tablename__ = 'Seller'

    # attributes
    uid = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    uname = Column(String, nullable=False)
    pwd = Column(String, nullable=False)
    account = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)
    token = Column(String, nullable=False)
    terminal = Column(String, nullable=False)


class StoreOwner(Base):
    """
    The store and owner relation contain two attributes
    """

    # relation name
    __tablename__ = 'StoreOwner'
    __table_args__ = {'extend_existing': True}

    # attribute name
    sid = Column(Integer, primary_key=True, unique=True)
    uid = Column(Integer, ForeignKey(Seller.uid))


class Book(Base):
    """
    The book relation table
    """

    # relation name
    __tablename__ = 'Book'

    #attribute name
    bid = Column(String, primary_key=True, unique=True, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)  # can have no author
    publisher = Column(String, nullable=False)
    original_title = Column(String, nullable=True)  # can have no origin title
    translator = Column(String, nullable=True)  # can have no translator
    pub_year = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    currency_unit = Column(String, nullable=False)
    binding = Column(String, nullable=False)
    isbn = Column(String, nullable=False)
    author_intro = Column(String, nullable=True)  # can have no intro
    book_intro = Column(String, nullable=True)  # can have no intro
    content = Column(String, nullable=True)  # can have no content
    tags = Column(String, nullable=True)  # can have no tag
    picture = Column(String, nullable=True)  # can have no picture


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
    sid = Column(Integer, ForeignKey(StoreOwner.sid), primary_key=True)
    uid = Column(Integer, ForeignKey(Seller.uid), nullable=False)
    bid = Column(String, ForeignKey(Book.bid))
    inventory_quantity = Column(Integer, nullable=False)
    title = Column(String, nullable=False)


class Deal(Base):
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
    __tablename__ = 'Deal'

    # attributes
    did = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=True)
    uid = Column(Integer, ForeignKey(Buyer.uid))
    sid = Column(Integer, ForeignKey(StoreOwner.sid))
    order_time = Column(String, nullable=False)
    status = Column(Integer, nullable=False)
    money = Column(Integer, nullable=False)


class DealBook(Base):
    """
    The order related books relation contain three attributes

    oid: id of the order
    bid: id of the book
    num: the num of books in this order that buyer has bought
    """

    # relation name
    __tablename__ = 'DealBook'

    # attribute name
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    did = Column(Integer, ForeignKey(Deal.did))
    sid = Column(Integer, ForeignKey(Store.sid))
    bid = Column(String, ForeignKey(Book.bid))
    num = Column(Integer, nullable=False)


def db_session():
    """get db session for following operations"""
    return DBSession()


def create_table():
    """
    create all the relations
    :return:
    """
    Base.metadata.create_all(engine)


def drop_all_table():
    """
    Remove all exists table
    """
    rm_sql = '''
    DROP TABLE IF EXISTS "Buyer" CASCADE ;
    DROP TABLE IF EXISTS "Seller" CASCADE ;
    DROP TABLE IF EXISTS "Store" CASCADE ;
    DROP TABLE IF EXISTS "Book" CASCADE ;
    DROP TABLE IF EXISTS "Deal" CASCADE ;
    DROP TABLE IF EXISTS "DealBook" CASCADE ;
    DROP TABLE IF EXISTS "StoreOwner" CASCADE ;
    '''
    with db_session() as session:
        session.execute(rm_sql)
        session.commit()


def buyer_id_exist(session, buyer_id):
    """If buyer id exists return true, else return false"""
    try:
        with session.begin():
            exists = session.query(Buyer).filter(Buyer.uid == buyer_id).first() is not None
            session.commit()
        return exists
    except Exception as e:
        return error_non_exist_user_id(buyer_id)


def book_id_exist(session, book_id):
    """if book id exists return true, else return false"""
    try:
        with session.begin():
            exists = session.query(Store.bid).filter(Store.bid == book_id).first() is not None
            session.commit()
        return exists
    except Exception as e:
        return error_non_exist_book_id(book_id)


def store_id_exist(session, store_id):
    """if store id exists return true, else return false"""
    try:
        with session.begin():
            exists = session.query(StoreOwner.sid).filter(StoreOwner.sid == store_id).first() is not None
            session.commit()
        return exists
    except Exception as e:
        return error_non_exist_store_id(store_id)


def copy_data_to_book(session):
    try:
        with session.begin():
            sql = """
               insert into "Book" (bid, title, author, publisher, original_title, translator, pub_year, pages, price, 
               currency_unit, binding, isbn, author_intro, book_intro, content, tags, picture)select * from "Book_bp"; 
            """
            session.execute(sql)
            session.commit()
    except Exception as e:
        print()


drop_all_table()
create_table()
copy_data_to_book(DBSession())
