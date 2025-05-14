$env:ENVIRONMENT = "staging"
uvicorn app.main:app --reload --port 8001
