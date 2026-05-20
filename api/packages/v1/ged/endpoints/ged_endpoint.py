from fastapi import APIRouter, Depends, Request, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.ged.controllers.ged_controller import GEDController
from packages.v1.ged.schemas.ged_schema import (
    GEDIndexSchema,
    GEDPathSchema,
    GEDSaveBase64RequestSchema,
    GEDSaveMultipartRequestSchema,
    GEDSaveSchema,
)

router = APIRouter()
Controller = GEDController()


@router.get(
    "/{serventia}/{pasta}/{registro_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca itens com filtros opcionais",
    response_description="Lista de itens encontrados com base nos criterios de busca.",
)
async def index(
    serventia: int,
    pasta: str,
    registro_id: str,
    current_user: dict = Depends(get_current_user),
):
    del current_user
    response = Controller.index(
        GEDIndexSchema(serventia=int(serventia), pasta=pasta, registro_id=registro_id)
    )
    return response


@router.post(
    "/{serventia}/{pasta}/{registro_id}/base64",
    status_code=status.HTTP_201_CREATED,
    summary="Salva arquivo GED via base64",
    response_description="Arquivo salvo com sucesso no GED.",
)
async def save_base64(
    serventia: int,
    pasta: str,
    registro_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    del current_user
    input_schema = GEDSaveBase64RequestSchema(
        path=GEDPathSchema(
            serventia=int(serventia),
            pasta=str(pasta),
            registro_id=str(registro_id),
        ),
        request=request,
    )
    response = await Controller.save_base64(input_schema)
    return response


@router.post(
    "/{serventia}/{pasta}/{registro_id}/multipart",
    status_code=status.HTTP_201_CREATED,
    summary="Salva arquivo GED via multipart/form-data",
    response_description="Arquivo salvo com sucesso no GED.",
)
async def save_multipart(
    serventia: int,
    pasta: str,
    registro_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user),
):
    del current_user
    input_schema = GEDSaveMultipartRequestSchema(
        path=GEDPathSchema(
            serventia=int(serventia),
            pasta=str(pasta),
            registro_id=str(registro_id),
        ),
        request=request,
    )
    response = await Controller.save_multipart(input_schema)
    return response


@router.post(
    "/{serventia}/{pasta}",
    status_code=status.HTTP_201_CREATED,
    summary="Salva arquivo GED (legado)",
    response_description="Arquivo salvo com payload legado.",
    deprecated=True,
)
async def save(
    serventia: int,
    pasta: str,
    data: GEDSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    del current_user
    data.serventia = int(serventia)
    data.pasta = str(pasta)
    response = Controller.save(data)
    return response


@router.delete(
    "/{serventia}/{pasta}/{registro_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca itens com filtros opcionais",
    response_description="Lista de itens encontrados com base nos criterios de busca.",
)
async def delete(
    serventia: int,
    pasta: str,
    registro_id: str,
    current_user: dict = Depends(get_current_user),
):
    del current_user
    response = Controller.delete(
        GEDIndexSchema(serventia=int(serventia), pasta=pasta, registro_id=registro_id)
    )
    return response
