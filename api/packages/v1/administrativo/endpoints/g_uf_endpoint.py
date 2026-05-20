# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_uf_controller import GUfController

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_uf_controller = GUfController()

# Lista todos os registros de uf
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de UF cadastrados',
            response_description='Lista todos os registros de UF cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de uf cadastrados
    response = g_uf_controller.index()

    # Retorna os dados localizados
    return response