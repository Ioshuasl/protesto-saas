from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_ocorrencias_controller import (
    POcorrenciasController,
)
from packages.v1.administrativo.schemas.p_ocorrencias_schema import (
    POcorrenciasIdSchema,
    POcorrenciasIndexSchema,
    POcorrenciasSaveSchema,
    POcorrenciasUpdateSchema,
)

router = APIRouter()
p_ocorrencias_controller = POcorrenciasController()

_POCORRENCIAS_INDEX_FILTER_KEYS = frozenset({"busca", "tipo"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista ocorrências de protesto",
    response_description="Lista ocorrências de protesto",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _POCORRENCIAS_INDEX_FILTER_KEYS
        if key in url_params
    }
    ocorrencias_index_schema = POcorrenciasIndexSchema(**filter_data)
    return p_ocorrencias_controller.index(ocorrencias_index_schema, query_params)


@router.get(
    "/{ocorrencias_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca ocorrência pelo ID",
    response_description="Busca ocorrência pelo ID",
)
async def show(
    ocorrencias_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencias_controller.show(
        POcorrenciasIdSchema(ocorrencias_id=ocorrencias_id)
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra ocorrência de protesto",
    response_description="Cadastra ocorrência de protesto",
)
async def save(
    ocorrencias_schema: POcorrenciasSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencias_controller.save(ocorrencias_schema)


@router.put(
    "/{ocorrencias_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza ocorrência de protesto",
    response_description="Atualiza ocorrência de protesto",
)
async def update(
    ocorrencias_id: int,
    ocorrencias_schema: POcorrenciasUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencias_controller.update(ocorrencias_id, ocorrencias_schema)


@router.delete(
    "/{ocorrencias_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove ocorrência de protesto",
    response_description="Remove ocorrência de protesto",
)
async def delete(
    ocorrencias_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencias_controller.delete(
        POcorrenciasIdSchema(ocorrencias_id=ocorrencias_id)
    )
