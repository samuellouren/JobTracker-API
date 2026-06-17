# JobTracker API

REST API built with FastAPI and SQLite to track job applications.

## Tech Stack

- Python 3.14
- FastAPI
- SQLite
- Uvicorn

## Features

- Create, list, update and delete job applications
- Status validation with Enum (aplicado, entrevista, aprovado, reprovado)
- Persistent SQLite database
- Auto-generated Swagger documentation at `/docs`

## Getting Started

### Installation

```bash
pip install fastapi uvicorn
```

### Run

```bash
uvicorn main:app --reload
```

### API Endpoints

| Method | Route         | Description               |
| ------ | ------------- | ------------------------- |
| GET    | `/vagas`      | List all applications     |
| POST   | `/vagas`      | Create new application    |
| PUT    | `/vagas/{id}` | Update application status |
| DELETE | `/vagas/{id}` | Delete application        |

## Request Examples

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
