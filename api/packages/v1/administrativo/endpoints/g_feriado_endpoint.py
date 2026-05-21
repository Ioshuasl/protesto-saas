from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_feriado_controller import GFeriadoController
from packages.v1.administrativo.schemas.g_feriado_schema import (
    GFeriadoIdSchema,
    GFeriadoIndexSchema,
    GFeriadoSaveSchema,
    GFeriadoUpdateSchema,
)

router = APIRouter()
g_feriado_controller = GFeriadoController()

_GFERIADO_INDEX_FILTER_KEYS = frozenset({"ano", "tipo", "situacao", "descricao"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista feriados cadastrados",
    response_description="Lista feriados cadastrados",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _GFERIADO_INDEX_FILTER_KEYS
        if key in url_params
    }
    feriado_index_schema = GFeriadoIndexSchema(**filter_data)
    return g_feriado_controller.index(feriado_index_schema, query_params)


@router.get(
    "/{feriado_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca feriado pelo ID",
    response_description="Busca feriado pelo ID",
)
async def show(
    feriado_id: int,
    current_user: dict = Depends(get_current_user),
):
    return g_feriado_controller.show(GFeriadoIdSchema(feriado_id=feriado_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra feriado",
    response_description="Cadastra feriado",
)
async def save(
    feriado_schema: GFeriadoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return g_feriado_controller.save(feriado_schema)


@router.put(
    "/{feriado_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza feriado",
    response_description="Atualiza feriado",
)
async def update(
    feriado_id: int,
    feriado_schema: GFeriadoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return g_feriado_controller.update(feriado_id, feriado_schema)


@router.delete(
    "/{feriado_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove feriado",
    response_description="Remove feriado",
)
async def delete(
    feriado_id: int,
    current_user: dict = Depends(get_current_user),
):
    return g_feriado_controller.delete(GFeriadoIdSchema(feriado_id=feriado_id))
