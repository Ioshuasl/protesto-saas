# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_medida_tipo_controller import GMedidaTipoController
from packages.v1.administrativo.schemas.g_medida_tipo_schema import (
    GMedidaTipoSchema,
    GMedidaTipoSaveSchema,
    GMedidaTipoUpdateSchema,
    GMedidaTipoIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
g_medida_tipo_controller = GMedidaTipoController()

# Lista todos os registros de g_medida_tipo
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de g_medida_tipo cadastrados',
            response_description='Lista todos os registros de g_medida_tipo cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de g_medida_tipo cadastrados
    response = g_medida_tipo_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de g_medida_tipo pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de g_medida_tipo em específico pela descrição',
            response_description='Busca um registro de g_medida_tipo em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    medida_tipo_schema = GMedidaTipoSchema(descricao=descricao)

    # Busca um registro de g_medida_tipo específico pela descrição
    response = g_medida_tipo_controller.get_by_descricao(medida_tipo_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de g_medida_tipo pelo ID
@router.get('/{medida_tipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de g_medida_tipo em específico pelo ID',
            response_description='Busca um registro de g_medida_tipo em específico')
async def show(medida_tipo_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    medida_tipo_schema = GMedidaTipoIdSchema(medida_tipo_id=medida_tipo_id)

    # Busca um registro de g_medida_tipo específico pelo ID
    response = g_medida_tipo_controller.show(medida_tipo_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de g_medida_tipo
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de g_medida_tipo',
            response_description='Cadastra um registro de g_medida_tipo')
async def save(medida_tipo_schema: GMedidaTipoSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_medida_tipo_controller.save(medida_tipo_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de g_medida_tipo
@router.put('/{medida_tipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de g_medida_tipo',
            response_description='Atualiza um registro de g_medida_tipo')
async def update(medida_tipo_id: int, medida_tipo_schema: GMedidaTipoUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_medida_tipo_controller.update(medida_tipo_id, medida_tipo_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de g_medida_tipo
@router.delete('/{medida_tipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de g_medida_tipo',
            response_description='Remove um registro de g_medida_tipo')
async def delete(medida_tipo_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    medida_tipo_schema = GMedidaTipoIdSchema(medida_tipo_id=medida_tipo_id)

    # Efetua a exclusão do registro de g_medida_tipo
    response = g_medida_tipo_controller.delete(medida_tipo_schema)

    # Retorna os dados localizados
    return response