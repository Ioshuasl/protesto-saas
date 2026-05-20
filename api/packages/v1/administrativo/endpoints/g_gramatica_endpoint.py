# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_gramatica_controller import (
    GGramaticaController,
)
from packages.v1.administrativo.schemas.g_gramatica_schema import (
    GGramaticaSaveSchema,
    GGramaticaUpdateSchema,
    GGramaticaIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_GRAMATICA
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_gramatica_controller = GGramaticaController()


# ----------------------------------------------------
# Lista todos os registros de G_GRAMATICA
# ----------------------------------------------------
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de G_GRAMATICA cadastrados",
    response_description="Lista todos os registros de G_GRAMATICA cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela G_GRAMATICA.
    """
    response = g_gramatica_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de G_GRAMATICA pelo ID
# ----------------------------------------------------
@router.get(
    "/{gramatica_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de G_GRAMATICA pelo ID",
    response_description="Busca um registro de G_GRAMATICA em específico",
)
async def show(gramatica_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_GRAMATICA com base no ID informado.
    """
    g_gramatica_id_schema = GGramaticaIdSchema(gramatica_id=gramatica_id)
    response = g_gramatica_controller.show(g_gramatica_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_GRAMATICA
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em G_GRAMATICA",
    response_description="Cadastra um novo registro em G_GRAMATICA",
)
async def save(
    g_gramatica_schema: GGramaticaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela G_GRAMATICA.
    """
    response = g_gramatica_controller.save(g_gramatica_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_GRAMATICA
# ----------------------------------------------------
@router.put(
    "/{gramatica_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em G_GRAMATICA",
    response_description="Atualiza um registro existente em G_GRAMATICA",
)
async def update(
    gramatica_id: int,
    g_gramatica_update_schema: GGramaticaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de G_GRAMATICA com base no ID informado.
    """
    g_gramatica_update_schema.gramatica_id = gramatica_id
    response = g_gramatica_controller.update(g_gramatica_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_GRAMATICA
# ----------------------------------------------------
@router.delete(
    "/{gramatica_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de G_GRAMATICA",
    response_description="Remove um registro de G_GRAMATICA",
)
async def delete(gramatica_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_GRAMATICA com base no ID informado.
    """
    g_gramatica_id_schema = GGramaticaIdSchema(gramatica_id=gramatica_id)
    response = g_gramatica_controller.delete(g_gramatica_id_schema)
    return response
