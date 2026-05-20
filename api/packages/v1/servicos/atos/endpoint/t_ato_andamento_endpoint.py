# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_ato_andamento_controller import (
    TAtoAndamentoController,
)
from packages.v1.servicos.atos.schemas.t_ato_andamento_schema import (
    TAtoAndamentoIndexSchema,
    TAtoAndamentoSaveSchema,
    TAtoAndamentoUpdateSchema,
    TAtoAndamentoIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_ATO_ANDAMENTO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_ato_andamento_controller = TAtoAndamentoController()


# ----------------------------------------------------
# Lista todos os registros de T_ATO_ANDAMENTO
# ----------------------------------------------------
@router.get(
    "/ato/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_ATO_ANDAMENTO cadastrados",
    response_description="Lista todos os registros de T_ATO_ANDAMENTO cadastrados",
)
async def index(ato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_ATO_ANDAMENTO.
    """
    data = TAtoAndamentoIndexSchema(ato_id=ato_id)
    response = t_ato_andamento_controller.index(data)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_ATO_ANDAMENTO pelo ID
# ----------------------------------------------------
@router.get(
    "/{ato_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_ATO_ANDAMENTO pelo ID",
    response_description="Busca um registro de T_ATO_ANDAMENTO em específico",
)
async def show(ato_andamento_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_ATO_ANDAMENTO com base no ID informado.
    """
    ato_andamento_id_schema = TAtoAndamentoIdSchema(ato_andamento_id=ato_andamento_id)
    response = t_ato_andamento_controller.show(ato_andamento_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_ATO_ANDAMENTO
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO_ANDAMENTO",
    response_description="Cadastra um novo registro em T_ATO_ANDAMENTO",
)
async def save(
    t_ato_andamento_schema: TAtoAndamentoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_ATO_ANDAMENTO.
    """
    response = t_ato_andamento_controller.save(t_ato_andamento_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_ATO_ANDAMENTO
# ----------------------------------------------------
@router.put(
    "/{ato_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO_ANDAMENTO",
    response_description="Atualiza um registro existente em T_ATO_ANDAMENTO",
)
async def update(
    ato_andamento_id: int,
    t_ato_andamento_update_schema: TAtoAndamentoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_ATO_ANDAMENTO com base no ID informado.
    """
    t_ato_andamento_update_schema.ato_andamento_id = ato_andamento_id
    response = t_ato_andamento_controller.update(t_ato_andamento_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_ANDAMENTO
# ----------------------------------------------------
@router.delete(
    "/{ato_andamento_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO_ANDAMENTO",
    response_description="Remove um registro de T_ATO_ANDAMENTO",
)
async def delete(ato_andamento_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de T_ATO_ANDAMENTO com base no ID informado.
    """
    ato_andamento_id_schema = TAtoAndamentoIdSchema(ato_andamento_id=ato_andamento_id)
    response = t_ato_andamento_controller.delete(ato_andamento_id_schema)
    return response
