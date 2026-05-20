from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_pessoa_sinal_publico_controller import (
    TPessoaSinalPublicoController,
)
from packages.v1.administrativo.schemas.t_pessoa_sinal_publico_schema import (
    TPessoaSinalPublicoIdSchema,
    TPessoaSinalPublicoSaveSchema,
    TPessoaSinalPublicoSchema,
    TPessoaSinalPublicoUpdateSchema,
)

router = APIRouter()
t_pessoa_sinal_publico_controller = TPessoaSinalPublicoController()


@router.get(
    "/pessoa/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os sinais publicos por pessoa cadastrados",
    response_description="Lista todos os sinais publicos por pessoa cadastrados",
)
async def index(pessoa_id: int, current_user: dict = Depends(get_current_user)):
    data = TPessoaSinalPublicoSchema(pessoa_id=pessoa_id)
    return t_pessoa_sinal_publico_controller.index(data)


@router.get(
    "/{pessoa_sinalpublico_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico pelo ID do sinal publico por pessoa",
    response_description="Busca um registro em especifico",
)
async def show(
    pessoa_sinalpublico_id: int, current_user: dict = Depends(get_current_user)
):
    pessoa_sinal_publico_schema = TPessoaSinalPublicoIdSchema(
        pessoa_sinalpublico_id=pessoa_sinalpublico_id
    )
    return t_pessoa_sinal_publico_controller.show(pessoa_sinal_publico_schema)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um sinal publico para pessoa",
    response_description="Cadastra um sinal publico para pessoa",
)
async def save(
    pessoa_sinal_publico_schema: TPessoaSinalPublicoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return t_pessoa_sinal_publico_controller.save(pessoa_sinal_publico_schema)


@router.put(
    "/{pessoa_sinalpublico_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um sinal publico por pessoa",
    response_description="Atualiza um sinal publico por pessoa",
)
async def update(
    pessoa_sinalpublico_id: int,
    pessoa_sinal_publico_schema: TPessoaSinalPublicoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return t_pessoa_sinal_publico_controller.update(
        pessoa_sinalpublico_id,
        pessoa_sinal_publico_schema,
    )


@router.delete(
    "/{pessoa_sinalpublico_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um sinal publico por pessoa",
    response_description="Remove um sinal publico por pessoa",
)
async def delete(
    pessoa_sinalpublico_id: int, current_user: dict = Depends(get_current_user)
):
    pessoa_sinal_publico_schema = TPessoaSinalPublicoIdSchema(
        pessoa_sinalpublico_id=pessoa_sinalpublico_id
    )
    return t_pessoa_sinal_publico_controller.delete(pessoa_sinal_publico_schema)
