from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.nfse.controllers.nfse_controller import NfseController
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema, NfseSaveSchema

router = APIRouter()
controller = NfseController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista NFS-e",
    response_description="Lista de NFS-e encontradas",
)
async def index(current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.index()


@router.get(
    "/{id_nfse}",
    status_code=status.HTTP_200_OK,
    summary="Busca NFS-e por ID",
    response_description="NFS-e localizada",
)
async def show(id_nfse: int, current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.show(NfseIdSchema(id_nfse=id_nfse))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra NFS-e",
    response_description="NFS-e cadastrada",
)
async def save(data: NfseSaveSchema, current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.save(data)


@router.delete(
    "/{id_nfse}",
    status_code=status.HTTP_200_OK,
    summary="Exclui NFS-e",
    response_description="NFS-e excluida",
)
async def delete(id_nfse: int, current_user: dict = Depends(get_current_user)):
    del current_user
    return controller.delete(NfseIdSchema(id_nfse=id_nfse))
