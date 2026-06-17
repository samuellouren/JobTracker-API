# JobTracker API

REST API built with FastAPI and SQLite to track job applications, featuring JWT authentication.

## Tech Stack

- Python 3.14
- FastAPI
- SQLite
- JWT (python-jose)
- Bcrypt (passlib)
- Uvicorn

## Features

- User registration and login with JWT authentication
- Protected routes — each user manages their own applications
- Create, list, update and delete job applications
- Status validation with Enum (aplicado, entrevista, aprovado, reprovado)
- Persistent SQLite database
- Auto-generated Swagger documentation at `/docs`

## Getting Started

### Installation

```bash
pip install fastapi uvicorn python-jose passlib bcrypt python-multipart python-dotenv
```

### Environment Variables

Create a `.env` file in the root folder:

```
SECRET_KEY=your-secret-key-here
```

### Run

```bash
uvicorn main:app --reload
```

## API Endpoints

### Auth

| Method | Route            | Description             |
| ------ | ---------------- | ----------------------- |
| POST   | `/auth/registro` | Register new user       |
| POST   | `/auth/login`    | Login and get JWT token |

### Vagas (requires JWT)

| Method | Route         | Description               |
| ------ | ------------- | ------------------------- |
| GET    | `/vagas`      | List all applications     |
| POST   | `/vagas`      | Create new application    |
| PUT    | `/vagas/{id}` | Update application status |
| DELETE | `/vagas/{id}` | Delete application        |

## Request Examples

### Register

```json
{
  "email": "user@email.com",
  "senha": "yourpassword"
}
```

### Create application

```json
{
  "empresa": "Trillia",
  "cargo": "Analista Júnior",
  "status": "aplicado",
  "data": "2026-06-17"
}
```

### Update status

```json
{
  "status": "entrevista"
}
```
