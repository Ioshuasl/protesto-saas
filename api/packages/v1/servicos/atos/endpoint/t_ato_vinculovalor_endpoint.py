# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_ato_vinculovalor_controller import (
    TAtoVinculoValorController,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculovalor_schema import (
    TAtoVinculoValorIndexSchema,
    TAtoVinculoValorSaveSchema,
    TAtoVinculoValorUpdateSchema,
    TAtoVinculoValorIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_ATO_VINCULOVALOR
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_ato_vinculovalor_controller = TAtoVinculoValorController()


# ----------------------------------------------------
# Lista todos os registros de T_ATO_VINCULOVALOR
# ----------------------------------------------------
@router.get(
    "/ato/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_ATO_VINCULOVALOR cadastrados",
    response_description="Lista todos os registros de T_ATO_VINCULOVALOR cadastrados",
)
async def index(ato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_ATO_VINCULOVALOR.
    """
    data = TAtoVinculoValorIndexSchema(ato_id=ato_id)
    response = t_ato_vinculovalor_controller.index(data)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_ATO_VINCULOVALOR pelo ID
# ----------------------------------------------------
@router.get(
    "/{ato_vinculovalor_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_ATO_VINCULOVALOR pelo ID",
    response_description="Busca um registro de T_ATO_VINCULOVALOR em específico",
)
async def show(
    ato_vinculovalor_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de T_ATO_VINCULOVALOR com base no ID informado.
    """
    ato_vinculovalor_id_schema = TAtoVinculoValorIdSchema(
        ato_vinculovalor_id=ato_vinculovalor_id
    )
    response = t_ato_vinculovalor_controller.show(ato_vinculovalor_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_ATO_VINCULOVALOR
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO_VINCULOVALOR",
    response_description="Cadastra um novo registro em T_ATO_VINCULOVALOR",
)
async def save(
    t_ato_vinculovalor_schema: TAtoVinculoValorSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_ATO_VINCULOVALOR.
    """
    response = t_ato_vinculovalor_controller.save(t_ato_vinculovalor_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_ATO_VINCULOVALOR
# ----------------------------------------------------
@router.put(
    "/{ato_vinculovalor_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO_VINCULOVALOR",
    response_description="Atualiza um registro existente em T_ATO_VINCULOVALOR",
)
async def update(
    ato_vinculovalor_id: int,
    t_ato_vinculovalor_update_schema: TAtoVinculoValorUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_ATO_VINCULOVALOR com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    t_ato_vinculovalor_update_schema.usuario_id = current_user.data.usuario_id
    t_ato_vinculovalor_update_schema.ato_vinculovalor_id = ato_vinculovalor_id
    response = t_ato_vinculovalor_controller.update(t_ato_vinculovalor_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_VINCULOVALOR
# ----------------------------------------------------
@router.delete(
    "/{ato_vinculovalor_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO_VINCULOVALOR",
    response_description="Remove um registro de T_ATO_VINCULOVALOR",
)
async def delete(
    ato_vinculovalor_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_ATO_VINCULOVALOR com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    ato_vinculovalor_id_schema = TAtoVinculoValorIdSchema(
        ato_vinculovalor_id=ato_vinculovalor_id,
        usuario_id=current_user.data.usuario_id,
    )
    response = t_ato_vinculovalor_controller.delete(ato_vinculovalor_id_schema)
    return response
