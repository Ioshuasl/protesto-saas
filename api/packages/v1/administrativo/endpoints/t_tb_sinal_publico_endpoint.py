from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_tb_sinal_publico_controller import (
    TTbSinalPublicoController,
)
from packages.v1.administrativo.schemas.t_tb_sinal_publico_schema import (
    TTbSinalPublicoDescricaoSchema,
    TTbSinalPublicoIdSchema,
    TTbSinalPublicoSaveSchema,
    TTbSinalPublicoUpdateSchema,
)

router = APIRouter()
t_tb_sinal_publico_controller = TTbSinalPublicoController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os sinais publicos cadastrados",
    response_description="Lista todos os sinais publicos cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):
    return t_tb_sinal_publico_controller.index()


@router.get(
    "/descricao",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico pela descricao",
    response_description="Busca um registro em especifico",
)
async def get_by_descricao(
    descricao: str, current_user: dict = Depends(get_current_user)
):
    sinal_publico_schema = TTbSinalPublicoDescricaoSchema(descricao=descricao)
    return t_tb_sinal_publico_controller.get_by_descricao(sinal_publico_schema)


@router.get(
    "/{tb_sinalpublico_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico pelo ID do sinal publico",
    response_description="Busca um registro em especifico",
)
async def show(tb_sinalpublico_id: int, current_user: dict = Depends(get_current_user)):
    sinal_publico_schema = TTbSinalPublicoIdSchema(
        tb_sinalpublico_id=tb_sinalpublico_id
    )
    return t_tb_sinal_publico_controller.show(sinal_publico_schema)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um sinal publico",
    response_description="Cadastra um sinal publico",
)
async def save(
    sinal_publico_schema: TTbSinalPublicoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return t_tb_sinal_publico_controller.save(sinal_publico_schema)


@router.put(
    "/{tb_sinalpublico_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um sinal publico",
    response_description="Atualiza um sinal publico",
)
async def update(
    tb_sinalpublico_id: int,
    sinal_publico_schema: TTbSinalPublicoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return t_tb_sinal_publico_controller.update(
        tb_sinalpublico_id, sinal_publico_schema
    )


@router.delete(
    "/{tb_sinalpublico_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um sinal publico",
    response_description="Remove um sinal publico",
)
async def delete(
    tb_sinalpublico_id: int, current_user: dict = Depends(get_current_user)
):
    sinal_publico_schema = TTbSinalPublicoIdSchema(
        tb_sinalpublico_id=tb_sinalpublico_id
    )
    return t_tb_sinal_publico_controller.delete(sinal_publico_schema)
