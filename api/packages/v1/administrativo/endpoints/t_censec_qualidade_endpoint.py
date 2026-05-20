# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_censec_qualidade_controller import TCensecQualidadeController
from packages.v1.administrativo.schemas.t_censec_qualidade_schema import (
    TCensecQualidadeSchema,
    TCensecQualidadeSaveSchema,
    TCensecQualidadeUpdateSchema,
    TCensecQualidadeIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
t_censec_qualidade_controller = TCensecQualidadeController()

# Lista todos os registros de t_censec_qualidade
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de t_censec_qualidade cadastrados',
            response_description='Lista todos os registros de t_censec_qualidade cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de t_censec_qualidade cadastrados
    response = t_censec_qualidade_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de t_censec_qualidade pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de t_censec_qualidade em específico pela descrição',
            response_description='Busca um registro de t_censec_qualidade em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_qualidade_schema = TCensecQualidadeSchema(descricao=descricao)

    # Busca um registro de t_censec_qualidade específico pela descrição
    response = t_censec_qualidade_controller.get_by_descricao(censec_qualidade_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de t_censec_qualidade pelo ID
@router.get('/{censec_qualidade_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de t_censec_qualidade em específico pelo ID',
            response_description='Busca um registro de t_censec_qualidade em específico')
async def show(censec_qualidade_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_qualidade_schema = TCensecQualidadeIdSchema(censec_qualidade_id=censec_qualidade_id)

    # Busca um registro de t_censec_qualidade específico pelo ID
    response = t_censec_qualidade_controller.show(censec_qualidade_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de t_censec_qualidade
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de t_censec_qualidade',
            response_description='Cadastra um registro de t_censec_qualidade')
async def save(censec_qualidade_schema: TCensecQualidadeSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = t_censec_qualidade_controller.save(censec_qualidade_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de t_censec_qualidade
@router.put('/{censec_qualidade_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de t_censec_qualidade',
            response_description='Atualiza um registro de t_censec_qualidade')
async def update(censec_qualidade_id: int, censec_qualidade_schema: TCensecQualidadeUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = t_censec_qualidade_controller.update(censec_qualidade_id, censec_qualidade_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de t_censec_qualidade
@router.delete('/{censec_qualidade_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de t_censec_qualidade',
            response_description='Remove um registro de t_censec_qualidade')
async def delete(censec_qualidade_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_qualidade_schema = TCensecQualidadeIdSchema(censec_qualidade_id=censec_qualidade_id)

    # Efetua a exclusão do registro de t_censec_qualidade
    response = t_censec_qualidade_controller.delete(censec_qualidade_schema)

    # Retorna os dados localizados
    return response