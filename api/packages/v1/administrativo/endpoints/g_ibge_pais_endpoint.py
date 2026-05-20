# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_ibge_pais_controller import (
    GIbgePaisController,
)
from packages.v1.administrativo.schemas.g_ibge_pais_schema import (
    GIbgePaisSaveSchema,
    GIbgePaisUpdateSchema,
    GIbgePaisIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_IBGE_PAIS
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
controller = GIbgePaisController()


# ----------------------------------------------------
# Lista todos os registros de G_IBGE_PAIS
# ----------------------------------------------------
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de G_IBGE_PAIS cadastrados",
    response_description="Lista todos os registros de G_IBGE_PAIS cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela G_IBGE_PAIS.
    """
    response = controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de G_IBGE_PAIS pelo ID
# ----------------------------------------------------
@router.get(
    "/{ibge_pais_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de G_IBGE_PAIS pelo ID",
    response_description="Busca um registro de G_IBGE_PAIS em específico",
)
async def show(ibge_pais_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_IBGE_PAIS com base no ID informado.
    """
    data = GIbgePaisIdSchema(ibge_pais_id=ibge_pais_id)
    response = controller.show(data)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_IBGE_PAIS
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em G_IBGE_PAIS",
    response_description="Cadastra um novo registro em G_IBGE_PAIS",
)
async def save(
    g_ibge_pais_schema: GIbgePaisSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela G_IBGE_PAIS.
    """
    response = controller.save(g_ibge_pais_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_IBGE_PAIS
# ----------------------------------------------------
@router.put(
    "/{ibge_pais_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em G_IBGE_PAIS",
    response_description="Atualiza um registro existente em G_IBGE_PAIS",
)
async def update(
    ibge_pais_id: int,
    data: GIbgePaisUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de G_IBGE_PAIS com base no ID informado.
    """
    setattr(data, "ibge_pais_id", ibge_pais_id)
    response = controller.update(setattr(data, "ibge_pais_id", ibge_pais_id))
    return response


# ----------------------------------------------------
# Exclui um registro de G_IBGE_PAIS
# ----------------------------------------------------
@router.delete(
    "/{ibge_pais_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de G_IBGE_PAIS",
    response_description="Remove um registro de G_IBGE_PAIS",
)
async def delete(ibge_pais_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de G_IBGE_PAIS com base no ID informado.
    """
    data = GIbgePaisIdSchema(ibge_pais_id=ibge_pais_id)
    response = controller.delete(data)
    return response
