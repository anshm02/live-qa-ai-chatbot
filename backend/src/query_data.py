'''
This module is responsible for query data from the relational db and to retrieve relevant documents
from the vector db
'''

from sqlalchemy import Column, Integer, String, create_engine, and_
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from pinecone import Pinecone
import os

from models import SessionLocal, User, Document


def query_specific_documents(user_id, topic):
    '''
    Query specific documents in relational db based on the vector based on the document_id

    Input: 
        - document_id(int) : document id 

    Output: 
        dict[str] : document metadata
    '''

    session = SessionLocal()
    try:
        # Build the query with filters
        query = session.query(Document)

        query = session.query(Document).filter(
            and_(
                Document.topic == topic,
                Document.user_id == user_id
            )
        ).all()


        rows_as_dicts = [
            {column.name: getattr(row, column.name) for column in row.__table__.columns}
            for row in query
        ]
    

    finally:
        session.close()

    return rows_as_dicts

def get_user_id(email):
    '''
    Finds the user ID based on the given name.
    
    Input :
        - name(str) : The name of the user.

    Output : 
        The user ID or None if no user is found.
    '''
    session = SessionLocal()
    try:
        query = session.query(User)
        
        # Build the query with filters
        user = session.query(User).filter(User.email == email).first()
    
    finally:
        session.close()
    
    return user.user_id if user else None

def search_vector_db(query_embedding):
    '''

    '''

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index('live-qa-chatbot')

    query_result = index.query(vector=[query_embedding], top_k=5) 
    return query_result['matches']


