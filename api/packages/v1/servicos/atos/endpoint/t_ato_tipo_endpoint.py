# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_ato_tipo_controller import (
    TAtoTipoController,
)
from packages.v1.servicos.atos.schemas.t_ato_tipo_schema import (
    TAtoTipoSaveSchema,
    TAtoTipoUpdateSchema,
    TAtoTipoIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_ATO_TIPO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_ato_tipo_controller = TAtoTipoController()


# ----------------------------------------------------
# Lista todos os registros de T_ATO_TIPO
# ----------------------------------------------------
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_ATO_TIPO cadastrados",
    response_description="Lista todos os registros de T_ATO_TIPO cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_ATO_TIPO.
    """
    response = t_ato_tipo_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de T_ATO_TIPO pelo ID
# ----------------------------------------------------
@router.get(
    "/{ato_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_ATO_TIPO pelo ID",
    response_description="Busca um registro de T_ATO_TIPO em específico",
)
async def show(
    ato_tipo_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de T_ATO_TIPO com base no ID informado.
    """
    ato_tipo_id_schema = TAtoTipoIdSchema(
        ato_tipo_id=ato_tipo_id
    )
    response = t_ato_tipo_controller.show(ato_tipo_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_ATO_TIPO
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO_TIPO",
    response_description="Cadastra um novo registro em T_ATO_TIPO",
)
async def save(
    t_ato_tipo_schema: TAtoTipoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_ATO_TIPO.
    """
    response = t_ato_tipo_controller.save(t_ato_tipo_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_ATO_TIPO
# ----------------------------------------------------
@router.put(
    "/{ato_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO_TIPO",
    response_description="Atualiza um registro existente em T_ATO_TIPO",
)
async def update(
    ato_tipo_id: int,
    t_ato_tipo_update_schema: TAtoTipoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_ATO_TIPO com base no ID informado.
    """
    t_ato_tipo_update_schema.ato_tipo_id = ato_tipo_id
    response = t_ato_tipo_controller.update(t_ato_tipo_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_TIPO
# ----------------------------------------------------
@router.delete(
    "/{ato_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO_TIPO",
    response_description="Remove um registro de T_ATO_TIPO",
)
async def delete(
    ato_tipo_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_ATO_TIPO com base no ID informado.
    """
    ato_tipo_id_schema = TAtoTipoIdSchema(
        ato_tipo_id=ato_tipo_id
    )
    response = t_ato_tipo_controller.delete(ato_tipo_id_schema)
    return response
