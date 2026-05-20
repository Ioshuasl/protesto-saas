# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_emolumento_item_controller import (
    GEmolumentoItemController,
)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import (
    GEmolumentoItemByTipoAtoSchema,
    GEmolumentoItemIndexSchema,
    GEmolumentoItemSaveSchema,
    GEmolumentoItemUpdateSchema,
    GEmolumentoItemIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_EMOLUMENTO_ITEM
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_emolumento_item_controller = GEmolumentoItemController()


# ----------------------------------------------------
# Lista todos os registros de G_EMOLUMENTO_ITEM
# ----------------------------------------------------
@router.get(
    "/{emolumento_id}/{emolumento_periodo_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de G_EMOLUMENTO_ITEM cadastrados",
    response_description="Lista todos os registros de G_EMOLUMENTO_ITEM cadastrados",
)
async def index(
    emolumento_id: int,
    emolumento_periodo_id: int,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna todos os registros da tabela G_EMOLUMENTO_ITEM.
    """
    g_emolumento_item_emolumento_index_schema = GEmolumentoItemIndexSchema(
        emolumento_id=emolumento_id, emolumento_periodo_id=emolumento_periodo_id
    )
    response = g_emolumento_item_controller.index(
        g_emolumento_item_emolumento_index_schema
    )
    return response


# ----------------------------------------------------
# Busca um registro específico de G_EMOLUMENTO_ITEM pelo ID
# ----------------------------------------------------
@router.get(
    "/{emolumento_item_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de G_EMOLUMENTO_ITEM pelo ID",
    response_description="Busca um registro de G_EMOLUMENTO_ITEM em específico",
)
async def show(emolumento_item_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de G_EMOLUMENTO_ITEM com base no ID informado.
    """
    g_emolumento_item_id_schema = GEmolumentoItemIdSchema(
        emolumento_item_id=emolumento_item_id
    )
    response = g_emolumento_item_controller.show(g_emolumento_item_id_schema)
    return response


# ----------------------------------------------------
# Busca um registro específico de G_EMOLUMENTO_ITEM pelo ID
# ----------------------------------------------------
@router.get(
    "/{tipo_ato}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de G_EMOLUMENTO_ITEM pelo Tipo de Ato",
    response_description="Busca um registro de G_EMOLUMENTO_ITEM em específico",
)
async def get_by_tipo_ato(
    tipo_ato: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de G_EMOLUMENTO_ITEM com base no ID informado.
    """
    data = GEmolumentoItemByTipoAtoSchema(numero=tipo_ato)
    response = g_emolumento_item_controller.get_by_tipo_ato(data)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em G_EMOLUMENTO_ITEM
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em G_EMOLUMENTO_ITEM",
    response_description="Cadastra um novo registro em G_EMOLUMENTO_ITEM",
)
async def save(
    g_emolumento_item_schema: GEmolumentoItemSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela G_EMOLUMENTO_ITEM.
    """
    response = g_emolumento_item_controller.save(g_emolumento_item_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de G_EMOLUMENTO_ITEM
# ----------------------------------------------------
@router.put(
    "/{emolumento_item_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em G_EMOLUMENTO_ITEM",
    response_description="Atualiza um registro existente em G_EMOLUMENTO_ITEM",
)
async def update(
    emolumento_item_id: int,
    g_emolumento_item_update_schema: GEmolumentoItemUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de G_EMOLUMENTO_ITEM com base no ID informado.
    """
    g_emolumento_item_update_schema.emolumento_item_id = emolumento_item_id
    response = g_emolumento_item_controller.update(g_emolumento_item_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de G_EMOLUMENTO_ITEM
# ----------------------------------------------------
@router.delete(
    "/{emolumento_item_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de G_EMOLUMENTO_ITEM",
    response_description="Remove um registro de G_EMOLUMENTO_ITEM",
)
async def delete(
    emolumento_item_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de G_EMOLUMENTO_ITEM com base no ID informado.
    """
    g_emolumento_item_id_schema = GEmolumentoItemIdSchema(
        emolumento_item_id=emolumento_item_id
    )
    response = g_emolumento_item_controller.delete(g_emolumento_item_id_schema)
    return response
