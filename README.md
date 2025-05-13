# Conecta - Procurement Team Login System

[![CI/CD](https://github.com/PKRBR25/conecta-backend/actions/workflows/main.yml/badge.svg)](https://github.com/PKRBR25/conecta-backend/actions/workflows/main.yml)
[![codecov](https://codecov.io/gh/PKRBR25/conecta-backend/branch/main/graph/badge.svg)](https://codecov.io/gh/PKRBR25/conecta-backend)

A secure and bilingual SaaS platform enabling procurement teams to manage their operations efficiently.

## Features

- Secure email/password authentication
- Bilingual support (English/Portuguese-BR)
- Password recovery via email
- WCAG 2.1 compliant accessibility

## Tech Stack

- Backend: Python with FastAPI
- Database: PostgreSQL
- ORM: SQLModel
- Authentication: JWT
- Email: SMTP integration

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

4. Run migrations:
```bash
alembic upgrade head
```

5. Start the development server:
```bash
uvicorn app.main:app --reload
```

## Project Structure

```
backend/
├── alembic/            # Database migrations
├── app/
│   ├── api/           # API routes
│   ├── core/          # Core functionality
│   ├── db/            # Database models and config
│   ├── schemas/       # Pydantic models
│   └── services/      # Business logic
├── tests/             # Test files
└── requirements.txt   # Project dependencies
```

## Development

- Follow PEP8 guidelines
- Use type hints
- Write tests for new features
- Update migrations for database changes

## License

Proprietary - All rights reserved
