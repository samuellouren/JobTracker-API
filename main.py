from fastapi import FastAPI
from pydantic import BaseModel
from database import conectar, criar_tabela
from enum import Enum

class StatusVaga(str, Enum):
    aplicado = "aplicado"
    entrevista = "entrevista"
    aprovado = "aprovado"
    reprovado = "reprovado"

app = FastAPI()
criar_tabela()


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