# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_natureza_titulo_controller import GNaturezaTituloController
from packages.v1.administrativo.schemas.g_natureza_titulo_schema import (
    GNaturezaTituloIndexSchema,
    GNaturezaTituloSaveSchema,
    GNaturezaTituloUpdateSchema,
    GNaturezaTituloIdSchema
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_NATUREZA_TITULO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_natureza_titulo_controller = GNaturezaTituloController()

# ----------------------------------------------------
# Lista todos os registros de G_NATUREZA_TITULO
# ----------------------------------------------------
@router.get('/sistema/{sistema_id}',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de G_NATUREZA_TITULO cadastrados',
            response_description='Lista todos os registros de G_NATUREZA_TITULO cadastrados')
async def index(sistema_id:int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela G_NATUREZA_TITULO.
    """
    g_natureza_titulo_index_schema = GNaturezaTituloIndexSchema(sistema_id=sistema_id)
    response = g_natureza_titulo_controller.index(g_natureza_titulo_index_schema)
    return response


# ----------------------------------------------------
# Busca um registro específico de G_NATUREZA_TITULO pelo ID
# ----------------------------------------------------
@router.get('/{natureza_titulo_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de G_NATUREZA_TITULO pelo ID',
            response_description='Busca um registro de G_NATUREZA_TITULO em específico')
async def show(natureza_titulo_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_NATUREZA_TITULO com base no ID informado.
    """
    g_natureza_titulo_id_schema = GNaturezaTituloIdSchema(natureza_titulo_id=natureza_titulo_id)
    response = g_natureza_titulo_controller.show(g_natureza_titulo_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_NATUREZA_TITULO
# ----------------------------------------------------
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Cadastra um novo registro em G_NATUREZA_TITULO',
             response_description='Cadastra um novo registro em G_NATUREZA_TITULO')
async def save(g_natureza_titulo_schema: GNaturezaTituloSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Cria um novo registro na tabela G_NATUREZA_TITULO.
    """
    response = g_natureza_titulo_controller.save(g_natureza_titulo_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_NATUREZA_TITULO
# ----------------------------------------------------
@router.put('/{natureza_titulo_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro existente em G_NATUREZA_TITULO',
            response_description='Atualiza um registro existente em G_NATUREZA_TITULO')
async def update(natureza_titulo_id: int, g_natureza_titulo_update_schema: GNaturezaTituloUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Atualiza um registro existente de G_NATUREZA_TITULO com base no ID informado.
    """
    g_natureza_titulo_update_schema.natureza_titulo_id = natureza_titulo_id
    response = g_natureza_titulo_controller.update(g_natureza_titulo_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_NATUREZA_TITULO
# ----------------------------------------------------
@router.delete('/{natureza_titulo_id}',
               status_code=status.HTTP_200_OK,
               summary='Remove um registro de G_NATUREZA_TITULO',
               response_description='Remove um registro de G_NATUREZA_TITULO')
async def delete(natureza_titulo_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_NATUREZA_TITULO com base no ID informado.
    """
    g_natureza_titulo_id_schema = GNaturezaTituloIdSchema(natureza_titulo_id=natureza_titulo_id)
    response = g_natureza_titulo_controller.delete(g_natureza_titulo_id_schema)
    return response