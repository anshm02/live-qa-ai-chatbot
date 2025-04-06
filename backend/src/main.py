''' 
this module is responsible for the overall execution of the program. It is responsible for digesting 
uploaded documents, and transcribing live audio and generating a chatbot to relevant user questions.
'''

from pinecone import Pinecone, ServerlessSpec
import os

from query_data import query_specific_documents
from data_processing import clean_text
from vector_data_loader import embed_text_content, chunk_text
from data_processing import extract_document_content, clean_text
from seed import add_document, add_user, add_chunked_documents
from query_data import get_user_id

from embeddings import embed_query
from generating import generate_repsonse 

from dotenv import load_dotenv
load_dotenv()


def main(): 

    # Process document content
    # doc_text = extract_document_content('sample_test_files/1. Review of functions and derivatives, and Integrals.pdf')
    # cleaned_doc_text = clean_text(doc_text)

    # # Chunk text document 
    # chunked_doc_text = chunk_text(cleaned_doc_text)

    # Add document and user data 
    #add_user("Test User", "testuser@gmail.com", "Professor")

    # add_chunked_documents(chunked_doc_text=chunked_doc_text, 
    #                     user_id=get_user_id('testuser@gmail.com'), 
    #                     title="1. Review of functions and derivatives, and Integrals.pdf", 
    #                     source_type="Powerpoint", 
    #                     topic="Machine Learning and Data Mining Lecture")

    # Init pinecone
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("INDEX_NAME")) 

    # Query postresql db for document content to store into vector db
    doc_metadata = query_specific_documents(2, "Machine Learning and Data Mining Lecture")

    pinecone_vectors = []

    for doc in doc_metadata: 
        embeddings = embed_text_content(doc)

        doc_id = doc['document_id']
        vector_id = f'doc_id{doc_id}'

        pinecone_vectors.append({
            "id": vector_id,
            "values": embeddings.data[0]['values'],
            "metadata": doc 
        })

    index.upsert(vectors=pinecone_vectors, namespace="documents")

    user_query = "What must I learn before attending my lecture on Machine learning and data mining?"
    generate_repsonse(user_query)


main()

