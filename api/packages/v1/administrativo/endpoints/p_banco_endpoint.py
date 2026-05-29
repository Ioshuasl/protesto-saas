from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_banco_controller import PBancoController
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoCodigoSchema,
    PBancoIdSchema,
    PBancoIndexSchema,
    PBancoSaveSchema,
    PBancoUpdateSchema,
)

router = APIRouter()
p_banco_controller = PBancoController()

@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista bancos cadastrados",
    response_description="Lista bancos cadastrados",
)
async def index(
    current_user: dict = Depends(get_current_user),
    busca: Optional[str] = Query(
        None,
        description="Busca unificada: LIKE em CODIGO_BANCO ou DESCRICAO (OR)",
    ),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {}
    if busca is not None:
        filter_data["busca"] = busca
    return p_banco_controller.index(PBancoIndexSchema(**filter_data), query_params)


@router.get(
    "/codigo/{codigo_banco}",
    status_code=status.HTTP_200_OK,
    summary="Busca banco pelo código",
    response_description="Busca banco pelo código (CODIGO_BANCO)",
)
async def show_by_codigo(
    codigo_banco: str,
    current_user: dict = Depends(get_current_user),
):
    return p_banco_controller.show_by_codigo(PBancoCodigoSchema(codigo_banco=codigo_banco))


@router.get(
    "/{banco_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca banco pelo ID",
    response_description="Busca banco pelo ID",
)
async def show(
    banco_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_banco_controller.show(PBancoIdSchema(banco_id=banco_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra banco",
    response_description="Cadastra banco",
)
async def save(
    banco_schema: PBancoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_banco_controller.save(banco_schema)


@router.put(
    "/{banco_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza banco",
    response_description="Atualiza banco",
)
async def update(
    banco_id: int,
    banco_schema: PBancoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_banco_controller.update(banco_id, banco_schema)


@router.delete(
    "/{banco_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove banco",
    response_description="Remove banco",
)
async def delete(
    banco_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_banco_controller.delete(PBancoIdSchema(banco_id=banco_id))
