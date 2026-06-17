from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from database import conectar, criar_tabela_usuarios
from auth import hash_senha, verificar_senha, criar_token

criar_tabela_usuarios()

router = APIRouter()

class Usuario(BaseModel):
    email: str
    senha: str

@router.post("/registro")
def registrar(usuario: Usuario):
    conn = conectar()
    try:
        conn.execute(
            "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
            (usuario.email, hash_senha(usuario.senha))
        )
        conn.commit()
        return {"mensagem": "Usuario criado com sucesso!"}
    except Exception:
        raise HTTPException(status_code=400, detail="Email ja cadastrado")
    finally:
        conn.close

@router.post("/login")
def login(usuario: Usuario):
    conn = conectar()
    user = conn.execute(
        "SELECT * FROM usuarios WHERE email = ?", (usuario.email,)
    ).fetchone()
    conn.close()

    if not user or not verificar_senha(usuario.senha, user["senha"]):
        raise HTTPException(status_code=401, detail="Email ou senha invalidos")
    
    token = criar_token({"sub": usuario.email})
    return {"access_token": token, "token_type": "bearer"}