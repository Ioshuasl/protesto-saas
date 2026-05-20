from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.nfse.controllers.parametros_controller import ParametrosController
from packages.v1.nfse.schemas.parametros_schema import (
    ParametrosIdSchema,
    ParametrosSaveSchema,
)

router = APIRouter()
controller = ParametrosController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista parametros",
    response_description="Lista de parametros",
)
async def index(current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.index()


@router.get(
    "/{id_parametros}",
    status_code=status.HTTP_200_OK,
    summary="Busca parametros por ID",
    response_description="Parametros localizados",
)
async def show(id_parametros: int, current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.show(ParametrosIdSchema(id_parametros=id_parametros))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra parametros",
    response_description="Parametros cadastrados",
)
async def save(data: ParametrosSaveSchema, current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.save(data)


@router.delete(
    "/{id_parametros}",
    status_code=status.HTTP_200_OK,
    summary="Exclui parametros",
    response_description="Parametros excluidos",
)
async def delete(id_parametros: int, current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.delete(ParametrosIdSchema(id_parametros=id_parametros))

