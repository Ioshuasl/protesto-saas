# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_cidade_controller import GCidadeController
from packages.v1.administrativo.schemas.g_cidade_schema import (
    GCidadeIndexSchema,
    GCidadeSaveSchema,
    GCidadeUpdateSchema,
    GCidadeIdSchema,
    GCidadeNomeSchema,
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_cidade_controller = GCidadeController()


# Lista todos os registros de cidade
@router.get(
    "/{uf}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de cidade cadastrados",
    response_description="Lista todos os registros de cidade cadastrados",
)
async def index(uf: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    data = GCidadeIndexSchema(uf=uf)

    # Busca todos os registros de cidade cadastrados
    response = g_cidade_controller.index(data)

    # Retorna os dados localizados
    return response


# Localiza um registro de cidade pelo nome (CIDADE_NOME)
@router.get(
    "/nome",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de cidade em específico pelo nome",
    response_description="Busca um registro de cidade em específico",
)
async def get_by_nome(cidade_nome: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    g_cidade_schema = GCidadeNomeSchema(cidade_nome=cidade_nome)

    # Busca um registro de cidade específico pelo nome
    response = g_cidade_controller.get_by_nome(g_cidade_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de cidade pelo ID
@router.get(
    "/{cidade_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de cidade em específico pelo ID",
    response_description="Busca um registro de cidade em específico",
)
async def show(cidade_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    g_cidade_schema = GCidadeIdSchema(cidade_id=cidade_id)

    # Busca um registro de cidade específico pelo ID
    response = g_cidade_controller.show(g_cidade_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de cidade
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um registro de cidade",
    response_description="Cadastra um registro de cidade",
)
async def save(
    g_cidade_schema: GCidadeSaveSchema, current_user: dict = Depends(get_current_user)
):

    # Efetua o cadastro no banco de dados
    response = g_cidade_controller.save(g_cidade_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de cidade
@router.put(
    "/{cidade_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de cidade",
    response_description="Atualiza um registro de cidade",
)
async def update(
    cidade_id: int,
    g_cidade_schema: GCidadeUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua a atualização dos dados
    response = g_cidade_controller.update(cidade_id, g_cidade_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado registro de cidade
@router.delete(
    "/{cidade_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de cidade",
    response_description="Remove um registro de cidade",
)
async def delete(cidade_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    g_cidade_schema = GCidadeIdSchema(cidade_id=cidade_id)

    # Efetua a exclusão do registro de cidade
    response = g_cidade_controller.delete(g_cidade_schema)

    # Retorna os dados localizados
    return response
