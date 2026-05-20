# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_estadocivil_controller import GTbEstadoCivilController
from packages.v1.administrativo.schemas.g_tb_estadocivil_schema import (
    GTbEstadoCivilSchema,
    GTbEstadoCivilSaveSchema,
    GTbEstadoCivilUpdateSchema,
    GTbEstadoCivilIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_tb_estadocivil_controller = GTbEstadoCivilController()

# Lista todos os registros de estadocivil
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de estadocivil cadastrados',
            response_description='Lista todos os registros de estadocivil cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de estadocivil cadastrados
    response = g_tb_estadocivil_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de estadocivil pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de estadocivil em específico pela descrição',
            response_description='Busca um registro de estadocivil em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    estadocivil_schema = GTbEstadoCivilSchema(descricao=descricao)

    # Busca um registro de estadocivil específico pela descrição
    response = g_tb_estadocivil_controller.get_by_descricao(estadocivil_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de estadocivil pelo ID
@router.get('/{tb_estadocivil_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de estadocivil em específico pelo ID',
            response_description='Busca um registro de estadocivil em específico')
async def show(tb_estadocivil_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    estadocivil_schema = GTbEstadoCivilIdSchema(tb_estadocivil_id=tb_estadocivil_id)

    # Busca um registro de estadocivil específico pelo ID
    response = g_tb_estadocivil_controller.show(estadocivil_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de estadocivil
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de estadocivil',
            response_description='Cadastra um registro de estadocivil')
async def save(estadocivil_schema: GTbEstadoCivilSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_tb_estadocivil_controller.save(estadocivil_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de estadocivil
@router.put('/{tb_estadocivil_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de estadocivil',
            response_description='Atualiza um registro de estadocivil')
async def update(tb_estadocivil_id: int, estadocivil_schema: GTbEstadoCivilUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_tb_estadocivil_controller.update(tb_estadocivil_id, estadocivil_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de estadocivil
@router.delete('/{tb_estadocivil_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de estadocivil',
            response_description='Remove um registro de estadocivil')
async def delete(tb_estadocivil_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    estadocivil_schema = GTbEstadoCivilIdSchema(tb_estadocivil_id=tb_estadocivil_id)

    # Efetua a exclusão do registro de estadocivil
    response = g_tb_estadocivil_controller.delete(estadocivil_schema)

    # Retorna os dados localizados
    return response