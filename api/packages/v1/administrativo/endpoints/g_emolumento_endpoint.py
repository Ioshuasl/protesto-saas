# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_emolumento_controller import (
    GEmolumentoController,
)
from packages.v1.administrativo.schemas.g_emolumento_schema import (
    GEmolumentoSaveSchema,
    GEmolumentoSistemaIdSchema,
    GEmolumentoUpdateSchema,
    GEmolumentoIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_EMOLUMENTO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_emolumento_controller = GEmolumentoController()


# ----------------------------------------------------
# Lista todos os registros de G_EMOLUMENTO
# ----------------------------------------------------
@router.get(
    "/sistema/{sistema_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de G_EMOLUMENTO cadastrados",
    response_description="Lista todos os registros de G_EMOLUMENTO cadastrados",
)
async def index(
    sistema_id: int,
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
):
    """
    Retorna todos os registros da tabela G_EMOLUMENTO.
    """
    response = g_emolumento_controller.indexBySistemaId(
        GEmolumentoSistemaIdSchema(sistema_id=sistema_id, **url_params)
    )
    return response


# ----------------------------------------------------
# Busca um registro específico de G_EMOLUMENTO pelo ID
# ----------------------------------------------------
@router.get(
    "/{emolumento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de G_EMOLUMENTO pelo ID",
    response_description="Busca um registro de G_EMOLUMENTO em específico",
)
async def show(emolumento_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_EMOLUMENTO com base no ID informado.
    """
    g_emolumento_id_schema = GEmolumentoIdSchema(emolumento_id=emolumento_id)
    response = g_emolumento_controller.show(g_emolumento_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_EMOLUMENTO
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em G_EMOLUMENTO",
    response_description="Cadastra um novo registro em G_EMOLUMENTO",
)
async def save(
    g_emolumento_schema: GEmolumentoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela G_EMOLUMENTO.
    """
    response = g_emolumento_controller.save(g_emolumento_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_EMOLUMENTO
# ----------------------------------------------------
@router.put(
    "/{emolumento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em G_EMOLUMENTO",
    response_description="Atualiza um registro existente em G_EMOLUMENTO",
)
async def update(
    emolumento_id: int,
    g_emolumento_update_schema: GEmolumentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de G_EMOLUMENTO com base no ID informado.
    """
    g_emolumento_update_schema.emolumento_id = emolumento_id
    response = g_emolumento_controller.update(g_emolumento_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_EMOLUMENTO
# ----------------------------------------------------
@router.delete(
    "/{emolumento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de G_EMOLUMENTO",
    response_description="Remove um registro de G_EMOLUMENTO",
)
async def delete(emolumento_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_EMOLUMENTO com base no ID informado.
    """
    g_emolumento_id_schema = GEmolumentoIdSchema(emolumento_id=emolumento_id)
    response = g_emolumento_controller.delete(g_emolumento_id_schema)
    return response
