from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_livro_andamento_controller import (
    TLivroAndamentoController,
)
from packages.v1.administrativo.schemas.t_livro_andamento_schema import (
    TLivroAndamentoIdSchema,
    TLivroAndamentoNaturezaIdSchema,
    TLivroAndamentoSaveSchema,
    TLivroAndamentoUpdateSchema,
)

router = APIRouter()
controller = TLivroAndamentoController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_LIVRO_ANDAMENTO",
    response_description="Lista todos os registros de T_LIVRO_ANDAMENTO",
)
async def index(current_user: dict = Depends(get_current_user)):
    return controller.index()


@router.get(
    "/livro-natureza/{livro_natureza_id}/abertos/first",
    status_code=status.HTTP_200_OK,
    summary="Busca o primeiro livro de andamento aberto por LIVRO_NATUREZA_ID",
    response_description="Primeiro livro de andamento aberto filtrado por LIVRO_NATUREZA_ID",
)
async def first_aberto_by_natureza(
    livro_natureza_id: int,
    current_user: dict = Depends(get_current_user),
):
    data = TLivroAndamentoNaturezaIdSchema(livro_natureza_id=livro_natureza_id)
    return controller.first_aberto_by_natureza(data)


@router.get(
    "/{livro_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_LIVRO_ANDAMENTO pelo ID",
    response_description="Retorna um registro especifico de T_LIVRO_ANDAMENTO",
)
async def show(livro_andamento_id: int, current_user: dict = Depends(get_current_user)):
    data = TLivroAndamentoIdSchema(livro_andamento_id=livro_andamento_id)
    return controller.show(data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria um novo registro de T_LIVRO_ANDAMENTO",
    response_description="Registro criado de T_LIVRO_ANDAMENTO",
)
async def save(data: TLivroAndamentoSaveSchema, current_user: dict = Depends(get_current_user)):
    return controller.save(data)


@router.put(
    "/{livro_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente de T_LIVRO_ANDAMENTO",
    response_description="Registro atualizado de T_LIVRO_ANDAMENTO",
)
async def update(
    livro_andamento_id: int,
    data: TLivroAndamentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.livro_andamento_id = livro_andamento_id
    return controller.update(data)


@router.delete(
    "/{livro_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_LIVRO_ANDAMENTO",
    response_description="Registro removido de T_LIVRO_ANDAMENTO",
)
async def delete(livro_andamento_id: int, current_user: dict = Depends(get_current_user)):
    data = TLivroAndamentoIdSchema(livro_andamento_id=livro_andamento_id)
    return controller.delete(data)
