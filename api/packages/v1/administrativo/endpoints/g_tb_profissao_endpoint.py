# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_tb_profissao_controller import GTbProfissaoController
from packages.v1.administrativo.schemas.g_tb_profissao_schema import (
    GTbProfissaoSaveSchema,
    GTbProfissaoUpdateSchema,
    GTbProfissaoIdSchema,
    GTbProfissaoDescricaoSchema
)

# Inicializa o roteador para as rotas da profissão
router = APIRouter()

# Instanciamento do controller desejado
g_tb_profissao_controller = GTbProfissaoController()

# Lista todas as profissões
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todas as profissões cadastradas',
            response_description='Lista todas as profissões cadastradas')
async def index(current_user: dict = Depends(get_current_user)):
    """
    Endpoint que retorna uma lista de todas as profissões cadastradas.
    """
    # Busca todas as profissões cadastradas
    response = g_tb_profissao_controller.index()
    return response


# Localiza uma profissão pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de profissão em específico pela descrição',
            response_description='Busca um registro de profissão em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):
    """
    Endpoint que busca uma profissão específica usando a descrição.
    """
    # Cria o schema com os dados recebidos
    profissao_schema = GTbProfissaoDescricaoSchema(descricao=descricao)

    # Busca a profissão específica pela descrição
    response = g_tb_profissao_controller.get_by_descricao(profissao_schema)
    return response


# Busca profissões pela descrição (endpoint de busca)
@router.get('/busca',
            status_code=status.HTTP_200_OK,
            summary='Busca profissão pela descrição',
            response_description='Busca profissão pela descrição')
async def search_by_descricao(descricao: str, current_user: dict = Depends(get_current_user)):
    """
    Endpoint de busca de profissão por descrição.
    """
    # Cria o schema com os dados recebidos
    profissao_schema = GTbProfissaoDescricaoSchema(descricao=descricao)

    # Busca a profissão pela descrição
    response = g_tb_profissao_controller.search_by_descricao(profissao_schema)
    return response


# Localiza uma profissão pelo ID
@router.get('/{tb_profissao_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de profissão em específico pelo ID',
            response_description='Busca um registro de profissão em específico')
async def show(tb_profissao_id : float, current_user: dict = Depends(get_current_user)):
    """
    Endpoint que busca uma profissão específica pelo ID.
    """
    # Cria o schema com os dados recebidos
    profissao_schema = GTbProfissaoIdSchema(tb_profissao_id=tb_profissao_id)

    # Busca a profissão específica pelo ID
    response = g_tb_profissao_controller.show(profissao_schema)
    return response


# Cadastro de profissão
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra uma nova profissão',
            response_description='Cadastra uma nova profissão')
async def save(profissao_schema : GTbProfissaoSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Endpoint para cadastrar uma nova profissão no banco de dados.
    """
    # Efetua o cadastro no banco de dados
    response = g_tb_profissao_controller.save(profissao_schema)
    return response


# Atualiza os dados de uma profissão
@router.put('/{tb_profissao_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza os dados de uma profissão',
            response_description='Atualiza os dados de uma profissão')
async def update(tb_profissao_id : float, profissao_schema : GTbProfissaoUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Endpoint para atualizar os dados de uma profissão existente.
    """
    # Efetua a atualização dos dados
    response = g_tb_profissao_controller.update(tb_profissao_id, profissao_schema)
    return response


# Exclui uma profissão
@router.delete('/{tb_profissao_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove uma profissão',
            response_description='Remove uma profissão')
async def delete(tb_profissao_id : float, current_user: dict = Depends(get_current_user)):
    """
    Endpoint para excluir uma profissão pelo ID.
    """
    # Cria o schema com os dados recebidos
    profissao_schema = GTbProfissaoIdSchema(tb_profissao_id=tb_profissao_id)

    # Efetua a exclusão da profissão
    response = g_tb_profissao_controller.delete(profissao_schema)
    return response