import json
from fastapi import APIRouter, Response, UploadFile, File
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse, StreamingResponse
from fastapi.exceptions import HTTPException
from src.models.estudante_dao import EstudanteDAO, EstudantePost, EstudanteUpdate
from src.db_connector import mycursor, db
import base64


router  = APIRouter(
    prefix="/estudante",
    tags=["Estudante"]
)

dao = EstudanteDAO(db=db, cursor=mycursor)

@router.get("/")
async def lista_estudantes():
    try:
        return dao.get_all()
    except HTTPException as e:
        raise e
    except Exception as err:
        HTTPException(status_code=500, detail=f"{err}")

@router.get("/{matriculaEstudante}")
async def busca_estudante(matriculaEstudante: int):
    try:
        return dao.get_estudante_by_id(matriculaEstudante)
    except HTTPException as e:
        raise e
    except Exception as err:
        HTTPException(status_code=500, detail=f"{err}")

@router.get("/image/{matriculaEstudante}")
async def busca_estudante_image(matriculaEstudante: int):
    try:
        img = dao.get_image_by_id(matriculaEstudante)
        return Response(content=img, media_type="image/*")
    except HTTPException as e:
        raise e
    except Exception as err:
        HTTPException(status_code=500, detail=f"{err}")

@router.post("/insere-estudante")
async def insere_estudante(estudante: EstudantePost):
    try:
        inserido = dao.add_aluno(estudante)
        return JSONResponse(status_code=201, content=json.loads(json.dumps(inserido.__dict__)))
    except HTTPException as e:
        raise e
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err}")
    
@router.post("/insere-imagem/{matriculaEstudante}")
async def insere_estudante(matriculaEstudante: int, image_file: UploadFile = File(...)):
    try:
        contents = image_file.file.read()
        dao.add_image(matriculaEstudante, contents)
        return JSONResponse(status_code=200, content=f"Imagem alterada com sucesso")
    except HTTPException as e:
        raise e
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err}")
    
@router.put("/atualiza-estudante/{matriculaEstudante}")
async def atualiza_estudante(matriculaEstudante: int, estudante: EstudanteUpdate):
    try:
        return dao.update_estudante(matriculaEstudante, estudante)
         
    except HTTPException as e:
        raise e
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err}")

@router.delete("/deleta-estudante/{matriculaEstudante}")
async def deleta_estudante(matriculaEstudante: int):
    try:
        dao.delete_estudante(matriculaEstudante)
        return JSONResponse(status_code=200, content="Usuário deletado com sucesso")
    except HTTPException as e:
        raise e
    except Exception as err:
        raise HTTPException(status_code=500, detail=f"{err}")