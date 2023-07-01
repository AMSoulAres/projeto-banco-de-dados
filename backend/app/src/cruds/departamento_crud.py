import json
from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from backend.app.src.db_connector import mycursor

router  = APIRouter(
    prefix="/departamento",
    tags=["Departamento"]
)

@router.get("")
async def lista_departamentos():
    mycursor.execute("SELECT * FROM avaliacaounb.Departamentos d")
    return mycursor.fetchall()

@router.get("{id}")
async def busca_departamento(id_departamento: int):
    mycursor.execute(f"SELECT NomeDepartamento FROM avaliacaounb.Departamentos d WHERE d.idDepartamento = {id_departamento}")
    return mycursor.fetchone()

