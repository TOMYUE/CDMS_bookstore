import re
import jieba
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, Integer, ForeignKey, create_engine
from sqlalchemy.orm import sessionmaker
import sqlite3 as sqlite
import random
import base64
import jieba.analyse

Base = declarative_base()
SQLALCHEMY_DATABASE_URL = "postgresql://stu10205501402:" \
                          "Stu10205501402@dase-cdms-2022-pub.pg.rds.aliyuncs.com:5432/stu10205501402"

# initialization
engine = create_engine(SQLALCHEMY_DATABASE_URL,
    echo=True,
    pool_size=8,
    pool_recycle=60*30
)
# connect to local database
DBSession = sessionmaker(autocommit=False, autoflush=False, bind=engine)

session = DBSession()


class Book4Search(Base):
    __tablename__ = 'book'
    book_id = Column(String(128), primary_key=True)
    title = Column(String, nullable=False)
    author = Column(String)
    publisher = Column(String)
    original_title = Column(String)
    translator = Column(String)
    pub_year = Column(String)
    pages = Column(Integer)
    original_price = Column(Integer)
    currency_unit = Column(String)
    binding = Column(String)
    isbn = Column(String)
    author_intro = Column(String)
    book_intro = Column(String)
    content = Column(String)
    tags = Column(String)
    picture = Column(String)


class Search_title(Base):
    __tablename__ = 'search_title'
    search_id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)

class Search_tags(Base):
    __tablename__ = 'search_tags'
    search_id = Column(Integer, primary_key=True, nullable=False)
    tags = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


class Search_author(Base):
    __tablename__ = 'search_author'
    search_id = Column(Integer, primary_key=True, nullable=False)
    author = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


class Search_book_intro(Base):
    __tablename__ = 'search_book_intro'
    search_id = Column(Integer, primary_key=True, nullable=False)
    book_intro = Column(String, primary_key=True, nullable=False)
    book_id = Column(String(128), ForeignKey('book.book_id'), nullable=False)


class Bookinit:
    id: str
    title: str
    author: str
    publisher: str
    original_title: str
    translator: str
    pub_year: str
    pages: int
    price: int
    binding: str
    isbn: str
    author_intro: str
    book_intro: str
    content: str
    tags: [str]
    pictures: [bytes]

    def __init__(self):
        self.tags = []
        self.pictures = []


class BookDB:
    def __init__(self):
        self.db_s = "book.db"
        self.book_db = self.db_s

    def get_book_count(self):
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT count(id) FROM book")
        row = cursor.fetchone()
        return row[0]

    def get_book_info(self, start, size) -> [Book4Search]:
        books = []
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT id, title, author, "
            "publisher, original_title, "
            "translator, pub_year, pages, "
            "price, currency_unit, binding, "
            "isbn, author_intro, book_intro, "
            "content, tags, picture FROM book ORDER BY id "
            "LIMIT ? OFFSET ?", (size, start))
        for row in cursor:
            book = Bookinit()
            book.id = row[0]
            book.title = row[1]
            book.author = row[2]
            book.publisher = row[3]
            book.original_title = row[4]
            book.translator = row[5]
            book.pub_year = row[6]
            book.pages = row[7]
            book.price = row[8]
            book.currency_unit = row[9]
            book.binding = row[10]
            book.isbn = row[11]
            book.author_intro = row[12]
            book.book_intro = row[13]
            book.content = row[14]
            tags = row[15]
            picture = row[16]

            for tag in tags.split("\n"):
                if tag.strip() != "":
                    book.tags.append(tag)
            for i in range(0, random.randint(0, 9)):
                if picture is not None:
                    encode_str = base64.b64encode(picture).decode('utf-8')
                    book.pictures.append(encode_str)
            books.append(book)
        return books

    def send_info_to_db(self, start, size):
        DBSession = sessionmaker(bind=engine)
        session = DBSession()
        conn = sqlite.connect(self.book_db)
        cursor = conn.execute(
            "SELECT id, title, author, "
            "publisher, original_title, "
            "translator, pub_year, pages, "
            "price, currency_unit, binding, "
            "isbn, author_intro, book_intro, "
            "content, tags, picture FROM book ORDER BY id "
            "LIMIT ? OFFSET ?", (size, start))
        for row in cursor:
            book = Book4Search()
            book.book_id = row[0]
            book.title = row[1]
            book.author = row[2]
            book.publisher = row[3]
            book.original_title = row[4]
            book.translator = row[5]
            book.pub_year = row[6]
            book.pages = row[7]
            book.original_price = row[8]
            book.currency_unit = row[9]
            book.binding = row[10]
            book.isbn = row[11]
            book.author_intro = row[12]
            book.book_intro = row[13]
            book.content = row[14]
            tags = row[15]
            picture = row[16]
            thelist = []
            for tag in tags.split("\n"):
                if tag.strip() != "":
                    thelist.append(tag)
            book.tags = str(thelist)
            book.picture = None
            if picture is not None:
                book.picture = picture

            session.add(book)
        session.commit()
        # 关闭session
        session.close()

    def send_info(self):
        bookdb.send_info_to_db(0, bookdb.get_book_count())


