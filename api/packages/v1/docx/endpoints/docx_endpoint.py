# Importação de bibliotecas
from fastapi import APIRouter
from fastapi import Request

from packages.v1.docx.controllers.docx_controller import DOCXController
from packages.v1.docx.schemas.docx_schema import DOCXSchemaCallback

# Inicializar o roteaodr para as rotas de produtos
router = APIRouter()

# Controller do docx
docx_controller = DOCXController()

@router.post("/callback/{registro_id}/{servico}")
async def callback(registro_id: int, servico: str, request: Request):

    # lê o JSON enviado
    data = await request.json()

    response = docx_controller.save(
        DOCXSchemaCallback(registro_id=registro_id, servico=servico, data=data)
    )

    return {"error": 0}
