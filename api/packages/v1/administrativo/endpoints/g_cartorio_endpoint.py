# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_cartorio_controller import GCartorioController
from packages.v1.administrativo.schemas.g_cartorio_schema import (
    GCartorioSaveSchema,
    GCartorioUpdateSchema,
    GCartorioIdSchema
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_CARTORIO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_cartorio_controller = GCartorioController()

# ----------------------------------------------------
# Lista todos os registros de G_CARTORIO
# ----------------------------------------------------
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de G_CARTORIO cadastrados',
            response_description='Lista todos os registros de G_CARTORIO cadastrados')
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela G_CARTORIO.
    """
    response = g_cartorio_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de G_CARTORIO pelo ID
# ----------------------------------------------------
@router.get('/{cartorio_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de G_CARTORIO pelo ID',
            response_description='Busca um registro de G_CARTORIO em específico')
async def show(cartorio_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_CARTORIO com base no ID informado.
    """
    g_cartorio_id_schema = GCartorioIdSchema(cartorio_id=cartorio_id)
    response = g_cartorio_controller.show(g_cartorio_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_CARTORIO
# ----------------------------------------------------
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Cadastra um novo registro em G_CARTORIO',
             response_description='Cadastra um novo registro em G_CARTORIO')
async def save(g_cartorio_schema: GCartorioSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Cria um novo registro na tabela G_CARTORIO.
    """
    response = g_cartorio_controller.save(g_cartorio_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_CARTORIO
# ----------------------------------------------------
@router.put('/{cartorio_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro existente em G_CARTORIO',
            response_description='Atualiza um registro existente em G_CARTORIO')
async def update(cartorio_id: int, g_cartorio_update_schema: GCartorioUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Atualiza um registro existente de G_CARTORIO com base no ID informado.
    """
    g_cartorio_update_schema.cartorio_id = cartorio_id
    response = g_cartorio_controller.update(g_cartorio_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_CARTORIO
# ----------------------------------------------------
@router.delete('/{cartorio_id}',
               status_code=status.HTTP_200_OK,
               summary='Remove um registro de G_CARTORIO',
               response_description='Remove um registro de G_CARTORIO')
async def delete(cartorio_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_CARTORIO com base no ID informado.
    """
    g_cartorio_id_schema = GCartorioIdSchema(cartorio_id=cartorio_id)
    response = g_cartorio_controller.delete(g_cartorio_id_schema)
    return response