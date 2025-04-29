import os
import pdfplumber
import openai
from tqdm import tqdm
from dotenv import load_dotenv
from azure.search.documents import SearchClient
from azure.core.credentials import AzureKeyCredential

# Load environment variables
dotenv_path = os.path.join(os.path.dirname(__file__), ".env")
load_dotenv(dotenv_path)



# Azure AI Search credentials
AZURE_SEARCH_ENDPOINT = "https://lexi-rag-search.search.windows.net"
AZURE_SEARCH_KEY = "VU902PCG5YepHDEYMr3Jzx4UPSwxl692oLpqBb3FUVAzSeCrK0Cr"
AZURE_SEARCH_INDEX = "lexi-immigration-rag"

# Azure OpenAI credentials
AZURE_OPENAI_DEPLOYMENT="gpt-4-turbo"
AZURE_OPENAI_EMBEDDING_MODEL = "text-embedding-ada-002"
AZURE_OPENAI_MAX_EMBEDDINGS = 5 # Free-tier limit
OPENAI_API_KEY = "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"

# Set OpenAI API Key explicitly
openai.api_key = OPENAI_API_KEY

# Azure OpenAI Endpoint
OPENAI_API_ENDPOINT = "https://jmaje-m83sq68w-eastus2.cognitiveservices.azure.com/"
# Initialize Azure AI Search Client
search_client = SearchClient(
    endpoint=AZURE_SEARCH_ENDPOINT,
    index_name=AZURE_SEARCH_INDEX,
    credential=AzureKeyCredential(AZURE_SEARCH_KEY)
)
import re

def clean_document_key(filename):
    """
    Converts filename into a valid Azure AI Search document key.
    - Replaces spaces and special characters with underscores (_)
    - Keeps only letters, numbers, dashes, and underscores
    """
    filename = filename.lower().replace(" ", "_")
    filename = re.sub(r"[^a-zA-Z0-9_\-=]", "", filename)  # Only keep valid characters
    return filename
# Function to extract text & title from PDF
def extract_text_and_title(pdf_path):
    text = ""
    with pdfplumber.open(pdf_path) as pdf:
        title = os.path.basename(pdf_path).replace(".pdf", "")  # Extract file name as title
        for page in pdf.pages:
            text += page.extract_text() + "\n"
    return title, text

# Function to chunk text for embedding
def chunk_text(text, chunk_size=500):
    words = text.split()
    return [" ".join(words[i:i+chunk_size]) for i in range(0, len(words), chunk_size)]

# Function to generate embeddings
def generate_embedding(text):
    response = openai.Embedding.create(input=text, model=AZURE_OPENAI_EMBEDDING_MODEL)
    return response["data"][0]["embedding"]
def upload_documents_in_batches(search_client, documents, batch_size=10):
    """Uploads documents in small batches with a progress bar."""
    for i in tqdm(range(0, len(documents), batch_size), desc="Uploading to Azure AI Search"):
        batch = documents[i:i+batch_size]
        try:
            search_client.upload_documents(documents=batch)
            print(f"Uploaded {len(batch)} documents successfully.")
        except Exception as e:
            print(f"Error uploading batch {i}-{i+batch_size}: {e}")

# Function to process & upload PDFs
def process_and_upload_pdfs(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith(".pdf")]

    #  Show progress while processing PDFs
    for file in tqdm(pdf_files, desc="Processing PDFs"):
        pdf_path = os.path.join(folder_path, file)
        title, text = extract_text_and_title(pdf_path)
        text_chunks = chunk_text(text)

        documents = []
        for i, chunk in enumerate(text_chunks):
            embedding = generate_embedding(chunk)
            doc_id = f"{title.replace(' ', '_')}-{i}"
            doc_id = clean_document_key(doc_id)
            documents.append({
                "id": doc_id,
                "title": title,
                "content": chunk,
                "embedding": embedding
            })

        # Upload in batches with progress tracking
        upload_documents_in_batches(search_client, documents, batch_size=10)
        print(f" Successfully uploaded {len(documents)} chunks from {title}.")


# Run the pipeline
process_and_upload_pdfs("./data")
