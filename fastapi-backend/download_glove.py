import os
import requests
import zipfile
import numpy as np
from tqdm import tqdm

def download_glove(glove_dir="./glove"):
    """Download GloVe embeddings if not already present"""
    if not os.path.exists(glove_dir):
        os.makedirs(glove_dir)
    
    glove_file = os.path.join(glove_dir, "glove.6B.300d.txt")
    
    if os.path.exists(glove_file):
        print("GloVe embeddings already downloaded.")
        return glove_file
    
    # Download GloVe embeddings (6B tokens, 300d vectors)
    url = "http://nlp.stanford.edu/data/glove.6B.zip"
    zip_file = os.path.join(glove_dir, "glove.6B.zip")
    
    print("Downloading GloVe embeddings...")
    response = requests.get(url, stream=True)
    total_size = int(response.headers.get('content-length', 0))
    
    with open(zip_file, 'wb') as f:
        with tqdm(total=total_size, unit='B', unit_scale=True) as pbar:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
                pbar.update(len(chunk))
    
    print("Extracting GloVe embeddings...")
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extract("glove.6B.300d.txt", glove_dir)
    
    # Clean up zip file
    os.remove(zip_file)
    print("GloVe embeddings downloaded successfully!")
    return glove_file

def load_glove_embeddings(glove_file, vocab_size=None):
    """Load GloVe embeddings into a dictionary"""
    embeddings = {}
    
    with open(glove_file, 'r', encoding='utf-8') as f:
        for i, line in enumerate(tqdm(f, desc="Loading GloVe")):
            if vocab_size and i >= vocab_size:
                break
            
            values = line.split()
            word = values[0]
            vector = np.array(values[1:], dtype='float32')
            embeddings[word] = vector
    
    return embeddings

if __name__ == "__main__":
    glove_file = download_glove()
    print(f"GloVe embeddings saved to: {glove_file}")