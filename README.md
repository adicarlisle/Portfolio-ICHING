# I Ching Query API 🔮

An intelligent FastAPI backend that provides I Ching divination services using modern NLP techniques. The system analyzes queries using GloVe embeddings and returns relevant hexagrams with their traditional meanings.

## Features ✨

- **Natural Language Processing**: Uses pre-trained GloVe embeddings to understand query semantics
- **64 Hexagram Database**: Complete I Ching hexagram set with Unicode characters (䷀-䷿)
- **Semantic Similarity**: Calculates relevance scores between queries and hexagrams
- **RESTful API**: Clean, documented endpoints for all operations
- **Query History**: Stores and retrieves past consultations
- **Similar Query Search**: Find related questions from history
- **Interactive CLI**: Command-line interface for easy interaction
- **Image Generation Support**: Generate mystical images for hexagrams (optional)

## Quick Start 🚀

### Prerequisites

- Python 3.8+
- pip3
- 2-3GB free space for GloVe embeddings

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd Portfolio-ICHING/fastapi-backend
```

2. Install dependencies:
```bash
pip3 install -r requirements.txt
```

3. Set up GloVe embeddings:
```bash
chmod +x setup.sh
./setup.sh
```

4. (Optional) Configure environment:
```bash
cp .env.example .env
# Edit .env if you want to use image generation features
```

### Running the API

Start the FastAPI server:
```bash
python3 main.py
```

The API will be available at `http://localhost:8000`

View API documentation at `http://localhost:8000/docs`

## Usage Examples 📖

### Quick Command-Line Query

Ask a single question:
```bash
python3 quick_query.py "What path should I take in my career?"
```

### Interactive Client

Launch the full interactive experience:
```bash
python3 interactive_client.py
```

Available commands:
- `ask <question>` - Consult the I Ching
- `find <query>` - Search similar past queries
- `history [n]` - View last n queries
- `hexagrams` - List all 64 hexagrams
- `help` - Show available commands
- `quit` - Exit

### Direct API Usage

```python
import requests

# Ask a question
response = requests.post(
    "http://localhost:8000/queries/",
    json={"query": "How can I find balance in my life?"}
)
result = response.json()

# Display hexagrams
for hexagram in result['hexagram_set']:
    print(f"{hexagram['hexagram_unicode']} {hexagram['hexagram_name']}")
```

## API Endpoints 🛠️

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Health check |
| POST | `/queries/` | Submit a new query |
| GET | `/queries/` | List all queries |
| GET | `/queries/{id}` | Get specific query |
| GET | `/queries/search/similar` | Find similar queries |
| GET | `/hexagrams/` | List all 64 hexagrams |

## How It Works 🧠

1. **Query Processing**: User questions are tokenized and converted to word embeddings
2. **Vector Calculation**: Query vectors are computed as the average of word embeddings
3. **Hexagram Matching**: Cosine similarity determines the most relevant hexagrams
4. **Result Ranking**: Top 6 hexagrams are returned with normalized relevance scores

## Project Structure 📁

```
fastapi-backend/
├── main.py                    # FastAPI application
├── models.py                  # SQLAlchemy models
├── schemas.py                 # Pydantic schemas
├── database.py                # Database configuration
├── services/
│   ├── iching_embeddings.py   # Core NLP service
│   └── image_generation.py    # Optional image gen
├── interactive_client.py      # CLI interface
├── quick_query.py            # Quick query tool
├── test_api.py               # API testing script
└── glove/                    # GloVe embeddings (after setup)
```

## Hexagram Example Output 📊

```
Your question: How can I find inner peace?

The I Ching responds with these hexagrams:

1. ䷊ Peace                          (95% relevance)
2. ䷤ The Family                    (82% relevance)
3. ䷾ After Completion              (76% relevance)
4. ䷘ Innocence                     (71% relevance)
5. ䷟ Duration                       (68% relevance)
6. ䷋ Standstill                    (65% relevance)
```

## Optional Features 🎨

### Image Generation

If you have API keys for image generation services, you can generate mystical representations of hexagrams:

1. Add API keys to `.env`:
```bash
OPENAI_API_KEY=your_key_here
STABILITY_API_KEY=your_key_here
REPLICATE_API_TOKEN=your_key_here
```

2. Generate images:
```bash
python3 generate_hexagram_images.py
```

## Performance Notes 📈

- **First Load**: ~10-30 seconds to load GloVe embeddings
- **Query Response**: <100ms after initialization
- **Memory Usage**: ~600MB-3GB depending on embedding size
- **Database**: SQLite by default, can be configured for PostgreSQL/MySQL

## Development 🔧

### Running Tests

```bash
python3 test_api.py
```

### Database Migrations

Using Alembic for database migrations:
```bash
alembic init alembic
alembic revision --autogenerate -m "Your migration message"
alembic upgrade head
```

### Adding New Features

1. Extend the models in `models.py`
2. Update schemas in `schemas.py`
3. Add new endpoints in `main.py`
4. Update the embedding service if needed

## Troubleshooting 🐛

**Cannot connect to API**
- Ensure the server is running: `python3 main.py`
- Check if port 8000 is available

**GloVe download fails**
- Check internet connection
- Manually download from [Stanford NLP](https://nlp.stanford.edu/projects/glove/)
- Place in `./glove/` directory

**High memory usage**
- Use smaller embeddings (50d or 100d instead of 300d)
- Implement selective vocabulary loading
- Consider using a database for embeddings

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License 📄

[Specify your license here]

## Acknowledgments 🙏

- Stanford NLP Group for GloVe embeddings
- I Ching wisdom tradition
- FastAPI framework
- Open source community

---

*"The I Ching does not offer itself with proofs and results; it does not vaunt itself, nor is it easy to approach. Like a part of nature, it waits until it is discovered."* - Carl Jung