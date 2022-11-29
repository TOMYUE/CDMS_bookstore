from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy import create_engine, MetaData, inspect
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

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


class Book_bp(Base):
    """
    The book relation table
    """

    # relation name
    __tablename__ = 'Book_bp'

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


Base.metadata.create_all(engine)

with open("book.sql", "r+") as f:
    # line = f.readline()
    # engine.connect().execute(line)
    sql = f.read()
    engine.connect().execute(sql)