from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.schemas.g_tb_txmodelogrupo_schema import (
    GTbTxmodelogrupoSaveSchema,
    GTbTxmodelogrupoUpdateSchema,
    GTbTxmodelogrupoDescricaoSchema,
    GTbTxmodelogrupoIdSchema
)
from packages.v1.administrativo.controllers.g_tb_txmodelogrupo_controller import GTbTxmodelogrupoController

router = APIRouter()

g_tb_txmodelogrupo_controller = GTbTxmodelogrupoController()

@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Lista todos os grupos de modelo de texto cadastrados',
    response_description='Lista todos os grupos de modelo de texto cadastrados'
)
async def index(current_user: dict = Depends(get_current_user)):
    response = g_tb_txmodelogrupo_controller.index()
    return response

@router.get(
    '/descricao',
    status_code=status.HTTP_200_OK,
    summary='Busca um grupo de modelo de texto pela descrição',
    response_description='Busca um grupo de modelo de texto pela descrição'
)
async def get_by_descricao(descricao: str, current_user: dict = Depends(get_current_user)):
    txmodelogrupo_schema = GTbTxmodelogrupoDescricaoSchema(descricao=descricao)
    response = g_tb_txmodelogrupo_controller.get_by_descricao(txmodelogrupo_schema)
    return response

@router.get(
    '/{tb_txmodelogrupo_id}',
    status_code=status.HTTP_200_OK,
    summary='Busca um grupo de modelo de texto pelo ID',
    response_description='Busca um grupo de modelo de texto pelo ID'
)
async def show(tb_txmodelogrupo_id: int, current_user: dict = Depends(get_current_user)):
    txmodelogrupo_schema = GTbTxmodelogrupoIdSchema(tb_txmodelogrupo_id=tb_txmodelogrupo_id)
    response = g_tb_txmodelogrupo_controller.show(txmodelogrupo_schema)
    return response

@router.post(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Cadastra um novo grupo de modelo de texto',
    response_description='Cadastra um novo grupo de modelo de texto'
)
async def save(txmodelogrupo_schema: GTbTxmodelogrupoSaveSchema, current_user: dict = Depends(get_current_user)):
    response = g_tb_txmodelogrupo_controller.save(txmodelogrupo_schema)
    return response

@router.put(
    '/{tb_txmodelogrupo_id}',
    status_code=status.HTTP_200_OK,
    summary='Atualiza um grupo de modelo de texto',
    response_description='Atualiza um grupo de modelo de texto'
)
async def update(tb_txmodelogrupo_id: int, txmodelogrupo_schema: GTbTxmodelogrupoUpdateSchema, current_user: dict = Depends(get_current_user)):
    response = g_tb_txmodelogrupo_controller.update(tb_txmodelogrupo_id, txmodelogrupo_schema)
    return response

@router.delete(
    '/{tb_txmodelogrupo_id}',
    status_code=status.HTTP_200_OK,
    summary='Remove um grupo de modelo de texto',
    response_description='Remove um grupo de modelo de texto'
)
async def delete(tb_txmodelogrupo_id: int, current_user: dict = Depends(get_current_user)):
    txmodelogrupo_schema = GTbTxmodelogrupoIdSchema(tb_txmodelogrupo_id=tb_txmodelogrupo_id)
    response = g_tb_txmodelogrupo_controller.delete(txmodelogrupo_schema)
    return response