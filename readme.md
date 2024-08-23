## Fund Investment CRUD APIs

REST APIs are designed using FastAPI framework. Error handling is done with the utilization of logging and HTTPException.

# Repo Navigation

1. API script files are stored in the app folder
2. Python class in the form of Pydantic base model is stored in `definitions.py`
3. Definition of API endpoints is in `main.py` and helper function(s) in `helper.py`
4. Logs are stored in `app.log` file in the root directory

# Cloning the Repo
1. After cloning the repo, run `pip install -r app/requirements.txt` to install libraries used
2. Start uvicorn server with `uvicorn app.main:app --reload` to run and test APIs