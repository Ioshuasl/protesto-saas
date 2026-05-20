from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user

from packages.v1.administrativo.controllers.t_livro_natureza_controller import TLivroNaturezaController
from packages.v1.administrativo.schemas.t_livro_natureza_schema import (
    TLivroNaturezaIdSchema,
    TLivroNaturezaSaveSchema,
    TLivroNaturezaShowModeloSchema,
    TLivroNaturezaUpdateSchema,
)

router = APIRouter()

controller = TLivroNaturezaController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_LIVRO_NATUREZA",
    response_description="Lista todos os registros de T_LIVRO_NATUREZA",
)
async def index(current_user: dict = Depends(get_current_user)):
    return controller.index()


@router.get(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_LIVRO_NATUREZA pelo ID",
    response_description="Retorna um registro específico de T_LIVRO_NATUREZA",
)
async def show(livro_natureza_id: int, current_user: dict = Depends(get_current_user)):
    data = TLivroNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
    return controller.show(data)

@router.get(
    "/{livro_natureza_id}/modelo/{modelo}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_LIVRO_NATUREZA pelo ID",
    response_description="Retorna um registro específico de T_LIVRO_NATUREZA",
)
async def show_modelo(livro_natureza_id: int, modelo: int, current_user: dict = Depends(get_current_user)):
    data = TLivroNaturezaShowModeloSchema(livro_natureza_id=livro_natureza_id, modelo=modelo)
    return controller.show_modelo(data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo registro de T_LIVRO_NATUREZA",
    response_description="Registro criado de T_LIVRO_NATUREZA",
)
async def save(
    data: TLivroNaturezaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return controller.save(data)


@router.put(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente de T_LIVRO_NATUREZA",
    response_description="Registro atualizado de T_LIVRO_NATUREZA",
)
async def update(
    livro_natureza_id: int,
    data: TLivroNaturezaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.livro_natureza_id = livro_natureza_id
    return controller.update(data)

@router.put(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente de T_LIVRO_NATUREZA",
    response_description="Registro atualizado de T_LIVRO_NATUREZA",
)
async def update_modelo_livro(
    livro_natureza_id: int,
    data: TLivroNaturezaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.livro_natureza_id = livro_natureza_id
    return controller.update_modelo_livro(data)


@router.delete(
    "/{livro_natureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_LIVRO_NATUREZA",
    response_description="Registro removido de T_LIVRO_NATUREZA",
)
async def delete(livro_natureza_id: int, current_user: dict = Depends(get_current_user)):
    data = TLivroNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
    return controller.delete(data)

