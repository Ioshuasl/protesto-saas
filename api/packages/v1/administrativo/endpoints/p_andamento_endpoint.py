from fastapi import APIRouter, Depends, status

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_andamento_controller import PAndamentoController
from packages.v1.administrativo.schemas.p_andamento_schema import (
    PAndamentoIdSchema,
    PAndamentoIndexByTituloSchema,
    PAndamentoIndexSchema,
    PAndamentoSaveSchema,
    PAndamentoUpdateSchema,
)

router = APIRouter()
p_andamento_controller = PAndamentoController()

_PANDAMENTO_INDEX_FILTER_KEYS = frozenset(
    {"titulo_id", "data_ocorrencia", "ocorrencia_andamento_id"}
)

_PANDAMENTO_INDEX_BY_TITULO_FILTER_KEYS = frozenset(
    {"data_ocorrencia", "ocorrencia_andamento_id"}
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista andamentos de título",
    response_description="Lista andamentos de título",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _PANDAMENTO_INDEX_FILTER_KEYS
        if key in url_params
    }
    andamento_index_schema = PAndamentoIndexSchema(**filter_data)
    return p_andamento_controller.index(andamento_index_schema, query_params)


@router.get(
    "/titulo/{titulo_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista andamentos de um título (com ocorrência de andamento)",
    response_description="Andamentos do título com include de P_OCORRENCIA_ANDAMENTO",
)
async def index_by_titulo(
    titulo_id: int,
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _PANDAMENTO_INDEX_BY_TITULO_FILTER_KEYS
        if key in url_params
    }
    filter_schema = PAndamentoIndexByTituloSchema(**filter_data)
    return p_andamento_controller.index_by_titulo(titulo_id, filter_schema, query_params)


@router.get(
    "/{andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca andamento pelo ID",
    response_description="Busca andamento pelo ID",
)
async def show(
    andamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_andamento_controller.show(PAndamentoIdSchema(andamento_id=andamento_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra andamento de título",
    response_description="Cadastra andamento de título",
)
async def save(
    andamento_schema: PAndamentoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_andamento_controller.save(andamento_schema)


@router.put(
    "/{andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza andamento de título",
    response_description="Atualiza andamento de título",
)
async def update(
    andamento_id: int,
    andamento_schema: PAndamentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_andamento_controller.update(andamento_id, andamento_schema)


@router.delete(
    "/{andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove andamento de título",
    response_description="Remove andamento de título",
)
async def delete(
    andamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_andamento_controller.delete(PAndamentoIdSchema(andamento_id=andamento_id))
