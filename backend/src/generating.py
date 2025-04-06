from pinecone import Pinecone
from transformers import pipeline
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, AutoModelForSeq2SeqLM, RagTokenizer, RagRetriever, RagTokenForGeneration
from huggingface_hub import InferenceClient

hf_token = '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'

def search_vector_db(query_embedding):

    pc = Pinecone(api_key='pcsk_2DJvfv_15BZUcMUVRpPuA4x6DLrFdBJHQuVLDBggtRjscxGWhqQ3B8Su4rtDMFUC7aihEb')
    index = pc.Index('live-qa-chatbot')

    return index.query(
        namespace="documents",
        vector=query_embedding,
        top_k=1,
        include_metadata=True,
    )

def embed_query(user_query):
    '''
    This function embeds a user query. The same embeddings model must be used between the documents
    and query.

    Input:
        - user_query(str) : represents a user question about a document.

    Output:
        - embeddings(dict[int]) : query embedded content.
    '''

    pc = Pinecone(api_key="pcsk_2DJvfv_15BZUcMUVRpPuA4x6DLrFdBJHQuVLDBggtRjscxGWhqQ3B8Su4rtDMFUC7aihEb")
    index = pc.Index('live-qa-chatbot')

    query_embedding = pc.inference.embed(
        model="multilingual-e5-large",
        inputs=user_query,
        parameters={"input_type": "passage", "truncate": "END"}
    )

    return query_embedding[0]['values']


def generate_repsonse(user_query): 

    repo_id = "mistralai/Mixtral-8x7B-Instruct-v0.1"

    llm_client = InferenceClient(model=repo_id, timeout=120, token=hf_token)

    PROMPT = """
    You are teaching assistant chatbot. Use the following pieces of information enclosed in <context> tags to provide an answer to the question enclosed in <question> tags. Please use only the 
    provided information enclosed in the context tags only. Be concise, clear and use direct language with your response. 
    <context>
    {context}
    </context>
    <question>
    {question}
    </question>
    """

    input_query = "what must I learn before I attend the lecture of functions and derivatives in my machine learning and data mining class?"

    # Embed the user query
    query_embedding = embed_query(user_query)

    # Search Pinecone for relevant documents based on the embedding
    search_results = search_vector_db(query_embedding)

    # Combine the results from Pinecone to form a more complete context for the LLaMA response
    document_context = "\n".join([match['metadata']['content'] for match in search_results['matches']])

    prompt = PROMPT.format(context=document_context, question=input_query)

    answer = llm_client.text_generation(
        prompt,
        max_new_tokens=1000,
    ).strip()
    print(answer)

