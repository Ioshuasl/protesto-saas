from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_livro_andamento_controller import (
    PLivroAndamentoController,
)
from packages.v1.administrativo.schemas.p_livro_andamento_schema import (
    PLivroAndamentoIdSchema,
    PLivroAndamentoIndexSchema,
    PLivroAndamentoNaturezaIdSchema,
    PLivroAndamentoSaveSchema,
    PLivroAndamentoUpdateSchema,
)

router = APIRouter()
p_livro_andamento_controller = PLivroAndamentoController()

_PLIVRO_ANDAMENTO_INDEX_FILTER_KEYS = frozenset(
    {"busca", "livro_natureza_id", "aberto"}
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista livros de andamento",
    response_description="Lista livros de andamento",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
    busca: Optional[str] = Query(
        None,
        description="Busca: LIKE em SIGLA ou NUMERO_LIVRO exato",
    ),
    livro_natureza_id: Optional[int] = Query(
        None, description="Filtra por LIVRO_NATUREZA_ID"
    ),
    aberto: Optional[str] = Query(
        None,
        description="S = aberto (DATA_FECHAMENTO null); N = fechado",
    ),
):
    filter_data = {
        k: url_params[k]
        for k in _PLIVRO_ANDAMENTO_INDEX_FILTER_KEYS
        if k in url_params
    }
    if busca is not None and "busca" not in filter_data:
        filter_data["busca"] = busca
    if livro_natureza_id is not None and "livro_natureza_id" not in filter_data:
        filter_data["livro_natureza_id"] = livro_natureza_id
    if aberto is not None and "aberto" not in filter_data:
        filter_data["aberto"] = aberto
    return p_livro_andamento_controller.index(
        PLivroAndamentoIndexSchema(**filter_data), query_params
    )


@router.get(
    "/proximo-numero-livro/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Sugere próximo número de livro por natureza",
    response_description="MAX(NUMERO_LIVRO)+1 para a natureza",
)
async def proximo_numero_livro(
    livro_natureza_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_andamento_controller.proximo_numero_livro(
        PLivroAndamentoNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
    )


@router.get(
    "/{livro_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca livro de andamento pelo ID",
    response_description="Busca livro de andamento pelo ID",
)
async def show(
    livro_andamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_andamento_controller.show(
        PLivroAndamentoIdSchema(livro_andamento_id=livro_andamento_id)
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra livro de andamento",
    response_description="Cadastra livro de andamento",
)
async def save(
    livro_andamento_schema: PLivroAndamentoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_andamento_controller.save(livro_andamento_schema)


@router.put(
    "/{livro_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza livro de andamento",
    response_description="Atualiza livro de andamento",
)
async def update(
    livro_andamento_id: int,
    livro_andamento_schema: PLivroAndamentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_andamento_controller.update(
        livro_andamento_id, livro_andamento_schema
    )


@router.delete(
    "/{livro_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove livro de andamento",
    response_description="Remove livro de andamento",
)
async def delete(
    livro_andamento_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_andamento_controller.delete(
        PLivroAndamentoIdSchema(livro_andamento_id=livro_andamento_id)
    )
