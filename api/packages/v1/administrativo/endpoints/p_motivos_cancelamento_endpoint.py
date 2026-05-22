from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_motivos_cancelamento_controller import (
    PMotivosCancelamentoController,
)
from packages.v1.administrativo.schemas.p_motivos_cancelamento_schema import (
    PMotivosCancelamentoIdSchema,
    PMotivosCancelamentoIndexSchema,
    PMotivosCancelamentoSaveSchema,
    PMotivosCancelamentoUpdateSchema,
)

router = APIRouter()
p_motivos_cancelamento_controller = PMotivosCancelamentoController()

_PMOTIVOS_CANCELAMENTO_INDEX_FILTER_KEYS = frozenset({"descricao"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista motivos de cancelamento",
    response_description="Lista motivos de cancelamento",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _PMOTIVOS_CANCELAMENTO_INDEX_FILTER_KEYS
        if key in url_params
    }
    motivos_cancelamento_index_schema = PMotivosCancelamentoIndexSchema(**filter_data)
    return p_motivos_cancelamento_controller.index(
        motivos_cancelamento_index_schema, query_params
    )


@router.get(
    "/{motivos_cancelamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca motivo de cancelamento pelo ID",
    response_description="Busca motivo de cancelamento pelo ID",
)
async def show(
    motivos_cancelamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_cancelamento_controller.show(
        PMotivosCancelamentoIdSchema(motivos_cancelamento_id=motivos_cancelamento_id)
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra motivo de cancelamento",
    response_description="Cadastra motivo de cancelamento",
)
async def save(
    motivos_cancelamento_schema: PMotivosCancelamentoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_cancelamento_controller.save(motivos_cancelamento_schema)


@router.put(
    "/{motivos_cancelamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza motivo de cancelamento",
    response_description="Atualiza motivo de cancelamento",
)
async def update(
    motivos_cancelamento_id: int,
    motivos_cancelamento_schema: PMotivosCancelamentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_cancelamento_controller.update(
        motivos_cancelamento_id, motivos_cancelamento_schema
    )


@router.delete(
    "/{motivos_cancelamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove motivo de cancelamento",
    response_description="Remove motivo de cancelamento",
)
async def delete(
    motivos_cancelamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_cancelamento_controller.delete(
        PMotivosCancelamentoIdSchema(motivos_cancelamento_id=motivos_cancelamento_id)
    )
