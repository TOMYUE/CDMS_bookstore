from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData, Table, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


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
session = DBSession()
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
    uid = Column(Integer, autoincrement=True, primary_key=True, unique=True, nullable=False)
    uname = Column(String, nullable=False)
    pwd = Column(String, nullable=False)
    account = Column(String, nullable=False)
    balance = Column(Integer, nullable=False)


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
    uid = Column(Integer, ForeignKey(Seller.uid), nullable=False)
    bid = Column(String,  primary_key=True, unique=True, nullable=False)
    inventory_quantity = Column(Integer, nullable=False)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)                      # can have no author
    publisher = Column(String, nullable=False)
    original_title = Column(String, nullable=True)              # can have no origin title
    translator = Column(String, nullable=True)                  # can have no translator
    pub_year = Column(String, nullable=False)
    pages = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    currency_unit = Column(String, nullable=False)
    binding = Column(String, nullable=False)
    isbn = Column(String, unique=True, nullable=False)
    author_intro = Column(String, nullable=True)                # can have no intro
    book_intro = Column(String, nullable=True)                  # can have no intro
    content = Column(String, nullable=True)                     # can have no content
    tags = Column(String, nullable=True)                        # can have no tag


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
    sid = Column(Integer, ForeignKey(Store.sid))
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
    bid = Column(String, ForeignKey(Store.bid))
    num = Column(Integer, nullable=False)


class StoreOwner(Base):
    """
    The store and owner relation contain two attributes
    """

    # relation name
    __tablename__ = 'StoreOwner'
    __table_args__ = {'extend_existing': True}

    # attribute name
    id = Column(Integer, autoincrement=True, primary_key=True, unique=True)
    sid = Column(Integer, ForeignKey(Store.sid))
    uid = Column(Integer, ForeignKey(Seller.uid))


def db_session():
    """get db session for following operations"""
    return session


def create_table():
    """
    create all the relations
    :return:
    """
    Base.metadata.create_all(engine)


def check_table_exists():
    """
    Check if all the table exists
    :return:
    """
    buyer_table = Table('Buyer', meta)
    assert insp.has_table(buyer_table) == True
    seller_table = Table('Seller', meta)
    assert insp.has_table(seller_table) == True
    store_table = Table('Store', meta)
    assert insp.has_table(store_table) == True
    deal_table = Table('Deal', meta)
    assert insp.has_table(deal_table) == True
    deal_book_table = Table('DealBook', meta)
    assert insp.has_table(deal_book_table) == True
    store_owner_table = Table('StoreOwner', meta)
    assert insp.has_table(store_owner_table) == True


def drop_all_table():
    """
    Remove all exists table
    :return:
    """
    rm_sql = '''
    DROP TABLE IF EXISTS Buyer CASCADE ;
    DROP TABLE IF EXISTS Seller CASCADE ;
    DROP TABLE IF EXISTS Store CASCADE ;
    DROP TABLE IF EXISTS Deal CASCADE ;
    DROP TABLE IF EXISTS DealBook CASCADE ;
    DROP TABLE IF EXISTS StoreOwner CASCADE ;
    '''
    engine.execute(rm_sql)


create_table()
# drop_all_table()
check_table_exists()