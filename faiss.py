from dotenv import load_dotenv
load_dotenv()
import os
import sys
import math
from openai import AzureOpenAI


client = AzureOpenAI(
  api_version = "2024-02-01",
  api_key = os.getenv("AZURE_OPENAI_API_KEY"),  
  azure_endpoint = os.getenv("OPENAI_API_BASE")  
)

### VERSION 3: CREATE FAISS INDEX ###
import faiss
import openai
from pathlib import Path
from utils.oai import OAIEmbedding
from utils.index import FAISSIndex
from utils.logging import log
from utils.lock import acquire_lock
from constants import INDEX_DIR

plotfile = "assets/plots.out"
plots=[]
with open(plotfile) as f:
  for line in f:
      plots.append(line)

## create batches for index loading
splits=800
s = math.ceil(len(plots)/splits)

def create_faiss_index(pdf_path: str) -> str:
    chunk_size = int(os.environ.get("CHUNK_SIZE"))
    chunk_overlap = int(os.environ.get("CHUNK_OVERLAP"))
    log(f"Chunk size: {chunk_size}, chunk overlap: {chunk_overlap}")

    file_name = Path(pdf_path).name + f".index_{chunk_size}_{chunk_overlap}"
    index_persistent_path = Path(INDEX_DIR) / file_name
    index_persistent_path = index_persistent_path.resolve().as_posix()
    lock_path = index_persistent_path + ".lock"
    log("Index path: " + os.path.abspath(index_persistent_path))
    log("Lock path: " + os.path.abspath(lock_path))


    with acquire_lock(lock_path):
        if os.path.exists(os.path.join(index_persistent_path, "index.faiss")):
            log("Index already exists, bypassing index creation")
            return index_persistent_path
        else:
            if not os.path.exists(index_persistent_path):
                os.makedirs(index_persistent_path)

        log("Building index")

        # Chunk the words into segments of X words with Y-word overlap, X=CHUNK_SIZE, Y=OVERLAP_SIZE
        #segments = split_text(text, chunk_size, chunk_overlap)
        segments = plots

        log(f"Number of segments: {len(segments)}")
        index = FAISSIndex(index=faiss.IndexFlatL2(1536), embedding=OAIEmbedding())
        
        for a in range(0,s):
           batch = segments[a*splits:min((a+1)*splits-1,len(plots)-1)]
           index.insert_batch(batch)
           index.save(index_persistent_path)

        log("Index built: " + index_persistent_path)
        return index_persistent_path

# Split the text into chunks with CHUNK_SIZE and CHUNK_OVERLAP as character count
def split_text(text, chunk_size, chunk_overlap):
    # Calculate the number of chunks
    num_chunks = (len(text) - chunk_overlap) // (chunk_size - chunk_overlap)

    # Split the text into chunks
    chunks = []
    for i in range(num_chunks):
        start = i * (chunk_size - chunk_overlap)
        end = start + chunk_size
        chunks.append(text[start:end])

    # Add the last chunk
    chunks.append(text[num_chunks * (chunk_size - chunk_overlap):])

    return chunks

create_faiss_index('./movies')
