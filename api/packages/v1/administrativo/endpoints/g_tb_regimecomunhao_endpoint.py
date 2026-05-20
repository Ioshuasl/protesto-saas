# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_regimecomunhao_controller import GTbRegimecomunhaoController
from packages.v1.administrativo.schemas.g_tb_regimecomunhao_schema import (
    GTbRegimecomunhaoSaveSchema,
    GTbRegimecomunhaoUpdateSchema,
    GTbRegimecomunhaoDescricaoSchema,
    GTbRegimecomunhaoIdSchema
)

# Inicializa o roteador para as rotas da tabela
router = APIRouter()

# Instânciamento do controller desejado
g_tb_regimecomunhao_controller = GTbRegimecomunhaoController()

# Lista todos os regimes de comunhão
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os regimes de comunhão cadastrados',
            response_description='Lista todos os regimes de comunhão cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros
    response = g_tb_regimecomunhao_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em especifico pela descrição',
            response_description='Busca um registro em especifico')
async def get_by_descricao(descricao: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    regimecomunhao_schema = GTbRegimecomunhaoDescricaoSchema(descricao=descricao)

    # Busca o registro especifico pela descrição
    response = g_tb_regimecomunhao_controller.get_by_descricao(regimecomunhao_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro pelo ID
@router.get('/{tb_regimecomunhao_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em especifico pelo ID',
            response_description='Busca um registro em especifico')
async def show(tb_regimecomunhao_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    regimecomunhao_schema = GTbRegimecomunhaoIdSchema(tb_regimecomunhao_id=tb_regimecomunhao_id)

    # Busca o registro especifico pelo ID
    response = g_tb_regimecomunhao_controller.show(regimecomunhao_schema)

    # Retorna os dados localizados
    return response


# Cadastro de novo registro
@router.post('/',
            status_code=status.HTTP_200_OK,
            summary='Cadastra um novo registro de regime de comunhão',
            response_description='Cadastra um novo registro')
async def save(regimecomunhao_schema: GTbRegimecomunhaoSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = g_tb_regimecomunhao_controller.save(regimecomunhao_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro
@router.put('/{tb_regimecomunhao_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro',
            response_description='Atualiza um registro')
async def update(tb_regimecomunhao_id: int, regimecomunhao_schema: GTbRegimecomunhaoUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = g_tb_regimecomunhao_controller.update(tb_regimecomunhao_id, regimecomunhao_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado registro
@router.delete('/{tb_regimecomunhao_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um registro',
            response_description='Remove um registro')
async def delete(tb_regimecomunhao_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    regimecomunhao_schema = GTbRegimecomunhaoIdSchema(tb_regimecomunhao_id=tb_regimecomunhao_id)

    # Efetua a exclusão do registro
    response = g_tb_regimecomunhao_controller.delete(regimecomunhao_schema)

    # Retorna os dados localizados
    return response