# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.c_caixa_item_controller import (
    CCaixaItemController,
)
from packages.v1.administrativo.schemas.c_caixa_item_schema import CaixaItemSchema

# Inicializar o roteaodr para as rotas de produtos
router = APIRouter()

# Instãnciamento do controller desejado
cCaixaItemController = CCaixaItemController()


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Busca itens com filtros opcionais",
    response_description="Lista de itens encontrados com base nos critérios de busca.",
)
async def index(current_user: dict = Depends(get_current_user)):
    # Busca todos os produtos cadastrados
    response = cCaixaItemController.index()

    # Retornar os dados localizados
    return response


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar uma nova receita ou despesa no sistema",
    response_description="Confirmação do cadastro da receita ou despesa, incluindo detalhes do item criado.",
)
async def save(
    caixa_item_schema: CaixaItemSchema, current_user: dict = Depends(get_current_user)
):

    # Salva o produto desejado
    response = cCaixaItemController.create(caixa_item_schema)

    # Retorna a informação desejada
    return response


@router.put(
    "/{caixa_item_id}",
    status_code=status.HTTP_201_CREATED,
    summary="Atualiza uma nova receita ou despesa no sistema",
    response_description="Confirmação de atualização da receita ou despesa, incluindo detalhes do item criado.",
)
async def update(
    caixa_item_id: int,
    caixa_item_schema: CaixaItemSchema,
    current_user: dict = Depends(get_current_user),
):

    # Salva o produto desejado
    response = cCaixaItemController.update(caixa_item_id, caixa_item_schema)

    # Retorna a informação desejada
    return response


@router.get(
    "/{caixa_item_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em específico",
    response_description="Busca um registro de acordo com o ID informado",
)
async def show(caixa_item_id: int, current_user: dict = Depends(get_current_user)):

    # Armazena o produto id no Schema
    CaixaItemSchema.caixa_item_id = caixa_item_id

    # Salva o produto desejado
    response = cCaixaItemController.show(CaixaItemSchema)

    # Retorna a informação desejada
    return response


@router.delete(
    "/{caixa_item_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro em específico",
    response_description="Remove um registro de acordo com o ID informado",
)
async def delete(caixa_item_id: int, current_user: dict = Depends(get_current_user)):

    # Armazena o produto id no Schema
    CaixaItemSchema.caixa_item_id = caixa_item_id

    # Salva o produto desejado
    response = cCaixaItemController.delete(CaixaItemSchema)

    # Retorna a informação desejada
    return response
