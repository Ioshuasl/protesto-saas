# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_tipologradouro_controller import GTbTipologradouroController
from packages.v1.administrativo.schemas.g_tb_tipologradouro_schema import (
    GTbTipoLogradouroSchema,
    GTbTipoLogradouroSaveSchema,
    GTbTipoLogradouroUpdateSchema,
    GTbTipoLogradouroIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_tb_tipologradouro_controller = GTbTipologradouroController()

# Lista todos os registros de tipologradouro
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de tipologradouro cadastrados',
            response_description='Lista todos os registros de tipologradouro cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de tipologradouro cadastrados
    response = g_tb_tipologradouro_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de tipologradouro pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de tipologradouro em específico pela descrição',
            response_description='Busca um registro de tipologradouro em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    tipologradouro_schema = GTbTipoLogradouroSchema(descricao=descricao)

    # Busca um registro de tipologradouro específico pela descrição
    response = g_tb_tipologradouro_controller.get_by_descricao(tipologradouro_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de tipologradouro pelo ID
@router.get('/{tb_tipologradouro_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de tipologradouro em específico pelo ID',
            response_description='Busca um registro de tipologradouro em específico')
async def show(tb_tipologradouro_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    tipologradouro_schema = GTbTipoLogradouroIdSchema(tb_tipologradouro_id=tb_tipologradouro_id)

    # Busca um registro de tipologradouro específico pelo ID
    response = g_tb_tipologradouro_controller.show(tipologradouro_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de tipologradouro
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de tipologradouro',
            response_description='Cadastra um registro de tipologradouro')
async def save(tipologradouro_schema: GTbTipoLogradouroSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_tb_tipologradouro_controller.save(tipologradouro_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de tipologradouro
@router.put('/{tb_tipologradouro_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de tipologradouro',
            response_description='Atualiza um registro de tipologradouro')
async def update(tb_tipologradouro_id: int, tipologradouro_schema: GTbTipoLogradouroUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_tb_tipologradouro_controller.update(tb_tipologradouro_id, tipologradouro_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de tipologradouro
@router.delete('/{tb_tipologradouro_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de tipologradouro',
            response_description='Remove um registro de tipologradouro')
async def delete(tb_tipologradouro_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    tipologradouro_schema = GTbTipoLogradouroIdSchema(tb_tipologradouro_id=tb_tipologradouro_id)

    # Efetua a exclusão do registro de tipologradouro
    response = g_tb_tipologradouro_controller.delete(tipologradouro_schema)

    # Retorna os dados localizados
    return response