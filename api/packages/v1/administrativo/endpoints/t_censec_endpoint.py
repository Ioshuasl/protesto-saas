# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_censec_controller import TCensecController
from packages.v1.administrativo.schemas.t_censec_schema import (
    TCensecSchema,
    TCensecSaveSchema,
    TCensecUpdateSchema,
    TCensecIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
t_censec_controller = TCensecController()

# Lista todos os registros de censec
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de censec cadastrados',
            response_description='Lista todos os registros de censec cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de censec cadastrados
    response = t_censec_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de censec pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de censec em específico pela descrição',
            response_description='Busca um registro de censec em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_schema = TCensecSchema(descricao=descricao)

    # Busca um registro de censec específico pela descrição
    response = t_censec_controller.get_by_descricao(censec_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de censec pelo ID
@router.get('/{censec_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de censec em específico pelo ID',
            response_description='Busca um registro de censec em específico')
async def show(censec_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_schema = TCensecIdSchema(censec_id=censec_id)

    # Busca um registro de censec específico pelo ID
    response = t_censec_controller.show(censec_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de censec
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de censec',
            response_description='Cadastra um registro de censec')
async def save(censec_schema: TCensecSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = t_censec_controller.save(censec_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de censec
@router.put('/{censec_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de censec',
            response_description='Atualiza um registro de censec')
async def update(censec_id: int, censec_schema: TCensecUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = t_censec_controller.update(censec_id, censec_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de censec
@router.delete('/{censec_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de censec',
            response_description='Remove um registro de censec')
async def delete(censec_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_schema = TCensecIdSchema(censec_id=censec_id)

    # Efetua a exclusão do registro de censec
    response = t_censec_controller.delete(censec_schema)

    # Retorna os dados localizados
    return response