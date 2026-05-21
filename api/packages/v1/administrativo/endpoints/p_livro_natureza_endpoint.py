from typing import Optional

from fastapi import APIRouter, Depends, Query, status
from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_livro_natureza_controller import (
    PLivroNaturezaController,
)
from packages.v1.administrativo.schemas.p_livro_natureza_schema import (
    PLivroNaturezaIdSchema,
    PLivroNaturezaIndexSchema,
    PLivroNaturezaSaveSchema,
    PLivroNaturezaUpdateSchema,
)

router = APIRouter()
p_livro_natureza_controller = PLivroNaturezaController()

_PLIVRO_NATUREZA_INDEX_FILTER_KEYS = frozenset({"busca"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista naturezas de livro",
    response_description="Lista naturezas de livro",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
    busca: Optional[str] = Query(
        None,
        description="Busca unificada: LIKE em SIGLA ou DESCRICAO (OR)",
    ),
):
    filter_data = {
        k: url_params[k] for k in _PLIVRO_NATUREZA_INDEX_FILTER_KEYS if k in url_params
    }
    if busca is not None and "busca" not in filter_data:
        filter_data["busca"] = busca
    return p_livro_natureza_controller.index(
        PLivroNaturezaIndexSchema(**filter_data), query_params
    )


@router.get(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca natureza de livro pelo ID",
    response_description="Busca natureza de livro pelo ID",
)
async def show(
    livro_natureza_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_natureza_controller.show(
        PLivroNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra natureza de livro",
    response_description="Cadastra natureza de livro",
)
async def save(
    livro_natureza_schema: PLivroNaturezaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_natureza_controller.save(livro_natureza_schema)


@router.put(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza natureza de livro",
    response_description="Atualiza natureza de livro",
)
async def update(
    livro_natureza_id: int,
    livro_natureza_schema: PLivroNaturezaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_natureza_controller.update(livro_natureza_id, livro_natureza_schema)


@router.delete(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove natureza de livro",
    response_description="Remove natureza de livro",
)
async def delete(
    livro_natureza_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_livro_natureza_controller.delete(
        PLivroNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
    )
