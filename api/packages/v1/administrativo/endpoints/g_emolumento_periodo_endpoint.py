# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_emolumento_periodo_controller import GEmolumentoPeriodoController
from packages.v1.administrativo.schemas.g_emolumento_periodo_schema import (
    GEmolumentoPeriodoSaveSchema,
    GEmolumentoPeriodoUpdateSchema,
    GEmolumentoPeriodoIdSchema
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_EMOLUMENTO_PERIODO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_emolumento_periodo_controller = GEmolumentoPeriodoController()

# ----------------------------------------------------
# Lista todos os registros de G_EMOLUMENTO_PERIODO
# ----------------------------------------------------
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de G_EMOLUMENTO_PERIODO cadastrados',
            response_description='Lista todos os registros de G_EMOLUMENTO_PERIODO cadastrados')
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela G_EMOLUMENTO_PERIODO.
    """
    response = g_emolumento_periodo_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de G_EMOLUMENTO_PERIODO pelo ID
# ----------------------------------------------------
@router.get('/{emolumento_periodo_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de G_EMOLUMENTO_PERIODO pelo ID',
            response_description='Busca um registro de G_EMOLUMENTO_PERIODO em específico')
async def show(emolumento_periodo_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_EMOLUMENTO_PERIODO com base no ID informado.
    """
    g_emolumento_periodo_id_schema = GEmolumentoPeriodoIdSchema(emolumento_periodo_id=emolumento_periodo_id)
    response = g_emolumento_periodo_controller.show(g_emolumento_periodo_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_EMOLUMENTO_PERIODO
# ----------------------------------------------------
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Cadastra um novo registro em G_EMOLUMENTO_PERIODO',
             response_description='Cadastra um novo registro em G_EMOLUMENTO_PERIODO')
async def save(g_emolumento_periodo_schema: GEmolumentoPeriodoSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Cria um novo registro na tabela G_EMOLUMENTO_PERIODO.
    """
    response = g_emolumento_periodo_controller.save(g_emolumento_periodo_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_EMOLUMENTO_PERIODO
# ----------------------------------------------------
@router.put('/{emolumento_periodo_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro existente em G_EMOLUMENTO_PERIODO',
            response_description='Atualiza um registro existente em G_EMOLUMENTO_PERIODO')
async def update(emolumento_periodo_id: int, g_emolumento_periodo_update_schema: GEmolumentoPeriodoUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Atualiza um registro existente de G_EMOLUMENTO_PERIODO com base no ID informado.
    """
    g_emolumento_periodo_update_schema.emolumento_periodo_id = emolumento_periodo_id
    response = g_emolumento_periodo_controller.update(g_emolumento_periodo_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_EMOLUMENTO_PERIODO
# ----------------------------------------------------
@router.delete('/{emolumento_periodo_id}',
               status_code=status.HTTP_200_OK,
               summary='Remove um registro de G_EMOLUMENTO_PERIODO',
               response_description='Remove um registro de G_EMOLUMENTO_PERIODO')
async def delete(emolumento_periodo_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_EMOLUMENTO_PERIODO com base no ID informado.
    """
    g_emolumento_periodo_id_schema = GEmolumentoPeriodoIdSchema(emolumento_periodo_id=emolumento_periodo_id)
    response = g_emolumento_periodo_controller.delete(g_emolumento_periodo_id_schema)
    return response