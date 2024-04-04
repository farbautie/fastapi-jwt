from sqlalchemy import create_engine
from sqlalchemy import Integer, String
from sqlalchemy.orm import sessionmaker, mapped_column
from sqlalchemy.orm import DeclarativeBase, Mapped

engine = create_engine('sqlite:///database.db')
Session = sessionmaker(engine)

def get_database():
    db = Session()
    try:
        yield db
    finally:
        db.close()
        
class Base(DeclarativeBase):
    __abstract__ = True
    
    id: Mapped[int] = mapped_column(Integer(), primary_key=True, autoincrement=True)
    
class User(Base):
    __tablename__ = 'users'
    
    username: Mapped[str] = mapped_column(String(55), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(100), nullable=False)
    
