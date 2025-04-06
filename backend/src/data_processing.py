'''
This module is responsible for processing and retrieving document cotent. 
'''

from tika import parser
import re


def extract_document_content(file_path):
    '''
    This function extracts text content from a document. 

    Input: 
        file_path (str): file path to the uploaded document 

    Output: 
        dictionary with text and metadata of extracted document content. 
    '''
    parsed = parser.from_file(file_path)
    text = parsed.get('content', '')
    return text


def clean_text(text):
    """
    Cleans text to make it optimal for chunking:
    1. Replaces multiple newlines with a single newline (preserving paragraphs).
    2. Removes tabs and extra spaces.
    3. Strips leading and trailing whitespace.
    4. Ensures consistent spacing between sentences.

    Input: 
        text (str) - text content of a document 
    
    Output: 
        cleaned text with removed spaces and identations 
    """
    # Replace tabs and carriage returns with a space
    text = text.replace('\t', ' ').replace('\r', ' ')
    # Replace multiple newlines with a single newline
    text = re.sub(r'\n{2,}', '\n', text)
    # Replace multiple spaces with a single space
    text = re.sub(r' +', ' ', text)
    # Strip leading/trailing whitespace from the entire text
    text = text.strip()
    return text