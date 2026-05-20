from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_selo_livro_controller import (
    GSeloLivroController,
)
from packages.v1.administrativo.schemas.g_selo_livro_schema import (
    GSeloLivroIdSchema,
    GSeloLivroSaveSchema,
    GSeloLivroUpdateSchema,
)


router = APIRouter()
controller = GSeloLivroController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Listar selos de livro",
    response_description="Selos de livro localizados com sucesso.",
)
async def index(current_user: dict = Depends(get_current_user)):
    return controller.index()


@router.get(
    "/{selo_livro_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar selo de livro por ID",
    response_description="Selo de livro localizado com sucesso.",
)
async def show(selo_livro_id: int, current_user: dict = Depends(get_current_user)):
    data = GSeloLivroIdSchema(selo_livro_id=selo_livro_id)
    return controller.show(data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar selo de livro",
    response_description="Selo de livro cadastrado com sucesso.",
)
async def save(
    data: GSeloLivroSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return controller.save(data)


@router.put(
    "/{selo_livro_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar selo de livro",
    response_description="Selo de livro atualizado com sucesso.",
)
async def update(
    selo_livro_id: int,
    data: GSeloLivroUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.selo_livro_id = selo_livro_id
    return controller.update(data)


@router.delete(
    "/{selo_livro_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover selo de livro",
    response_description="Selo de livro removido com sucesso.",
)
async def delete(selo_livro_id: int, current_user: dict = Depends(get_current_user)):
    data = GSeloLivroIdSchema(selo_livro_id=selo_livro_id)
    return controller.delete(data)
