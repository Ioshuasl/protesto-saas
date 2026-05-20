# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_historico_controller import (
    THistoricoController,
)
from packages.v1.servicos.atos.schemas.t_historico_schema import (
    THistoricoHashSchema,
    THistoricoIndexSchema,
    THistoricoSaveSchema,
    THistoricoUpdateSchema,
    THistoricoIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_HISTORICO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
controller = THistoricoController()


@router.get(
    "/hash/{hash_input}",
    status_code=status.HTTP_200_OK,
    summary="Busca registros de T_HISTORICO por hash",
    response_description="Busca registros de T_HISTORICO por hash gerado no backend",
)
async def show_by_hash(
    hash_input: str,
    current_user: dict = Depends(get_current_user),
):
    data = THistoricoHashSchema(hash_input=hash_input)
    response = controller.show_by_hash(data)
    return response


# ----------------------------------------------------
# Lista todos os registros de T_HISTORICO
# ----------------------------------------------------
@router.get(
    "/{tabela}/{id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_HISTORICO cadastrados",
    response_description="Lista todos os registros de T_HISTORICO cadastrados",
)
async def index(id: int, tabela: str, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_HISTORICO.
    """
    data = THistoricoIndexSchema(id=id, tabela=tabela)
    response = controller.index(data)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_HISTORICO pelo ID
# ----------------------------------------------------
@router.get(
    "/{historico_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_HISTORICO pelo ID",
    response_description="Busca um registro de T_HISTORICO em específico",
)
async def show(historico_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_HISTORICO com base no ID informado.
    """
    schema = THistoricoIdSchema(historico_id=historico_id)
    response = controller.show(schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_HISTORICO
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_HISTORICO",
    response_description="Cadastra um novo registro em T_HISTORICO",
)
async def save(schema: THistoricoSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Cria um novo registro na tabela T_HISTORICO.
    """
    response = controller.save(schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_HISTORICO
# ----------------------------------------------------
@router.put(
    "/{historico_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_HISTORICO",
    response_description="Atualiza um registro existente em T_HISTORICO",
)
async def update(
    historico_id: int,
    schema: THistoricoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_HISTORICO com base no ID informado.
    """
    setattr(schema, "historico_id", historico_id)
    response = controller.update(schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_HISTORICO
# ----------------------------------------------------
@router.delete(
    "/{historico_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_HISTORICO",
    response_description="Remove um registro de T_HISTORICO",
)
async def delete(historico_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de T_HISTORICO com base no ID informado.
    """
    schema = THistoricoIdSchema(historico_id=historico_id)
    response = controller.delete(schema)
    return response
