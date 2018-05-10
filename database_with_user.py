from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# user class
class User(Base):
    __tablename__ = 'user'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    email = Column(String(150), nullable=False)


# category class
class Category(Base):
    __tablename__ = 'category'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)


# Items Class
class Items(Base):
    __tablename__ = 'items'
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    description = Column(String(250))
    price = Column(String(10), nullable=False)
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship(Category)
    user_id = Column(Integer, ForeignKey('user.id'))
    user = relationship(User)

    @property
    def serialize(self):
        return {
            'name': self.name,
            'id': self.category_id,
            'description': self.description,
            'price': self.price,
            'category_id': self.category_id,
            'category': self.category.name
        }


# creating Database
engine = create_engine('sqlite:///itemcatalogwithUser.db')
Base.metadata.create_all(engine)
