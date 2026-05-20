# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_natureza_controller import GNaturezaController
from packages.v1.administrativo.schemas.g_natureza_schema import (
    GNaturezaSchema,
    GNaturezaSaveSchema,
    GNaturezaSistemaIdSchema,
    GNaturezaUpdateSchema,
    GNaturezaIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_natureza_controller = GNaturezaController()

# Lista todos os registros de natureza
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de natureza cadastrados',
            response_description='Lista todos os registros de natureza cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de natureza cadastrados
    response = g_natureza_controller.index()

    # Retorna os dados localizados
    return response

# Lista todos os registros de natureza
@router.get(
    "/sistema/{sistema_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de natureza cadastrados",
    response_description="Lista todos os registros de natureza cadastrados"
)
async def index_by_sistema_id(
    sistema_id: int,
    current_user: dict = Depends(get_current_user)
):
    # Cria o schema com os dados recebidos
    natureza_schema = GNaturezaSistemaIdSchema(sistema_id=sistema_id)

    # Chama o controller (sem await)
    response = g_natureza_controller.indexBySistemaId(natureza_schema)

    # Retorna os dados
    return response

# Localiza um registro de natureza pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de natureza em específico pela descrição',
            response_description='Busca um registro de natureza em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    natureza_schema = GNaturezaSchema(descricao=descricao)

    # Busca um registro de natureza específico pela descrição
    response = g_natureza_controller.get_by_descricao(natureza_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de natureza pelo ID
@router.get('/{natureza_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de natureza em específico pelo ID',
            response_description='Busca um registro de natureza em específico')
async def show(natureza_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    natureza_schema = GNaturezaIdSchema(natureza_id=natureza_id)

    # Busca um registro de natureza específico pelo ID
    response = g_natureza_controller.show(natureza_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de natureza
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de natureza',
            response_description='Cadastra um registro de natureza')
async def save(natureza_schema: GNaturezaSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_natureza_controller.save(natureza_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de natureza
@router.put('/{natureza_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de natureza',
            response_description='Atualiza um registro de natureza')
async def update(natureza_id: int, natureza_schema: GNaturezaUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_natureza_controller.update(natureza_id, natureza_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de natureza
@router.delete('/{natureza_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de natureza',
            response_description='Remove um registro de natureza')
async def delete(natureza_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    natureza_schema = GNaturezaIdSchema(natureza_id=natureza_id)

    # Efetua a exclusão do registro de natureza
    response = g_natureza_controller.delete(natureza_schema)

    # Retorna os dados localizados
    return response