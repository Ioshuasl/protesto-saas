# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_regimebens_controller import GTbRegimebensController
from packages.v1.administrativo.schemas.g_tb_regimebens_schema import (
    GTbRegimebensSchema,
    GTbRegimebensSaveSchema,
    GTbRegimebensUpdateSchema,
    GTbRegimebensIdSchema
)

# Inicializa o roteador para as rotas do regime de bens
router = APIRouter()

# Instânciamento do controller desejado
g_tb_regimebens_controller = GTbRegimebensController()

# Lista todos os regimes de bens
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os regimes de bens cadastrados',
            response_description='Lista todos os regimes de bens cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os regimes de bens cadastrados
    response = g_tb_regimebens_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um regime de bens pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em específico pela descrição',
            response_description='Busca um registro em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    regimebens_schema = GTbRegimebensSchema(descricao=descricao)

    # Busca um regime de bens específico pela descrição
    response = g_tb_regimebens_controller.get_by_descricao(regimebens_schema)

    # Retorna os dados localizados
    return response


# Localiza um regime de bens pelo ID
@router.get('/{tb_regimebens_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em específico pelo ID do regime de bens',
            response_description='Busca um registro em específico')
async def show(tb_regimebens_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    regimebens_schema = GTbRegimebensIdSchema(tb_regimebens_id=tb_regimebens_id)

    # Busca um regime de bens específico pelo ID
    response = g_tb_regimebens_controller.show(regimebens_schema)

    # Retorna os dados localizados
    return response


# Cadastro de regime de bens
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um regime de bens',
            response_description='Cadastra um regime de bens')
async def save(regimebens_schema : GTbRegimebensSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_tb_regimebens_controller.save(regimebens_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um regime de bens
@router.put('/{tb_regimebens_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um regime de bens',
            response_description='Atualiza um regime de bens')
async def update(tb_regimebens_id : int, regimebens_schema : GTbRegimebensUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_tb_regimebens_controller.update(tb_regimebens_id, regimebens_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado regime de bens
@router.delete('/{tb_regimebens_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um regime de bens',
            response_description='Remove um regime de bens')
async def delete(tb_regimebens_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    regimebens_schema = GTbRegimebensIdSchema(tb_regimebens_id=tb_regimebens_id)

    # Efetua a exclusão do regime de bens
    response = g_tb_regimebens_controller.delete(regimebens_schema)

    # Retorna os dados localizados
    return response