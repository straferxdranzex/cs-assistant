# Customer Support Assistant Backend

A FastAPI-based backend for a customer support assistant that uses AI to generate helpful responses to customer inquiries.

## Features

- User authentication (signup/login) with JWT
- Support ticket creation and management
- Real-time AI response streaming using Server-Sent Events (SSE)
- PostgreSQL database integration
- Docker containerization

## Tech Stack

- FastAPI
- SQLAlchemy (async)
- PostgreSQL
- JWT Authentication
- Groq API for AI responses
- Docker & Docker Compose

## Project Structure

```
src/
├── app/
│   ├── api/
│   │   └── api_v1/
│   │       ├── endpoints/
│   │       │   ├── auth.py
│   │       │   ├── tickets.py
│   │       │   └── ai.py
│   │       └── api.py
│   ├── core/
│   │   ├── config.py
│   │   └── security.py
│   ├── db/
│   │   └── session.py
│   ├── models/
│   │   ├── base.py
│   │   ├── user.py
│   │   └── ticket.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── user.py
│   │   └── ticket.py
│   ├── services/
│   │   ├── user.py
│   │   ├── ticket.py
│   │   └── ai.py
│   └── main.py
```

## Design Patterns and OOP Principles

### Service-Oriented Architecture

The application follows a service-oriented architecture where:

- Services handle business logic
- Models represent database entities
- Schemas define data validation and serialization
- Endpoints handle HTTP requests and responses

### Dependency Injection

Dependencies are injected through FastAPI's dependency injection system, making the code more testable and maintainable.

### Repository Pattern

The service layer acts as a repository, abstracting database operations and providing a clean interface for the API layer.

## Setup and Installation

1. Clone the repository
2. Copy `.env.example` to `.env` and fill in your environment variables
3. Install dependencies:
   ```bash
   poetry install
   ```
4. Start the application with Docker:
   ```bash
   docker-compose up --build
   ```

The API will be available at `http://localhost:8000`

## API Documentation

Once the application is running, you can access the interactive API documentation at:

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `SECRET_KEY`: JWT secret key
- `ALGORITHM`: JWT algorithm (default: HS256)
- `ACCESS_TOKEN_EXPIRE_MINUTES`: JWT token expiration time
- `GROQ_API_KEY`: Groq API key
- `GROQ_MODEL`: Groq model to use (default: mixtral-8x7b-32768)

## Challenges and Solutions

1. **Real-time AI Response Streaming**

   - Challenge: Implementing efficient streaming of AI responses
   - Solution: Used Server-Sent Events (SSE) with FastAPI's StreamingResponse

2. **Asynchronous Database Operations**

   - Challenge: Managing async database sessions
   - Solution: Implemented async SQLAlchemy with proper session management

3. **Authentication and Authorization**
   - Challenge: Securing endpoints and managing user permissions
   - Solution: Implemented JWT-based authentication with role-based access control

## Future Improvements

1. Add rate limiting to prevent abuse
2. Implement caching for frequently accessed data
3. Add more comprehensive error handling
4. Implement WebSocket support for real-time updates
5. Add unit and integration tests
6. Implement CI/CD pipeline
7. Add monitoring and logging
8. Implement more advanced AI response customization

## License

MIT
