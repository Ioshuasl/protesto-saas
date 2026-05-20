# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_documentotipo_controller import GTbDocumentoTipoController
from packages.v1.administrativo.schemas.g_tb_documentotipo_schema import (
    GTbDocumentoTipoSchema,
    GTbDocumentoTipoSaveSchema,
    GTbDocumentoTipoUpdateSchema,
    GTbDocumentoTipoIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_tb_documentotipo_controller = GTbDocumentoTipoController()

# Lista todos os registros de g_tb_documentotipo
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de g_tb_documentotipo cadastrados',
            response_description='Lista todos os registros de g_tb_documentotipo cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de g_tb_documentotipo cadastrados
    response = g_tb_documentotipo_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de g_tb_documentotipo pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de g_tb_documentotipo em específico pela descrição',
            response_description='Busca um registro de g_tb_documentotipo em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    documento_tipo_schema = GTbDocumentoTipoSchema(descricao=descricao)

    # Busca um registro de g_tb_documentotipo específico pela descrição
    response = g_tb_documentotipo_controller.get_by_descricao(documento_tipo_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de g_tb_documentotipo pelo ID
@router.get('/{tb_documentotipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de g_tb_documentotipo em específico pelo ID',
            response_description='Busca um registro de g_tb_documentotipo em específico')
async def show(tb_documentotipo_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    documento_tipo_schema = GTbDocumentoTipoIdSchema(tb_documentotipo_id=tb_documentotipo_id)

    # Busca um registro de g_tb_documentotipo específico pelo ID
    response = g_tb_documentotipo_controller.show(documento_tipo_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de g_tb_documentotipo
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de g_tb_documentotipo',
            response_description='Cadastra um registro de g_tb_documentotipo')
async def save(documento_tipo_schema: GTbDocumentoTipoSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_tb_documentotipo_controller.save(documento_tipo_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de g_tb_documentotipo
@router.put('/{tb_documentotipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de g_tb_documentotipo',
            response_description='Atualiza um registro de g_tb_documentotipo')
async def update(tb_documentotipo_id: int, documento_tipo_schema: GTbDocumentoTipoUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_tb_documentotipo_controller.update(tb_documentotipo_id, documento_tipo_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de g_tb_documentotipo
@router.delete('/{tb_documentotipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de g_tb_documentotipo',
            response_description='Remove um registro de g_tb_documentotipo')
async def delete(tb_documentotipo_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    documento_tipo_schema = GTbDocumentoTipoIdSchema(tb_documentotipo_id=tb_documentotipo_id)

    # Efetua a exclusão do registro de g_tb_documentotipo
    response = g_tb_documentotipo_controller.delete(documento_tipo_schema)

    # Retorna os dados localizados
    return response