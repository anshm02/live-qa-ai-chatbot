'''
This module is responsible for querying from the database, and inserting data into our vector db.  
'''

from pinecone import Pinecone, ServerlessSpec
import uuid
from transformers import AutoTokenizer, AutoModel
import torch

import os
from dotenv import load_dotenv
load_dotenv()

import time


def chunk_text(text, max_length=300, overlap=50):
    """
    Splits a document into chunks of specified max length with overlap.

    Input:
        - text (str): The document to chunk.
        - max_length (int): The maximum length of each chunk in words.
        - overlap (int): The number of overlapping words between chunks.

    Output:
        List[str]: A list of text chunks.
    """
    words = text.split()
    chunks = []
    start = 0

    while start < len(words):
        end = min(start + max_length, len(words))
        chunk = " ".join(words[start:end])
        chunks.append(chunk)
        
        start += max_length - overlap

    return chunks


def embed_text_content(document_metadata): 
    '''
    Embed text content to before upserting to vector db 

    Input: 
        - text (str): document text content to be embedded. 

    Output: 
        - List[str]: embedded document text chunked into different parts. 
    
    '''
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

    pinecone_metadata = "\n".join([
        f"{key}: {value}" for key, value in document_metadata.items()
    ])

    embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=pinecone_metadata,
        parameters={"input_type": "passage", "truncate": "END"}
    )

    return embedding 


def index_upload_embedding_content(): 
    '''
    Uploads embedded content to vector db 

    Input : 
        - 
    
    Output : 
        - loads vectorized content to db 
    '''

    
