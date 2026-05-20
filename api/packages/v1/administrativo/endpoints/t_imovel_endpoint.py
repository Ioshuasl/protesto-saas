# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_imovel_controller import TImovelController
from packages.v1.administrativo.schemas.t_imovel_schema import (
    TImovelIndexSchema,
    TImovelSaveSchema,
    TImovelUpdateSchema,
    TImovelIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
t_imovel_controller = TImovelController()

# Lista todos os registros de t_imovel
@router.get('/classe/{tipo_classe}',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de t_imovel cadastrados',
            response_description='Lista todos os registros de t_imovel cadastrados')
async def index(tipo_classe: int, current_user: dict = Depends(get_current_user)):

    t_imovel_index_schema = TImovelIndexSchema(tipo_classe=tipo_classe)

    # Busca todos os registros de t_imovel cadastrados
    response = t_imovel_controller.index(t_imovel_index_schema)

    # Retorna os dados localizados
    return response

# Localiza um registro de t_imovel pelo ID
@router.get('/{imovel_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de t_imovel em específico pelo ID',
            response_description='Busca um registro de t_imovel em específico')
async def show(imovel_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    t_imovel_id_schema = TImovelIdSchema(imovel_id=imovel_id)

    # Busca um registro de t_imovel específico pelo ID
    response = t_imovel_controller.show(t_imovel_id_schema)

    # Retorna os dados localizados
    return response

# Cadastro de registro de t_imovel
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de t_imovel',
            response_description='Cadastra um registro de t_imovel')
async def save(t_imovel_schema: TImovelSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = t_imovel_controller.save(t_imovel_schema)

    # Retorna os dados localizados
    return response

# Atualiza os dados de um registro de t_imovel
@router.put('/{imovel_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de t_imovel',
            response_description='Atualiza um registro de t_imovel')
async def update(imovel_id: int, t_imovel_update_schema: TImovelUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Adiciona o ID do registro ao schema
    t_imovel_update_schema.imovel_id = imovel_id

    # Efetua a atualização dos dados
    response = t_imovel_controller.update(t_imovel_update_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de t_imovel
@router.delete('/{imovel_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de t_imovel',
            response_description='Remove um registro de t_imovel')
async def delete(imovel_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    t_imovel_schema = TImovelIdSchema(imovel_id=imovel_id)

    # Efetua a exclusão do registro de t_imovel
    response = t_imovel_controller.delete(t_imovel_schema)

    # Retorna os dados localizados
    return response