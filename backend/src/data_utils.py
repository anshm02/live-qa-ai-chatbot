

from pinecone import Pinecone, ServerlessSpec
import os
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM

from dotenv import load_dotenv
load_dotenv()


# index_name = "live-qa-chatbot"

# pc.create_index(
#     name=index_name,
#     dimension=384,
#     metric="cosine", 
#     spec=ServerlessSpec(
#         cloud="aws",
##        region="us-east-1"
#     ) 
# )

# Defining pinecone instance

def init_pc(): 
    return Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

def init_pc_index(): 
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index = pc.Index(os.getenv("INDEX_HOST"))

    return index

def init_llm(): 
    tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-7B-hf")
    model = AutoModelForCausalLM.from_pretrained("meta-llama/Llama-7B-hf")
    device = "cuda" if torch.cuda.is_available() else "cpu"
    model.to(device)

    