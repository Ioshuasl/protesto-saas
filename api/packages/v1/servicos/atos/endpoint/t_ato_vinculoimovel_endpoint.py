# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_ato_vinculoimovel_controller import (
    TAtoVinculoImovelController,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoimovel_schema import (
    TAtoVinculoImovelIndexSchema,
    TAtoVinculoImovelSaveSchema,
    TAtoVinculoImovelUpdateSchema,
    TAtoVinculoImovelIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_ATO_VINCULOIMOVEL
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_ato_vinculoimovel_controller = TAtoVinculoImovelController()


# ----------------------------------------------------
# Lista todos os registros de T_ATO_VINCULOIMOVEL
# ----------------------------------------------------
@router.get(
    "/ato/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_ATO_VINCULOIMOVEL cadastrados",
    response_description="Lista todos os registros de T_ATO_VINCULOIMOVEL cadastrados",
)
async def index(ato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_ATO_VINCULOIMOVEL com base no ID informado.
    """
    data = TAtoVinculoImovelIndexSchema(ato_id=ato_id)
    response = t_ato_vinculoimovel_controller.index(data)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_ATO_VINCULOIMOVEL pelo ID
# ----------------------------------------------------
@router.get(
    "/{ato_vinculoimovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_ATO_VINCULOIMOVEL pelo ID",
    response_description="Busca um registro de T_ATO_VINCULOIMOVEL em específico",
)
async def show(
    ato_vinculoimovel_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de T_ATO_VINCULOIMOVEL com base no ID informado.
    """
    ato_vinculoimovel_id_schema = TAtoVinculoImovelIdSchema(
        ato_vinculoimovel_id=ato_vinculoimovel_id
    )
    response = t_ato_vinculoimovel_controller.show(ato_vinculoimovel_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_ATO_VINCULOIMOVEL
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO_VINCULOIMOVEL",
    response_description="Cadastra um novo registro em T_ATO_VINCULOIMOVEL",
)
async def save(
    t_ato_vinculoimovel_schema: TAtoVinculoImovelSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_ATO_VINCULOIMOVEL.
    """
    current_user = dict_to_namespace(current_user)
    t_ato_vinculoimovel_schema.usuario_id = current_user.data.usuario_id
    response = t_ato_vinculoimovel_controller.save(t_ato_vinculoimovel_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_ATO_VINCULOIMOVEL
# ----------------------------------------------------
@router.put(
    "/{ato_vinculoimovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO_VINCULOIMOVEL",
    response_description="Atualiza um registro existente em T_ATO_VINCULOIMOVEL",
)
async def update(
    ato_vinculoimovel_id: int,
    t_ato_vinculoimovel_update_schema: TAtoVinculoImovelUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_ATO_VINCULOIMOVEL com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    t_ato_vinculoimovel_update_schema.usuario_id = current_user.data.usuario_id
    t_ato_vinculoimovel_update_schema.ato_vinculoimovel_id = ato_vinculoimovel_id
    response = t_ato_vinculoimovel_controller.update(t_ato_vinculoimovel_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_VINCULOIMOVEL
# ----------------------------------------------------
@router.delete(
    "/{ato_vinculoimovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO_VINCULOIMOVEL",
    response_description="Remove um registro de T_ATO_VINCULOIMOVEL",
)
async def delete(
    ato_vinculoimovel_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_ATO_VINCULOIMOVEL com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    ato_vinculoimovel_id_schema = TAtoVinculoImovelIdSchema(
        ato_vinculoimovel_id=ato_vinculoimovel_id,
        usuario_id=current_user.data.usuario_id,
    )
    response = t_ato_vinculoimovel_controller.delete(ato_vinculoimovel_id_schema)
    return response
