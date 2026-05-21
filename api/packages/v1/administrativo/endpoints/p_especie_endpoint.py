from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_especie_controller import PEspecieController
from packages.v1.administrativo.schemas.p_especie_schema import (
    PEspecieIdSchema,
    PEspecieIndexSchema,
    PEspecieSaveSchema,
    PEspecieUpdateSchema,
)

router = APIRouter()
p_especie_controller = PEspecieController()

_PESPECIE_INDEX_FILTER_KEYS = frozenset({"busca"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista espécies cadastradas",
    response_description="Lista espécies cadastradas",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
    busca: Optional[str] = Query(
        None,
        description="Busca unificada: LIKE em ESPECIE ou DESCRICAO (OR)",
    ),
):
    filter_data = {k: url_params[k] for k in _PESPECIE_INDEX_FILTER_KEYS if k in url_params}
    if busca is not None and "busca" not in filter_data:
        filter_data["busca"] = busca
    return p_especie_controller.index(PEspecieIndexSchema(**filter_data), query_params)


@router.get(
    "/{especie_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca espécie pelo ID",
    response_description="Busca espécie pelo ID",
)
async def show(
    especie_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_especie_controller.show(PEspecieIdSchema(especie_id=especie_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra espécie",
    response_description="Cadastra espécie",
)
async def save(
    especie_schema: PEspecieSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_especie_controller.save(especie_schema)


@router.put(
    "/{especie_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza espécie",
    response_description="Atualiza espécie",
)
async def update(
    especie_id: int,
    especie_schema: PEspecieUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_especie_controller.update(especie_id, especie_schema)


@router.delete(
    "/{especie_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove espécie",
    response_description="Remove espécie",
)
async def delete(
    especie_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_especie_controller.delete(PEspecieIdSchema(especie_id=especie_id))
