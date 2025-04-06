'''
This module defines the structure and schema of the database. 
'''

from sqlalchemy import create_engine, Column, Integer, String, ForeignKey, Text, DateTime
from sqlalchemy.orm import relationship, sessionmaker, declarative_base
import datetime

from dotenv import load_dotenv
import os
load_dotenv()


Base = declarative_base()

# User Table
class User(Base):
    __tablename__ = "users"
    user_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    role = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    # relationship: one user can upload many documents
    documents = relationship("Document", back_populates="user")


# Document Table
class Document(Base):
    __tablename__ = "documents"

    document_id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    chunk = Column(Integer, nullable=False, server_default='1')
    user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
    title = Column(String, nullable=False)
    source_type = Column(String, nullable=False) # 'document', 'audio transcription'
    topic = Column(String)
    date_uploaded = Column(DateTime, default=datetime.datetime.utcnow)
    content = Column(Text)  # This is where content or transcription text will be stored.
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    # Relationship: A document is uploaded by a user (professor or presenter)
    user = relationship('User', back_populates='documents')

    # Method to update document content progressively
    def update_content(self, new_content):
        self.content += new_content
        self.updated_at = datetime.datetime.utcnow()

'''
We will need to store user queries somewhere so we can display previous chat history.
'''
# class Query(Base):
#     __tablename__ = 'queries'

#     query_id = Column(Integer, primary_key=True)
#     user_id = Column(Integer, ForeignKey('users.user_id'), nullable=False)
#     document_id = Column(Integer, ForeignKey('documents.document_id'), nullable=False)
#     query_text = Column(Text, nullable=False)
#     timestamp = Column(DateTime, default=datetime.utcnow)
#     response = Column(Text)  # The chatbot's response to the query
#     relevant_document_ids = Column(Text)  # A list of relevant document IDs related to the query

#     # Relationship: A query is associated with a user and a document
#     user = relationship('User')
#     document = relationship('Document', back_populates='queries')


# Creating a Database Engine
DATABASE_URL = os.getenv("DATABASE_URL")
engine = create_engine(DATABASE_URL)

# Create Tables
Base.metadata.create_all(engine)

# Create a Session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)