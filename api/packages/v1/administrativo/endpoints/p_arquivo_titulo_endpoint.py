from typing import Optional

from urllib.parse import quote

from fastapi import APIRouter, Depends, Query, status
from fastapi.responses import Response

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_arquivo_titulo_controller import (
    PArquivoTituloController,
)
from packages.v1.administrativo.schemas.p_arquivo_titulo_schema import (
    PArquivoTituloIdSchema,
    PArquivoTituloIndexSchema,
    PArquivoTituloSaveSchema,
    PArquivoTituloShowSchema,
    PArquivoTituloUpdateSchema,
    parse_arquivo_titulo_includes,
)

router = APIRouter()
p_arquivo_titulo_controller = PArquivoTituloController()

_PARQUIVO_TITULO_INDEX_FILTER_KEYS = frozenset(
    {"nome_arquivo", "portador_codigo", "codigo_praca", "data_inicio", "data_fim"}
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista arquivos de título CRA",
    response_description="Lista arquivos de título CRA",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
    include: Optional[str] = Query(
        None,
        description="Relacionamentos: titulos (somente numero_apontamento de P_TITULO)",
    ),
):
    filter_data = {
        key: url_params[key]
        for key in _PARQUIVO_TITULO_INDEX_FILTER_KEYS
        if key in url_params
    }
    return p_arquivo_titulo_controller.index(
        PArquivoTituloIndexSchema(
            **filter_data,
            includes=parse_arquivo_titulo_includes(include),
        ),
        query_params,
    )


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra arquivo de título CRA",
    response_description="Cadastra arquivo de título CRA",
)
async def save(
    arquivo_schema: PArquivoTituloSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_arquivo_titulo_controller.save(arquivo_schema)


@router.get(
    "/{arquivo_titulo_id}/texto/",
    status_code=status.HTTP_200_OK,
    summary="Retorna BLOB TEXTO do arquivo",
    response_description="Conteúdo da coluna TEXTO",
)
async def show_texto(
    arquivo_titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_arquivo_titulo_controller.show_texto(
        PArquivoTituloIdSchema(arquivo_titulo_id=arquivo_titulo_id)
    )


@router.get(
    "/{arquivo_titulo_id}/download/",
    status_code=status.HTTP_200_OK,
    summary="Baixa o arquivo importado (TEXTO_IMPORTADO)",
    response_description="Arquivo de remessa com nome NOME_ARQUIVO",
)
async def download(
    arquivo_titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    payload = p_arquivo_titulo_controller.download(
        PArquivoTituloIdSchema(arquivo_titulo_id=arquivo_titulo_id)
    )
    filename = str(payload["filename"])
    content = payload["content"]
    ascii_filename = filename.encode("ascii", "ignore").decode("ascii") or "arquivo.rem"
    encoded_filename = quote(filename)

    return Response(
        content=content,
        media_type="text/plain; charset=iso-8859-1",
        headers={
            "Content-Disposition": (
                f'attachment; filename="{ascii_filename}"; '
                f"filename*=UTF-8''{encoded_filename}"
            ),
            "Content-Length": str(len(content)),
        },
    )


@router.get(
    "/{arquivo_titulo_id}/texto_importado/",
    status_code=status.HTTP_200_OK,
    summary="Retorna BLOB TEXTO_IMPORTADO do arquivo",
    response_description="Conteúdo da coluna TEXTO_IMPORTADO",
)
async def show_texto_importado(
    arquivo_titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_arquivo_titulo_controller.show_texto_importado(
        PArquivoTituloIdSchema(arquivo_titulo_id=arquivo_titulo_id)
    )


@router.get(
    "/{arquivo_titulo_id}/",
    status_code=status.HTTP_200_OK,
    summary="Busca arquivo de título pelo ID",
    response_description="Busca arquivo de título pelo ID",
)
async def show(
    arquivo_titulo_id: int,
    include: Optional[str] = Query(
        None,
        description="Relacionamentos: titulos (P_TITULO por ARQUIVO_TITULO_ID)",
    ),
    current_user: dict = Depends(get_current_user),
):
    return p_arquivo_titulo_controller.show(
        PArquivoTituloShowSchema.from_id(arquivo_titulo_id, include=include)
    )


@router.put(
    "/{arquivo_titulo_id}/",
    status_code=status.HTTP_200_OK,
    summary="Atualiza arquivo de título CRA",
    response_description="Atualiza arquivo de título CRA",
)
async def update(
    arquivo_titulo_id: int,
    arquivo_schema: PArquivoTituloUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_arquivo_titulo_controller.update(arquivo_titulo_id, arquivo_schema)


@router.delete(
    "/{arquivo_titulo_id}/",
    status_code=status.HTTP_200_OK,
    summary="Remove arquivo de título CRA",
    response_description="Remove arquivo de título CRA",
)
async def delete(
    arquivo_titulo_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_arquivo_titulo_controller.delete(
        PArquivoTituloIdSchema(arquivo_titulo_id=arquivo_titulo_id)
    )
