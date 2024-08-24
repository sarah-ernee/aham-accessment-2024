## Fund Investment CRUD APIs

REST APIs are designed using FastAPI framework. Error handling is done with the utilization of logging and HTTPException.

# Repository Structure

```bash
.
├── app/   
│   ├── app.log               # API logging file
│   ├── definitions.py        # Pydantic base model defined here
│   ├── helper.py             # Helper functions defined here
│   ├── main.py               # API endpoints defined here
│   └── requirements.txt
├── migration/   
│   ├── create.sql            # CREATE statements
│   ├── migrate.sql           # JSON-SQL migrate script
│   └── schema.png            # Schema of SQL tables made in DBDiagrams
├── tests/   
│   ├── pytest.ini           
│   ├── test_sql.py           # Test script for SQL queries
│   └── test_main.py          # Test script for APIs
└── temp_db.csv               
└── temp_db.json              
```

# How to Use

1. Upon cloning the repository, make sure to remain in the root directory.
2. Create a Conda or virtual environment before running Python code.
3. Within the environment, run `pip install -r app/requirements.txt`.
4. Start uvicorn server with `uvicorn app.main:app --reload` to interact with APIs in Postman or /docs.
5. To run `migrate.sql`, you can use `\i` or copy pasting into CMD Prompt. `COPY` statement uses absolute path so make sure to plug in your own path to the CSV file.
6. Run unit tests with `pytest tests/`


