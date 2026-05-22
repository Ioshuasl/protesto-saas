from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_pessoa_controller import PPessoaController
from packages.v1.administrativo.schemas.p_pessoa_schema import (
    PPessoaIdSchema,
    PPessoaIndexSchema,
    PPessoaSaveSchema,
    PPessoaUpdateSchema,
)

router = APIRouter()
p_pessoa_controller = PPessoaController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista pessoas cadastradas",
    response_description="Lista pessoas cadastradas",
)
async def index(
    current_user: dict = Depends(get_current_user),
    busca: Optional[str] = Query(
        None,
        description=(
            "Busca unificada: concatena resultados por NOME (LIKE), "
            "depois CPFCNPJ (prefixo), depois TELEFONE (prefixo)"
        ),
    ),
    cidade: Optional[str] = Query(
        None, description="Filtro exato em CIDADE (valor do seletor)"
    ),
    uf: Optional[str] = Query(None, description="Filtro exato em UF (seletor)"),
    tipo_pessoa: Optional[str] = Query(
        None,
        description="F = pessoa física (CPF, 11 dígitos); J = pessoa jurídica (CNPJ, 14 dígitos)",
    ),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: value
        for key, value in {
            "busca": busca,
            "cidade": cidade,
            "uf": uf,
            "tipo_pessoa": tipo_pessoa,
        }.items()
        if value is not None
    }
    return p_pessoa_controller.index(PPessoaIndexSchema(**filter_data), query_params)


@router.get(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca pessoa pelo ID",
    response_description="Busca pessoa pelo ID",
)
async def show(
    pessoa_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_controller.show(PPessoaIdSchema(pessoa_id=pessoa_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra pessoa",
    response_description="Cadastra pessoa",
)
async def save(
    pessoa_schema: PPessoaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_controller.save(pessoa_schema)


@router.put(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza pessoa",
    response_description="Atualiza pessoa",
)
async def update(
    pessoa_id: int,
    pessoa_schema: PPessoaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_controller.update(pessoa_id, pessoa_schema)


@router.delete(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove pessoa",
    response_description="Remove pessoa",
)
async def delete(
    pessoa_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_controller.delete(PPessoaIdSchema(pessoa_id=pessoa_id))
