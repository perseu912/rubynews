# import sqlite3 as sql


# conn = sql.connect('news.)
# cursor = conn.cursor()

# cursor.execute("""
# CREATE TABLE news (
#         id INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
#         url_news TEXT,
#         title TEXT NOT NULL,
#         date TEXT,
#         time_read TEXT,
#         time INTEGER,
#         url_banner TEXT,
#         news TEXT
# );
# """)


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String

Base = declarative_base()

#Session = sessionmaker(bind=engine)
#session = Session()

engine = create_engine('sqlite:////tmp/ruby_news.db')



#nn = engine.connect()


# session.begin()





class News(Base):
        __tablename__ = 'news'

        id = Column(Integer,primary_key=True)
        url_image = Column(String(20))
        title = Column(String(40),unique=True, nullable=False)
        url_news = Column(String(40),unique=True,nullable=False)
        notice = Column(String(1024),unique=True, nullable=False)
        date = Column(String(20),unique=True, nullable=False)

        def __repr__(self):
                return f'Title news: {self.title}'




print(News.__table__)

Base.metadata.create_all(engine)


Session = sessionmaker(bind=engine)

session = Session()

news = News(title='guerra',date='06/03/2022',url_image='',url_news='',notice='eferfrf')
session.add_all([news])

print(news.id)
# print(conn.begin().commit())
#session.flush()
#session.close()

# session.flush()
# session.commit()

print(session.new)

print(session.query(News).filter_by(title='guerra').first())

session.commit()

print(news.id)