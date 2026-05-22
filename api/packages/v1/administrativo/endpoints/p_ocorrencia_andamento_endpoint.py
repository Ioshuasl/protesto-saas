from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_ocorrencia_andamento_controller import (
    POcorrenciaAndamentoController,
)
from packages.v1.administrativo.schemas.p_ocorrencia_andamento_schema import (
    POcorrenciaAndamentoIdSchema,
    POcorrenciaAndamentoIndexSchema,
    POcorrenciaAndamentoSaveSchema,
    POcorrenciaAndamentoUpdateSchema,
)

router = APIRouter()
p_ocorrencia_andamento_controller = POcorrenciaAndamentoController()

_POCORRENCIA_ANDAMENTO_INDEX_FILTER_KEYS = frozenset({"descricao"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista ocorrências de andamento",
    response_description="Lista ocorrências de andamento",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _POCORRENCIA_ANDAMENTO_INDEX_FILTER_KEYS
        if key in url_params
    }
    index_schema = POcorrenciaAndamentoIndexSchema(**filter_data)
    return p_ocorrencia_andamento_controller.index(index_schema, query_params)


@router.get(
    "/{ocorrencia_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca ocorrência de andamento pelo ID",
    response_description="Busca ocorrência de andamento pelo ID",
)
async def show(
    ocorrencia_andamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencia_andamento_controller.show(
        POcorrenciaAndamentoIdSchema(ocorrencia_andamento_id=ocorrencia_andamento_id)
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra ocorrência de andamento",
    response_description="Cadastra ocorrência de andamento",
)
async def save(
    ocorrencia_andamento_schema: POcorrenciaAndamentoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencia_andamento_controller.save(ocorrencia_andamento_schema)


@router.put(
    "/{ocorrencia_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza ocorrência de andamento",
    response_description="Atualiza ocorrência de andamento",
)
async def update(
    ocorrencia_andamento_id: int,
    ocorrencia_andamento_schema: POcorrenciaAndamentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencia_andamento_controller.update(
        ocorrencia_andamento_id, ocorrencia_andamento_schema
    )


@router.delete(
    "/{ocorrencia_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove ocorrência de andamento",
    response_description="Remove ocorrência de andamento",
)
async def delete(
    ocorrencia_andamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_ocorrencia_andamento_controller.delete(
        POcorrenciaAndamentoIdSchema(ocorrencia_andamento_id=ocorrencia_andamento_id)
    )
