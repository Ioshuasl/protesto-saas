from typing import Optional

from fastapi import APIRouter, Depends, Query, status

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_titulo_controller import PTituloController
from packages.v1.administrativo.schemas.p_titulo_schema import (
    PTituloIdSchema,
    PTituloIndexSchema,
    PTituloSaveSchema,
    PTituloUpdateSchema,
)

router = APIRouter()
p_titulo_controller = PTituloController()

_PTITULO_INDEX_FILTER_KEYS = frozenset(
    {
        "busca_pessoa",
        "numero_apontamento",
        "nosso_numero",
        "numero_titulo",
        "numero_titulo_banco",
        "ocorrencia_id",
        "ocorrencia_andamento_id",
        "banco_id",
        "especie_id",
    }
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista títulos de protesto",
    response_description="Lista títulos de protesto com paginação",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
    busca_pessoa: Optional[str] = Query(
        None,
        description="Busca em P_PESSOA_VINCULO (nome/cpfcnpj) e P_PESSOA vinculada",
    ),
    numero_apontamento: Optional[float] = Query(
        None, description="Número de apontamento (igualdade)"
    ),
    nosso_numero: Optional[str] = Query(None, description="Nosso número (LIKE)"),
    numero_titulo: Optional[str] = Query(None, description="Número do título (LIKE)"),
    numero_titulo_banco: Optional[str] = Query(
        None, description="Número do título no banco (LIKE)"
    ),
    ocorrencia_id: Optional[int] = Query(
        None, description="FK P_OCORRENCIAS (opcional — omitir para listar todas)"
    ),
    ocorrencia_andamento_id: Optional[int] = Query(
        None, description="FK P_OCORRENCIA_ANDAMENTO"
    ),
    banco_id: Optional[int] = Query(
        None, description="FK P_BANCO — filtra por BANCO_ID (opcional)"
    ),
    especie_id: Optional[int] = Query(None, description="FK P_ESPECIE"),
):
    filter_data = {
        key: url_params[key]
        for key in _PTITULO_INDEX_FILTER_KEYS
        if key in url_params
    }
    return p_titulo_controller.index(PTituloIndexSchema(**filter_data), query_params)


@router.get(
    "/{titulo_id}/selos",
    status_code=status.HTTP_200_OK,
    summary="Lista selos vinculados ao título",
    response_description="Selos de G_SELO_LIVRO e G_SELO_LIVRO_ANTIGO ligados ao P_TITULO",
)
async def selos(
    titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_titulo_controller.selos(PTituloIdSchema(titulo_id=titulo_id))


@router.get(
    "/{titulo_id}/",
    status_code=status.HTTP_200_OK,
    summary="Busca título pelo ID",
    response_description="Busca título pelo ID",
)
async def show(
    titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_titulo_controller.show(PTituloIdSchema(titulo_id=titulo_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra título",
    response_description="Cadastra título",
)
async def save(
    titulo_schema: PTituloSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_titulo_controller.save(titulo_schema)


@router.put(
    "/{titulo_id}/",
    status_code=status.HTTP_200_OK,
    summary="Atualiza título",
    response_description="Atualiza título",
)
async def update(
    titulo_id: int,
    titulo_schema: PTituloUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_titulo_controller.update(titulo_id, titulo_schema)


@router.delete(
    "/{titulo_id}/",
    status_code=status.HTTP_200_OK,
    summary="Remove título",
    response_description="Remove título",
)
async def delete(
    titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_titulo_controller.delete(PTituloIdSchema(titulo_id=titulo_id))
