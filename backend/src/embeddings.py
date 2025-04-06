'''
This module is responsible for the embedding query, speech and document content. 
'''

from pinecone import Pinecone
import os 

from dotenv import load_dotenv
load_dotenv()


def embed_query(user_query): 
    '''
    This function embeds a user query. The same embeddings model must be used between the documents 
    and query. 

    Input: 
        - user_query(str) : represents a user question about a document. 

    Output: 
        - embeddings(dict[int]) : query embedded content. 
    '''

    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index('live-qa-chatbot')    

    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=user_query,
        parameters={"input_type": "passage", "truncate": "END"}
    )

    return query_embedding[0]['values']