

from sqlalchemy import Column, Integer, String, Boolean
from .database import Base 
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship

class Post(Base):
    __tablename__ = "posts"

    id=Column(Integer, primary_key=True, index=True,nullable=False)
    title=Column(String, index=True,nullable=False)
    content=Column(String, index=True, nullable=False)
    published= Column(Boolean, server_default='True')
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
    owner_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner=relationship("User")

   

class User(Base):
    __tablename__="users"
    id=Column(Integer, primary_key=True, index=True,nullable=False) 
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


class Vote(Base):
    __tablename__="votes"
    #composite primary key post_id and user_id
    post_id=Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)
    user_id=Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)


