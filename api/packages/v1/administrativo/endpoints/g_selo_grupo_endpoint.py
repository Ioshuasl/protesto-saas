# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_selo_grupo_controller import GSeloGrupoController
from packages.v1.administrativo.schemas.g_selo_grupo_schema import (
    GSeloGrupoSaveSchema,
    GSeloGrupoUpdateSchema,
    GSeloGrupoIdSchema
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_SELO_GRUPO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_selo_grupo_controller = GSeloGrupoController()

# ----------------------------------------------------
# Lista todos os registros de G_SELO_GRUPO
# ----------------------------------------------------
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de G_SELO_GRUPO cadastrados',
            response_description='Lista todos os registros de G_SELO_GRUPO cadastrados')
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela G_SELO_GRUPO.
    """
    response = g_selo_grupo_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de G_SELO_GRUPO pelo ID
# ----------------------------------------------------
@router.get('/{selo_grupo_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de G_SELO_GRUPO pelo ID',
            response_description='Busca um registro de G_SELO_GRUPO em específico')
async def show(selo_grupo_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_SELO_GRUPO com base no ID informado.
    """
    g_selo_grupo_id_schema = GSeloGrupoIdSchema(selo_grupo_id=selo_grupo_id)
    response = g_selo_grupo_controller.show(g_selo_grupo_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_SELO_GRUPO
# ----------------------------------------------------
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Cadastra um novo registro em G_SELO_GRUPO',
             response_description='Cadastra um novo registro em G_SELO_GRUPO')
async def save(g_selo_grupo_schema: GSeloGrupoSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Cria um novo registro na tabela G_SELO_GRUPO.
    """
    response = g_selo_grupo_controller.save(g_selo_grupo_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_SELO_GRUPO
# ----------------------------------------------------
@router.put('/{selo_grupo_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro existente em G_SELO_GRUPO',
            response_description='Atualiza um registro existente em G_SELO_GRUPO')
async def update(selo_grupo_id: int, g_selo_grupo_update_schema: GSeloGrupoUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Atualiza um registro existente de G_SELO_GRUPO com base no ID informado.
    """
    g_selo_grupo_update_schema.selo_grupo_id = selo_grupo_id
    response = g_selo_grupo_controller.update(g_selo_grupo_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_SELO_GRUPO
# ----------------------------------------------------
@router.delete('/{selo_grupo_id}',
               status_code=status.HTTP_200_OK,
               summary='Remove um registro de G_SELO_GRUPO',
               response_description='Remove um registro de G_SELO_GRUPO')
async def delete(selo_grupo_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_SELO_GRUPO com base no ID informado.
    """
    g_selo_grupo_id_schema = GSeloGrupoIdSchema(selo_grupo_id=selo_grupo_id)
    response = g_selo_grupo_controller.delete(g_selo_grupo_id_schema)
    return response