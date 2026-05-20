# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_bairro_controller import GTbBairroController
from packages.v1.administrativo.schemas.g_tb_bairro_schema import (
    GTbBairroSchema,
    GTbBairroSaveSchema,
    GTbBairroUpdateSchema,
    GTbBairroIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_tb_bairro_controller = GTbBairroController()

# Lista todos os registros de bairro
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de bairro cadastrados',
            response_description='Lista todos os registros de bairro cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de bairro cadastrados
    response = g_tb_bairro_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de bairro pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de bairro em específico pela descrição',
            response_description='Busca um registro de bairro em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    bairro_schema = GTbBairroSchema(descricao=descricao)

    # Busca um registro de bairro específico pela descrição
    response = g_tb_bairro_controller.get_by_descricao(bairro_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de bairro pelo ID
@router.get('/{tb_bairro_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de bairro em específico pelo ID',
            response_description='Busca um registro de bairro em específico')
async def show(tb_bairro_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    bairro_schema = GTbBairroIdSchema(tb_bairro_id=tb_bairro_id)

    # Busca um registro de bairro específico pelo ID
    response = g_tb_bairro_controller.show(bairro_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de bairro
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de bairro',
            response_description='Cadastra um registro de bairro')
async def save(bairro_schema: GTbBairroSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_tb_bairro_controller.save(bairro_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de bairro
@router.put('/{tb_bairro_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de bairro',
            response_description='Atualiza um registro de bairro')
async def update(tb_bairro_id: int, bairro_schema: GTbBairroUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_tb_bairro_controller.update(tb_bairro_id, bairro_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de bairro
@router.delete('/{tb_bairro_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de bairro',
            response_description='Remove um registro de bairro')
async def delete(tb_bairro_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    bairro_schema = GTbBairroIdSchema(tb_bairro_id=tb_bairro_id)

    # Efetua a exclusão do registro de bairro
    response = g_tb_bairro_controller.delete(bairro_schema)

    # Retorna os dados localizados
    return response