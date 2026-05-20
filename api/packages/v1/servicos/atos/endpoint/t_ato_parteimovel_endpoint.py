# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_ato_parteimovel_controller import (
    TAtoParteImovelController,
)
from packages.v1.servicos.atos.schemas.t_ato_parteimovel_schema import (
    TAtoParteImovelIndexSchema,
    TAtoParteImovelSaveSchema,
    TAtoParteImovelUpdateSchema,
    TAtoParteImovelIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_ATO_PARTEIMOVEL
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_ato_parteimovel_controller = TAtoParteImovelController()


# ----------------------------------------------------
# Lista todos os registros de T_ATO_PARTEIMOVEL
# ----------------------------------------------------
@router.get(
    "/ato/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_ATO_PARTEIMOVEL cadastrados",
    response_description="Lista todos os registros de T_ATO_PARTEIMOVEL cadastrados",
)
async def index(ato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_ATO_PARTEIMOVEL.
    """
    data = TAtoParteImovelIndexSchema(ato_id=ato_id)
    response = t_ato_parteimovel_controller.index(data)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_ATO_PARTEIMOVEL pelo ID
# ----------------------------------------------------
@router.get(
    "/{ato_parteimovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_ATO_PARTEIMOVEL pelo ID",
    response_description="Busca um registro de T_ATO_PARTEIMOVEL em específico",
)
async def show(ato_parteimovel_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_ATO_PARTEIMOVEL com base no ID informado.
    """
    ato_parteimovel_id_schema = TAtoParteImovelIdSchema(
        ato_parteimovel_id=ato_parteimovel_id
    )
    response = t_ato_parteimovel_controller.show(ato_parteimovel_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_ATO_PARTEIMOVEL
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO_PARTEIMOVEL",
    response_description="Cadastra um novo registro em T_ATO_PARTEIMOVEL",
)
async def save(
    t_ato_parteimovel_schema: TAtoParteImovelSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_ATO_PARTEIMOVEL.
    """
    response = t_ato_parteimovel_controller.save(t_ato_parteimovel_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_ATO_PARTEIMOVEL
# ----------------------------------------------------
@router.put(
    "/{ato_parteimovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO_PARTEIMOVEL",
    response_description="Atualiza um registro existente em T_ATO_PARTEIMOVEL",
)
async def update(
    ato_parteimovel_id: int,
    t_ato_parteimovel_update_schema: TAtoParteImovelUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_ATO_PARTEIMOVEL com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    t_ato_parteimovel_update_schema.usuario_id = current_user.data.usuario_id
    t_ato_parteimovel_update_schema.ato_parteimovel_id = ato_parteimovel_id
    response = t_ato_parteimovel_controller.update(t_ato_parteimovel_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_PARTEIMOVEL
# ----------------------------------------------------
@router.delete(
    "/{ato_parteimovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO_PARTEIMOVEL",
    response_description="Remove um registro de T_ATO_PARTEIMOVEL",
)
async def delete(
    ato_parteimovel_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_ATO_PARTEIMOVEL com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    ato_parteimovel_id_schema = TAtoParteImovelIdSchema(
        ato_parteimovel_id=ato_parteimovel_id,
        usuario_id=current_user.data.usuario_id,
    )
    response = t_ato_parteimovel_controller.delete(ato_parteimovel_id_schema)
    return response
