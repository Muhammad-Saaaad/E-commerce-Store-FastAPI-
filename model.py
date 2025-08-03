from sqlalchemy import Column , Integer , String , DateTime , Float , ForeignKey
from database import base
from datetime import datetime
from sqlalchemy.orm import relationship

class User(base):
    __tablename__ = 'User'

    id = Column(Integer , primary_key=True , index=True)
    username = Column(String, nullable=False)
    password= Column(String, nullable=False)

    product = relationship('Product' , back_populates='user' , cascade="all, delete-orphan") # if user deleted the foreignkey data will also deleted
    likes = relationship('Likes' , back_populates='user' , cascade="all, delete-orphan")
    cart = relationship('Shopping_Cart' , back_populates='user', cascade="all, delete-orphan")

class Product(base):
    __tablename__ = 'Product'

    id = Column(Integer , primary_key=True , index=True)
    name = Column(String , nullable=False)
    description = Column(String)
    price = Column(Float, nullable=False)
    like_count = Column(Integer)
    user_id = Column(Integer , ForeignKey('User.id'))

    user = relationship('User' , back_populates='product')
    likes = relationship('Likes' , back_populates='product' , cascade="all, delete-orphan")
    cart = relationship('Shopping_Cart' , back_populates='product', cascade="all, delete-orphan")

class Likes(base):
    __tablename__ = 'Likes'

    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer , ForeignKey('User.id'), nullable=False)
    product_id = Column(Integer , ForeignKey('Product.id'), nullable=False)

    user = relationship("User" , back_populates='likes')
    product = relationship('Product' , back_populates='likes')


class Shopping_Cart(base):
    __tablename__ = 'Shopping_Cart'

    id = Column(Integer , primary_key=True , index=True)
    user_id = Column(Integer , ForeignKey('User.id'), nullable=False)
    product_id = Column(Integer , ForeignKey('Product.id'), nullable=False)
    quantity  =Column(Integer)
    total_price = Column(Float)

    user = relationship('User' , back_populates='cart')
    product = relationship('Product' , back_populates='cart')