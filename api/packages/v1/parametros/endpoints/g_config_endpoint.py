from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.parametros.controllers.g_config_controller import GConfigController
from packages.v1.parametros.schemas.g_config_schema import (
    GConfigIdSchema,
    GConfigIndexFilterSchema,
    GConfigSaveSchema,
)

router = APIRouter()
controller = GConfigController()


@router.get(
    "/{sistema_id}/{descricao}/{secao}",
    status_code=status.HTTP_200_OK,
    summary="Lista configuracoes G_CONFIG",
    response_description="Lista de configuracoes",
)
async def index(
    sistema_id: float,
    secao: str,
    descricao: str,
    current_user: dict = Depends(get_current_user),
):
    filter_schema = GConfigIndexFilterSchema(
        sistema_id=sistema_id,
        secao=secao,
        descricao=descricao,
    )

    response = controller.index(filter_schema)
    return response


@router.get(
    "/{config_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca configuracao G_CONFIG por ID",
    response_description="Configuracao localizada",
)
async def show(config_id: float, current_user: dict = Depends(get_current_user)):
    g_config_schema = GConfigIdSchema(config_id=config_id)
    response = controller.show(g_config_schema)
    return response


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Salva configuracao G_CONFIG",
    response_description="Configuracao salva",
)
async def save(data: GConfigSaveSchema, current_user: dict = Depends(get_current_user)):
    response = controller.save(data)
    return response


@router.delete(
    "/{config_id}",
    status_code=status.HTTP_200_OK,
    summary="Exclui configuracao G_CONFIG",
    response_description="Configuracao excluida",
)
async def delete(config_id: float, current_user: dict = Depends(get_current_user)):
    g_config_schema = GConfigIdSchema(config_id=config_id)

    response = controller.delete(g_config_schema)
    return response
