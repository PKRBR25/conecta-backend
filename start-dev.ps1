$env:ENVIRONMENT = "development"
uvicorn app.main:app --reload --port 8000
