## Fund Investment CRUD APIs

REST APIs are designed using FastAPI framework. Error handling is done with the utilization of logging and HTTPException.

# Repository Structure

```bash
.
├── app/
│   ├── migration/
│   │   ├── run.sql           # SQL script here (including CREATE statements)
│   │   ├── schema.png        # SQL schema made in DBDiagrams
│   ├── .env
│   ├── app.log               # API logging file
│   ├── definitions.py        # Pydantic base model defined here
│   ├── helper.py             # Helper functions defined here
│   ├── main.py               # API endpoints defined here
│   └── requirements.txt
├── tests/                    # Unit and integration tests
├── readme.md
└── temp_db.json              # Lightweight database ie. JSON file
```

# How to Use

1. Upon cloning the repository, make sure to remain in the root directory.
2. Create a Conda or virtual environment before running Python code.
3. Within the environment, run `pip install -r app/requirements.txt`.
4. Start uvicorn server with `uvicorn app.main:app --reload` to interact with APIs in Postman or /docs.
5. 

