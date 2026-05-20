# Importacao de bibliotecas
from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_minuta_controller import TMinutaController
from packages.v1.administrativo.schemas.t_minuta_schema import (
    TMinutaDescricaoSchema,
    TMinutaIdSchema,
    TMinutaSaveSchema,
    TMinutaUpdateSchema,
    TMinutaUpdateTextoSchema,
)

# Inicializa o roteador para as rotas de minuta
router = APIRouter()

# Instanciamento do controller desejado
t_minuta_controller = TMinutaController()

# Lista todos os registros de minuta
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de minuta cadastrados",
    response_description="Lista todos os registros de minuta cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):
    # Busca todos os registros de minuta cadastrados
    response = t_minuta_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de minuta pela descricao
@router.get(
    "/descricao",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de minuta em especifico pela descricao",
    response_description="Busca um registro de minuta em especifico",
)
async def get_by_descricao(descricao: str, current_user: dict = Depends(get_current_user)):
    minuta_schema = TMinutaDescricaoSchema(descricao=descricao)

    # Efetua a busca por descricao
    response = t_minuta_controller.get_by_descricao(minuta_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de minuta pelo ID
@router.get(
    "/{minuta_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de minuta em especifico pelo ID",
    response_description="Busca um registro de minuta em especifico",
)
async def show(minuta_id: int, current_user: dict = Depends(get_current_user)):

    minuta_schema = TMinutaIdSchema(minuta_id=minuta_id)

    # Efetua a busca por ID
    response = t_minuta_controller.show(minuta_schema)

    # Retorna os dados localizados
    return response

# Localiza um registro de minuta pelo ID
@router.get(
    "/{minuta_id}/texto",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de minuta em especifico pelo ID",
    response_description="Busca um registro de minuta em especifico",
)
async def show_texto(minuta_id: int, current_user: dict = Depends(get_current_user)):

    minuta_schema = TMinutaIdSchema(minuta_id=minuta_id)

    # Efetua a busca por ID
    response = t_minuta_controller.show_texto(minuta_schema)

    # Retorna os dados localizados
    return response


# Cadastra um registro de minuta
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um registro de minuta",
    response_description="Cadastra um registro de minuta",
)
async def save(minuta_schema: TMinutaSaveSchema, current_user: dict = Depends(get_current_user)):
    # Efetua o cadastro no banco de dados
    response = t_minuta_controller.save(minuta_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de minuta
@router.put(
    "/{minuta_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de minuta",
    response_description="Atualiza um registro de minuta",
)
async def update(
    minuta_id: int,
    minuta_schema: TMinutaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    minuta_id_schema = TMinutaIdSchema(minuta_id=minuta_id)

    # Efetua a atualizacao dos dados
    response = t_minuta_controller.update(minuta_id_schema, minuta_schema)

    # Retorna os dados localizados
    return response

# Atualiza os dados de um registro de minuta
@router.put(
    "/{minuta_id}/texto",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de minuta",
    response_description="Atualiza um registro de minuta",
)
async def update_texto(
    minuta_id: int,
    minuta_schema: TMinutaUpdateTextoSchema,
    current_user: dict = Depends(get_current_user),
):

    minuta_schema = minuta_schema.model_copy(update={"minuta_id": minuta_id})

    # Efetua a atualizacao dos dados
    response = t_minuta_controller.update_texto(minuta_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado registro de minuta
@router.delete(
    "/{minuta_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de minuta",
    response_description="Remove um registro de minuta",
)
async def delete(minuta_id: int, current_user: dict = Depends(get_current_user)):
    # Cria o schema com os dados recebidos
    minuta_schema = TMinutaIdSchema(minuta_id=minuta_id)

    # Efetua a exclusao do registro
    response = t_minuta_controller.delete(minuta_schema)

    # Retorna os dados localizados
    return response
