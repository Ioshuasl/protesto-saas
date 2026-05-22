from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_pessoa_vinculo_controller import (
    PPessoaVinculoController,
)
from packages.v1.administrativo.schemas.p_pessoa_vinculo_schema import (
    PPessoaVinculoIdSchema,
    PPessoaVinculoIndexSchema,
    PPessoaVinculoSaveSchema,
    PPessoaVinculoUpdateSchema,
)

router = APIRouter()
p_pessoa_vinculo_controller = PPessoaVinculoController()

_PPESSOA_VINCULO_INDEX_FILTER_KEYS = frozenset(
    {
        "titulo_id",
        "pessoa_id",
        "tipo_vinculo",
        "nome",
        "cpfcnpj",
        "busca",
    }
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista vínculos de pessoa",
    response_description="Lista vínculos de pessoa com paginação",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
    titulo_id: Optional[int] = Query(None, description="FK P_TITULO"),
    pessoa_id: Optional[int] = Query(None, description="FK P_PESSOA"),
    tipo_vinculo: Optional[str] = Query(
        None,
        description="APRESENTANTE, CEDENTE, CREDOR ou DEVEDOR",
    ),
    nome: Optional[str] = Query(None, description="LIKE em NOME"),
    cpfcnpj: Optional[str] = Query(None, description="LIKE em CPFCNPJ"),
    busca: Optional[str] = Query(
        None, description="LIKE em NOME ou CPFCNPJ (OR)"
    ),
):
    filter_data = {
        key: url_params[key]
        for key in _PPESSOA_VINCULO_INDEX_FILTER_KEYS
        if key in url_params
    }
    for key, value in {
        "titulo_id": titulo_id,
        "pessoa_id": pessoa_id,
        "tipo_vinculo": tipo_vinculo,
        "nome": nome,
        "cpfcnpj": cpfcnpj,
        "busca": busca,
    }.items():
        if value is not None and key not in filter_data:
            filter_data[key] = value
    return p_pessoa_vinculo_controller.index(
        PPessoaVinculoIndexSchema(**filter_data), query_params
    )


@router.get(
    "/{pessoa_vinculo_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca vínculo de pessoa pelo ID",
    response_description="Busca vínculo de pessoa pelo ID",
)
async def show(
    pessoa_vinculo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_vinculo_controller.show(
        PPessoaVinculoIdSchema(pessoa_vinculo_id=pessoa_vinculo_id)
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra vínculo de pessoa",
    response_description="Cadastra vínculo de pessoa",
)
async def save(
    vinculo_schema: PPessoaVinculoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_vinculo_controller.save(vinculo_schema)


@router.put(
    "/{pessoa_vinculo_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza vínculo de pessoa",
    response_description="Atualiza vínculo de pessoa",
)
async def update(
    pessoa_vinculo_id: int,
    vinculo_schema: PPessoaVinculoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_vinculo_controller.update(pessoa_vinculo_id, vinculo_schema)


@router.delete(
    "/{pessoa_vinculo_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove vínculo de pessoa",
    response_description="Remove vínculo de pessoa",
)
async def delete(
    pessoa_vinculo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_pessoa_vinculo_controller.delete(
        PPessoaVinculoIdSchema(pessoa_vinculo_id=pessoa_vinculo_id)
    )
