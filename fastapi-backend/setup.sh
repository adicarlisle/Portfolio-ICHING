#!/bin/bash

echo "Setting up I Ching Query API..."

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Download GloVe embeddings if not present
echo "Checking for GloVe embeddings..."
python3 download_glove.py

echo "Setup complete!"