def insert_tags():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    row = session.execute("SELECT book_id,tags FROM book;").fetchall()
    m = 0
    for i in row[1:]:
        tmp = i.tags.replace("'", "").replace("[", "").replace("]",
                                                               "").split(", ")
        for j in tmp:
            session.execute(
                "INSERT into search_tags(search_id, tags, book_id) VALUES (%d, '%s', %d)"
                % (m, j, int(i.book_id)))
            m = m + 1
    session.commit()


def insert_author():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    row = session.execute("SELECT book_id, author FROM book;").fetchall()
    m = 0
    for i in row:
        tmp = i.author
        if tmp == None:
            j = '作者不详'
            session.execute(
                "INSERT into search_author(search_id, author, book_id) VALUES (%d, '%s', %d)"
                % (m, j, int(i.book_id)))
            m = m + 1
        else:
            tmp = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', tmp)
            tmp = re.sub(r'[^\w\s]', '', tmp)
            length = len(tmp)
            for k in range(1, length + 1):
                if tmp[k - 1] == '':
                    continue
                j = tmp[:k]
                session.execute(
                    "INSERT into search_author(search_id, author, book_id) VALUES (%d, '%s', %d)"
                    % (m, j, int(i.book_id)))
                m = m + 1
    session.commit()


def insert_title():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    row = session.execute("SELECT book_id, title FROM book;").fetchall()
    m = 0
    for i in row:
        tmp = i.title
        # print(tmp)
        tmp = re.sub(r'[\(\[\{（【][^)）】]*[\)\]\{\】\）]\s?', '', tmp)
        tmp = re.sub(r'[^\w\s]', '', tmp)
        # 处理空标题
        if len(tmp) == 0:
            continue
        seg_list = jieba.cut_for_search(tmp)
        sig_list = []
        tag = 0
        for k in seg_list:
            sig_list.append(k)
            if k == tmp:
                tag = 1
        if tag == 0:
            sig_list.append(tmp)

        for j in sig_list:
            if j == "" or j == " ":
                continue
            session.execute(
                "INSERT into search_title(search_id, title, book_id) VALUES (%d, '%s', %d)"
                % (m, j, int(i.book_id)))
            m = m + 1
    session.commit()


def insert_book_intro():
    DBSession = sessionmaker(bind=engine)
    session = DBSession()
    row = session.execute("SELECT book_id, book_intro FROM book;").fetchall()
    m = 0
    for i in row:
        tmp = i.book_intro
        if tmp != None:
            keywords_textrank = jieba.analyse.textrank(tmp)
            # print(keywords_textrank)
            # keywords_tfidf = jieba.analyse.extract_tags(tmp)
            # print(keywords_tfidf)
            for j in keywords_textrank:
                session.execute(
                    "INSERT into search_book_intro(search_id, book_intro, book_id) VALUES (%d, '%s', %d)"
                    % (m, j, int(i.book_id)))
                m = m + 1
    session.commit()


def init_db():
    Base.metadata.create_all(engine)


def drop_db():
    Base.metadata.drop_all(engine)



if __name__ == "__main__":
    drop_db()
    init_db()
    bookdb = BookDB()
    bookdb.send_info()
    insert_tags()
    insert_author()
    insert_title()
    insert_book_intro()