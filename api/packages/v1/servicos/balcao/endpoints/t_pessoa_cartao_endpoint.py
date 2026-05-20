# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.balcao.controllers.t_pessoa_cartao_controller import (
    TPessoaCartaoController,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
    TPessoaCartaoSaveSchema,
    TPessoaCartaoUpdateSchema,
    TPessoaCartaoIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_PESSOA_CARTAO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_pessoa_cartao_controller = TPessoaCartaoController()


# ----------------------------------------------------
# Lista todos os registros de T_PESSOA_CARTAO
# ----------------------------------------------------
@router.get(
    "/pessoa/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_PESSOA_CARTAO cadastrados",
    response_description="Lista todos os registros de T_PESSOA_CARTAO cadastrados",
)
async def index(pessoa_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_PESSOA_CARTAO.
    """
    t_pessoa_cartao_index_schema = TPessoaCartaoIndexchema(pessoa_id=pessoa_id)
    response = t_pessoa_cartao_controller.index(t_pessoa_cartao_index_schema)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_PESSOA_CARTAO pelo ID
# ----------------------------------------------------
@router.get(
    "/{pessoa_cartao_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_PESSOA_CARTAO pelo ID",
    response_description="Busca um registro de T_PESSOA_CARTAO em específico",
)
async def show(pessoa_cartao_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_PESSOA_CARTAO com base no ID informado.
    """
    t_pessoa_cartao_id_schema = TPessoaCartaoIdSchema(pessoa_cartao_id=pessoa_cartao_id)
    response = t_pessoa_cartao_controller.show(t_pessoa_cartao_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_PESSOA_CARTAO
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_PESSOA_CARTAO",
    response_description="Cadastra um novo registro em T_PESSOA_CARTAO",
)
async def save(
    t_pessoa_cartao_schema: TPessoaCartaoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    current_user = dict_to_namespace(current_user)

    t_pessoa_cartao_schema.usuario_id = current_user.data.usuario_id

    response = t_pessoa_cartao_controller.save(t_pessoa_cartao_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_PESSOA_CARTAO
# ----------------------------------------------------
@router.put(
    "/{pessoa_cartao_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_PESSOA_CARTAO",
    response_description="Atualiza um registro existente em T_PESSOA_CARTAO",
)
async def update(
    pessoa_cartao_id: int,
    t_pessoa_cartao_update_schema: TPessoaCartaoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_PESSOA_CARTAO com base no ID informado.
    """
    t_pessoa_cartao_update_schema.pessoa_cartao_id = pessoa_cartao_id
    response = t_pessoa_cartao_controller.update(t_pessoa_cartao_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_PESSOA_CARTAO
# ----------------------------------------------------
@router.delete(
    "/{pessoa_cartao_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_PESSOA_CARTAO",
    response_description="Remove um registro de T_PESSOA_CARTAO",
)
async def delete(pessoa_cartao_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de T_PESSOA_CARTAO com base no ID informado.
    """
    t_pessoa_cartao_id_schema = TPessoaCartaoIdSchema(pessoa_cartao_id=pessoa_cartao_id)
    response = t_pessoa_cartao_controller.delete(t_pessoa_cartao_id_schema)
    return response
