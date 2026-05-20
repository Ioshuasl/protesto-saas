# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_censec_naturezalitigio_controller import TCensecNaturezalitigioController
from packages.v1.administrativo.schemas.t_censec_naturezalitigio_schema import (
    TCensecNaturezalitigioSchema,
    TCensecNaturezalitigioSaveSchema,
    TCensecNaturezalitigioUpdateSchema,
    TCensecNaturezalitigioIdSchema
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
t_censec_naturezalitigio_controller = TCensecNaturezalitigioController()

# Lista todos os registros de natureza_litigio
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de natureza_litigio cadastrados',
            response_description='Lista todos os registros de natureza_litigio cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de natureza_litigio cadastrados
    response = t_censec_naturezalitigio_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de natureza_litigio pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de natureza_litigio em específico pela descrição',
            response_description='Busca um registro de natureza_litigio em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_naturezalitigio_schema = TCensecNaturezalitigioSchema(descricao=descricao)

    # Busca um registro de natureza_litigio específico pela descrição
    response = t_censec_naturezalitigio_controller.get_by_descricao(censec_naturezalitigio_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de natureza_litigio pelo ID
@router.get('/{censec_naturezalitigio_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de natureza_litigio em específico pelo ID',
            response_description='Busca um registro de natureza_litigio em específico')
async def show(censec_naturezalitigio_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_naturezalitigio_schema = TCensecNaturezalitigioIdSchema(censec_naturezalitigio_id=censec_naturezalitigio_id)

    # Busca um registro de natureza_litigio específico pelo ID
    response = t_censec_naturezalitigio_controller.show(censec_naturezalitigio_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de natureza_litigio
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um registro de natureza_litigio',
            response_description='Cadastra um registro de natureza_litigio')
async def save(censec_naturezalitigio_schema: TCensecNaturezalitigioSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = t_censec_naturezalitigio_controller.save(censec_naturezalitigio_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de natureza_litigio
@router.put('/{censec_naturezalitigio_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro de natureza_litigio',
            response_description='Atualiza um registro de natureza_litigio')
async def update(censec_naturezalitigio_id: int, censec_naturezalitigio_schema: TCensecNaturezalitigioUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = t_censec_naturezalitigio_controller.update(censec_naturezalitigio_id, censec_naturezalitigio_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado registro de natureza_litigio
@router.delete('/{censec_naturezalitigio_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro de natureza_litigio',
            response_description='Remove um registro de natureza_litigio')
async def delete(censec_naturezalitigio_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    censec_naturezalitigio_schema = TCensecNaturezalitigioIdSchema(censec_naturezalitigio_id=censec_naturezalitigio_id)

    # Efetua a exclusão do registro de natureza_litigio
    response = t_censec_naturezalitigio_controller.delete(censec_naturezalitigio_schema)

    # Retorna os dados localizados
    return response