from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_motivos_controller import PMotivosController
from packages.v1.administrativo.schemas.p_motivos_schema import (
    PMotivosIdSchema,
    PMotivosIndexSchema,
    PMotivosSaveSchema,
    PMotivosUpdateSchema,
)

router = APIRouter()
p_motivos_controller = PMotivosController()

_PMOTIVOS_INDEX_FILTER_KEYS = frozenset({"descricao", "situacao"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista motivos de apontamento",
    response_description="Lista motivos de apontamento",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key]
        for key in _PMOTIVOS_INDEX_FILTER_KEYS
        if key in url_params
    }
    motivos_index_schema = PMotivosIndexSchema(**filter_data)
    return p_motivos_controller.index(motivos_index_schema, query_params)


@router.get(
    "/{motivos_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca motivo pelo ID",
    response_description="Busca motivo pelo ID",
)
async def show(
    motivos_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_controller.show(PMotivosIdSchema(motivos_id=motivos_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra motivo de apontamento",
    response_description="Cadastra motivo de apontamento",
)
async def save(
    motivos_schema: PMotivosSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_controller.save(motivos_schema)


@router.put(
    "/{motivos_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza motivo de apontamento",
    response_description="Atualiza motivo de apontamento",
)
async def update(
    motivos_id: int,
    motivos_schema: PMotivosUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_controller.update(motivos_id, motivos_schema)


@router.delete(
    "/{motivos_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove motivo de apontamento",
    response_description="Remove motivo de apontamento",
)
async def delete(
    motivos_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_motivos_controller.delete(PMotivosIdSchema(motivos_id=motivos_id))
