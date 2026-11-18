FastAPI Database Fundamentals
A hands-on Python backend learning project built with FastAPI,
SQLModel, Pydantic, and Ollama. It demonstrates REST API
development, relational data models, database sessions, dependency
injection, CRUD operations, and a local LLM integration.
This repository is an evolving learning project. The current committed
application uses SQLite by default. A PostgreSQL connection example is
present in main.py as an alternative configuration.

Features
Database APIs
- Item and Order SQLModel database models
- Automatic table creation during application startup
- Database session dependency using FastAPI dependency injection
- Create and list endpoints for items and orders
- SQLite database stored in database.db
Local LLM API
- Integrates FastAPI with a locally running Ollama server
- Sends chat requests to Ollama's /api/chat endpoint
- Uses the model configured in services/ollama_service.py
- Supports prompt and temperature inputs
- Uses asynchronous HTTP requests through httpx
- Returns the prompt, generated response, and model name
- Handles Ollama connection, HTTP, and timeout errors
Technology Stack
- Python
- FastAPI
- SQLModel
- Pydantic
- SQLite (default database configuration)
- PostgreSQL (alternative configuration example)
- Ollama
- Qwen model configured in the application
- HTTPX
- Uvicorn
- Swagger UI / OpenAPI
Repository Structure
fastapi-database-fundamentals/
├── routers/
│   └── llm.py
├── schemas/
│   └── llm.py
├── services/
│   └── ollama_service.py
├── database.db
├── fastAPI.py
├── hello-python.py
└── main.py
Prerequisites
- Python 3.10 or newer
- pip
- Ollama installed and running for the LLM endpoint
- The model configured in services/ollama_service.py downloaded in
  Ollama
Check your Python installation:
python3 --version
Check Ollama:
ollama --version
ollama list
The committed Ollama service currently specifies:
MODEL_NAME = "qwen2.5-coder:3b"
Make sure this exact model is available locally, or update MODEL_NAME
to match a model you have downloaded.
ollama pull qwen2.5-coder:3b
Start Ollama if it is not already running:
ollama serve
If Ollama is managed by systemd on your Linux machine, you can also
check it with:
sudo systemctl status ollama
Setup and Run
1. Clone the repository
git clone https://github.com/vvudugula/fastapi-database-fundamentals.git
cd fastapi-database-fundamentals
2. Create and activate a virtual environment
Linux / macOS:
python3 -m venv .venv
source .venv/bin/activate
Windows PowerShell:
python -m venv .venv
.venv\Scripts\Activate.ps1
3. Install dependencies
Install the packages used by the application:
pip install fastapi uvicorn sqlmodel httpx
4. Start the API
From the project root:
uvicorn main:app --reload --host 127.0.0.1 --port 8000
The API will be available at:
- Base URL: http://127.0.0.1:8000
- Swagger UI: http://127.0.0.1:8000/docs
- ReDoc: http://127.0.0.1:8000/redoc
The database tables are created by the application's startup lifespan
function.
API Endpoints
Health check
  Method   Endpoint   Purpose
  GET      /        Returns application status

Example response:
{
  "status": "running"
}
Items
  Method   Endpoint    Purpose
  POST     /items/   Create an item
GET      /items/   List items

Example create-item request (based on the current Item model):
{
  "name": "Laptop",
  "description": "Development laptop",
  "price": 1200.0
}
Orders
  Method   Endpoint     Purpose
  POST     /orders/   Create an order
GET      /orders/   List orders

Example create-order request (based on the current Order model):
{
  "customer_name": "John",
  "product_name": "Laptop",
  "description": "Development laptop order",
  "price": 1200.0,
  "item_id": 1
}
The item_id field is optional and references an item when supplied.
The current model also defines an SQLModel relationship between Order
and Item.
Local LLM
  Method                  Endpoint                Purpose
  POST                    /llm/generate         Generate a response
using the configured
local Ollama model
Example request:
{
  "prompt": "Explain microservices architecture in simple terms.",
  "temperature": 0.3
}
Example response shape:
{
  "prompt": "Explain microservices architecture in simple terms.",
  "response": "A generated response from the local language model.",
  "model": "qwen2.5-coder:3b"
}
The generated response will vary depending on the prompt and model
output.
LLM error handling
The current LLM route maps common Ollama communication failures to HTTP
responses:

  HTTP status   Meaning
  503           Ollama service is unavailable
502           Ollama returned an unsuccessful HTTP response
504           LLM generation timed out
422           Request validation failed
How the LLM Integration Works
1. A client submits a prompt and temperature to POST /llm/generate.
2. FastAPI validates the request using the LLMRequest Pydantic model.
3. The route calls the Ollama service function.
4. The service sends an asynchronous HTTP request to
   http://127.0.0.1:11434/api/chat.
5. Ollama runs the configured local model and returns the generated
   message.
6. FastAPI returns the prompt, generated response, and model name.
The current implementation uses non-streaming responses
(stream: false) and an HTTPX timeout of 180 seconds.
PostgreSQL Configuration
The committed main.py currently uses SQLite:
DATABASE_URL = "sqlite:///./database.db"
connect_args = {"check_same_thread": False}
engine = create_engine(DATABASE_URL, connect_args=connect_args)
A PostgreSQL URL example is also present in the source:
DATABASE_URL = "postgresql+psycopg2://user:password@localhost:5432/dbname"
To switch to PostgreSQL:
1. Install a PostgreSQL driver, for example:
   pip install psycopg2-binary
2. Configure the PostgreSQL URL using environment variables rather than
   committing credentials.
3. Update engine creation to omit SQLite-specific connect_args:
   engine = create_engine(DATABASE_URL)
4. Ensure the PostgreSQL database exists and the configured user has
   the required permissions.
Do not commit database passwords, API keys, or other secrets to source
control.
Learning Objectives
This repository is being used to practise:
- Python backend development
- REST API design with FastAPI
- Data modelling with SQLModel
- Request validation with Pydantic
- Database sessions and dependency injection
- CRUD operations
- API documentation with Swagger / OpenAPI
- Asynchronous HTTP calls with HTTPX
- Local LLM integration using Ollama
- Error handling around model-serving dependencies
Current Scope and Future Improvements
The project is a learning foundation. Potential next improvements
include:
- Separate database models from request and response schemas
- Move database configuration into environment variables
- Add database migrations with Alembic
- Add update, delete, and retrieve-by-ID endpoints
- Add pagination and filtering
- Add automated tests with pytest
- Add shared HTTP client lifecycle management
- Add system prompts and configurable chat messages
- Add structured JSON output validation
- Add conversation history
- Add RAG using embeddings and a vector store
- Add authentication, logging, and monitoring
Run and Test with Swagger
1. Start Ollama and confirm the configured model is available.
2. Start FastAPI using the Uvicorn command above.
3. Open http://127.0.0.1:8000/docs.
4. Test the Items and Orders endpoints.
5. Test POST /llm/generate with a prompt.
6. Confirm the generated response is returned by the API.
Author
GitHub: @vvudugula

Repository:
fastapi-database-fundamentals
This repository is maintained as a practical learning and portfolio
project. Features and documentation will evolve as new backend and LLM
engineering topics are implemented.
