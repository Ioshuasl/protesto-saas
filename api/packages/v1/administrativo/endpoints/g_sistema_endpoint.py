from fastapi import APIRouter, Depends, status

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_sistema_controller import GSistemaController
from packages.v1.administrativo.schemas.g_sistema_schema import (
    GSistemaIdSchema,
    GSistemaIndexSchema,
    GSistemaSaveSchema,
    GSistemaUpdateSchema,
)

router = APIRouter()
g_sistema_controller = GSistemaController()

_GSISTEMA_INDEX_FILTER_KEYS = frozenset({"descricao", "situacao", "tipo_cartorio"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista sistemas cadastrados",
    response_description="Lista sistemas cadastrados",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _GSISTEMA_INDEX_FILTER_KEYS
        if key in url_params
    }
    sistema_index_schema = GSistemaIndexSchema(**filter_data)
    return g_sistema_controller.index(sistema_index_schema, query_params)


@router.get(
    "/{sistema_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca sistema pelo ID",
    response_description="Busca sistema pelo ID",
)
async def show(
    sistema_id: float,
    current_user: dict = Depends(get_current_user),
):
    return g_sistema_controller.show(GSistemaIdSchema(sistema_id=sistema_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra sistema",
    response_description="Cadastra sistema",
)
async def save(
    sistema_schema: GSistemaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return g_sistema_controller.save(sistema_schema)


@router.put(
    "/{sistema_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza sistema",
    response_description="Atualiza sistema",
)
async def update(
    sistema_id: float,
    sistema_schema: GSistemaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return g_sistema_controller.update(sistema_id, sistema_schema)


@router.delete(
    "/{sistema_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove sistema",
    response_description="Remove sistema",
)
async def delete(
    sistema_id: float,
    current_user: dict = Depends(get_current_user),
):
    return g_sistema_controller.delete(GSistemaIdSchema(sistema_id=sistema_id))
