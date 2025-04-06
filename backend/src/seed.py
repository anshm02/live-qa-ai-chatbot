"""
This module is response for inserting data into database. 
"""

from models import SessionLocal, User, Document
from data_processing import extract_document_content


def add_user(name, email, role): 
    '''
    Adds a user to the postresql db.

    Input: 
        - name (str): name of user
        - email (str): email id of user 
        - role (str): role of the user, speaker or audience
    
    Output:
        added user to db.
    '''

    # Create a database session
    session = SessionLocal()

    # Add a user
    user = User(name=name, email=email, role=role)
    session.add(user)
    session.commit()

    # Close the session
    session.close()

def add_document(user_id, title, source_type, topic, content, chunk):
    '''
    Adds a user to the postresql db.

    Input: 
        - user_id (str): user id of user adding a document
        - title (str): title of the document
        - source_type (str): document type, powerpoint, image, pdf..
        - topic (str): topic of the document
        - content (str): text content of the document
    
    Output:
        added document to db.
    '''

    # Create a database session
    session = SessionLocal()

    # Add a document
    document = Document(user_id=user_id, title=title, source_type=source_type, topic=topic, 
                        content=content, chunk=chunk)
    session.add(document)
    session.commit()

    # Close the session
    session.close()

#add_user('Ansh Marwa', 'anshmarwa@gmail.com', 'speaker')
#add_document('1', '1. Review of functions and derivatives, and Integrals', 'Powerpoint', 'DS4400 - Machine Learning and Data Mining', extract_document_content('sample_test_files/1. Review of functions and derivatives, and Integrals.pdf')['text'])


def add_chunked_documents(chunked_doc_text, user_id, title, source_type, topic): 
    '''
    Iteratively add document chunked text to db. 

    Input : 
        - chunked_doc_text(str) : document text chunked into parts 
        - user_id (int) : user id of user uploading document 
        - title : title of document
        - source_type : source type of document 
        - topic : topic of document 

    Output : 
        adds documents chunks into db 
    '''


    # iterate through chunked document texts and add text content iteratively to db. 
    for idx in range(len(chunked_doc_text)): 
        add_document(user_id, title, source_type, topic, chunked_doc_text[idx], idx)