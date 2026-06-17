from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.openapi.utils import get_openapi
from pydantic import BaseModel
from enum import Enum
from database import conectar, criar_tabela
from auth import verificar_token
import usuarios

app = FastAPI()
criar_tabela()

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="JobTracker API",
        version="1.0.0",
        routes=app.routes,
    )
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

app.include_router(usuarios.router, prefix="/auth", tags=["Auth"])
security = HTTPBearer()

def obter_usuario(credentials: HTTPAuthorizationCredentials = Depends(security)):
    email = verificar_token(credentials.credentials)
    if not email:
        raise HTTPException(status_code=401, detail="Token invalido ou expirado")
    return email
class StatusVaga(str, Enum):
    aplicado = "aplicado"
    entrevista = "entrevista"
    aprovado = "aprovado"
    reprovado = "reprovado"

class Vaga(BaseModel):
    empresa: str
    cargo: str
    status: StatusVaga
    data: str

class AtualizarStatus(BaseModel):
    status: StatusVaga

vagas = []

@app.get("/")
def inicio():
    return {"mensagem": "JobTracker API funcionando!"}

@app.post("/vagas")
def criar_vaga(vaga: Vaga):
    conn = conectar()
    conn.execute(
        "INSERT INTO vagas (empresa, cargo, status, data) VALUES (?, ?, ?, ?)",
        (vaga.empresa, vaga.cargo, vaga.status, vaga.data)
    )
    conn.commit()
    conn.close()
    return {"mensagem": "Vaga cadastrada!"}


@app.get("/vagas")
def listar_vagas():
    conn = conectar()
    vagas = conn.execute("SELECT * FROM vagas").fetchall()
    conn.close()
    return [dict(v) for v in vagas]

@app.put("/vagas/{id}")
def att_vaga(id: int, dados: AtualizarStatus):
    conn = conectar()
    resultado = conn.execute("UPDATE vagas SET status = ? WHERE id = ?", (dados.status, id))
    conn.commit()
    conn.close()
    if resultado.rowcount == 0:
        return {"erro": "Vaga não encontrada"}
    return {"mensagem": "Status atualizado!"}

@app.delete("/vagas/{id}")
def apagar_vaga(id: int):
    conn = conectar()
    resultado = conn.execute("DELETE FROM vagas WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    if resultado.rowcount == 0:
        return {"erro": "Vaga não encontrada"}
    return {"mensagem": "Vaga removida!"}