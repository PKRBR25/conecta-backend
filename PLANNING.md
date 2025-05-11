# Conecta - Project Planning

## Architecture & Design Patterns

### Backend Architecture
- FastAPI for REST API
- Clean Architecture pattern:
  - API Layer (routes)
  - Service Layer (business logic)
  - Repository Layer (data access)
  - Domain Layer (models)

### Database Design
- PostgreSQL with SQLModel ORM
- Tables:
  - users (id, email, hashed_password, is_active, created_at, updated_at)
  - password_reset_tokens (id, user_id, token, expires_at, used)

### Authentication Flow
1. User submits email/password
2. Backend validates credentials
3. On success: returns JWT token
4. On failure: returns error message in user's language

### Password Recovery Flow
1. User requests password reset
2. System generates 6-digit code
3. Code sent via email
4. User enters code
5. On success: user sets new password

## Code Style & Conventions

### Python Style
- Follow PEP8
- Use type hints
- Black for formatting
- Line length: 88 characters
- Docstrings: Google style

### Naming Conventions
- Files: snake_case
- Classes: PascalCase
- Functions/Variables: snake_case
- Constants: UPPER_CASE

### Import Order
1. Standard library
2. Third-party packages
3. Local modules

## Security Measures
- Password hashing with bcrypt
- JWT with short expiration
- Rate limiting on auth endpoints
- SQL injection prevention via ORM
- XSS prevention
- CORS configuration

## Testing Strategy
- Unit tests with pytest
- Integration tests for API endpoints
- Test coverage > 80%
- Mock external services

## Internationalization
- Language codes: en, pt-br
- Translation files in JSON
- Default: English
- Runtime language switching

## Performance Considerations
- Database indexing
- Query optimization
- Caching where appropriate
- Rate limiting
- Connection pooling
