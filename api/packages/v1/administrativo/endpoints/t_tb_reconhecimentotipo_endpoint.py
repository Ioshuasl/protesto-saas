# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_tb_reconhecimentotipo_controller import TTbReconhecimentotipoController
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import (
    TTbReconhecimentotipoSchema,
    TTbReconhecimentotipoSaveSchema,
    TTbReconhecimentotipoUpdateSchema,
    TTbReconhecimentotipoIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instânciamento do controller desejado
t_tb_reconhecimentotipo_controller = TTbReconhecimentotipoController()

# Lista todos os tipos de reconhecimento
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os tipos de reconhecimento cadastrados',
            response_description='Lista todos os tipos de reconhecimento cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os tipos de reconhecimento cadastrados
    response = t_tb_reconhecimentotipo_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um tipo de reconhecimento pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em específico pela descrição',
            response_description='Busca um registro em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    reconhecimentotipo_schema = TTbReconhecimentotipoSchema(descricao=descricao)

    # Busca um tipo de reconhecimento específico pela descrição
    response = t_tb_reconhecimentotipo_controller.get_by_descricao(reconhecimentotipo_schema)

    # Retorna os dados localizados
    return response


# Localiza um tipo de reconhecimento pelo ID
@router.get('/{tb_reconhecimentotipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em específico pelo ID do tipo de reconhecimento',
            response_description='Busca um registro em específico')
async def show(tb_reconhecimentotipo_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    reconhecimentotipo_schema = TTbReconhecimentotipoIdSchema(tb_reconhecimentotipo_id=tb_reconhecimentotipo_id)

    # Busca um tipo de reconhecimento específico pelo ID
    response = t_tb_reconhecimentotipo_controller.show(reconhecimentotipo_schema)

    # Retorna os dados localizados
    return response


# Cadastro de tipo de reconhecimento
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um tipo de reconhecimento',
            response_description='Cadastra um tipo de reconhecimento')
async def save(reconhecimentotipo_schema : TTbReconhecimentotipoSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = t_tb_reconhecimentotipo_controller.save(reconhecimentotipo_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um tipo de reconhecimento
@router.put('/{tb_reconhecimentotipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um tipo de reconhecimento',
            response_description='Atualiza um tipo de reconhecimento')
async def update(tb_reconhecimentotipo_id : int, reconhecimentotipo_schema : TTbReconhecimentotipoUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = t_tb_reconhecimentotipo_controller.update(tb_reconhecimentotipo_id, reconhecimentotipo_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado tipo de reconhecimento
@router.delete('/{tb_reconhecimentotipo_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um tipo de reconhecimento',
            response_description='Remove um tipo de reconhecimento')
async def delete(tb_reconhecimentotipo_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    reconhecimentotipo_schema = TTbReconhecimentotipoIdSchema(tb_reconhecimentotipo_id=tb_reconhecimentotipo_id)

    # Efetua a exclusão do tipo de reconhecimento
    response = t_tb_reconhecimentotipo_controller.delete(reconhecimentotipo_schema)

    # Retorna os dados localizados
    return response
