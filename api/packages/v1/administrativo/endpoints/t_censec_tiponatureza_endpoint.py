# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_censec_tiponatureza_controller import (
    TCensecTipoNaturezaController,
)
from packages.v1.administrativo.schemas.t_censec_tiponatureza_schema import (
    TCensecTipoNaturezaSaveSchema,
    TCensecTipoNaturezaUpdateSchema,
    TCensecTipoNaturezaIdSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_CENSEC_TIPONATUREZA
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_censec_tiponatureza_controller = TCensecTipoNaturezaController()


# ----------------------------------------------------
# Lista todos os registros de T_CENSEC_TIPONATUREZA
# ----------------------------------------------------
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_CENSEC_TIPONATUREZA cadastrados",
    response_description="Lista todos os registros de T_CENSEC_TIPONATUREZA cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_CENSEC_TIPONATUREZA.
    """
    response = t_censec_tiponatureza_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de T_CENSEC_TIPONATUREZA pelo ID
# ----------------------------------------------------
@router.get(
    "/{censec_tiponatureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_CENSEC_TIPONATUREZA pelo ID",
    response_description="Busca um registro de T_CENSEC_TIPONATUREZA em específico",
)
async def show(
    censec_tiponatureza_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de T_CENSEC_TIPONATUREZA com base no ID informado.
    """
    t_censec_tiponatureza_id_schema = TCensecTipoNaturezaIdSchema(
        censec_tiponatureza_id=censec_tiponatureza_id
    )
    response = t_censec_tiponatureza_controller.show(t_censec_tiponatureza_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_CENSEC_TIPONATUREZA
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_CENSEC_TIPONATUREZA",
    response_description="Cadastra um novo registro em T_CENSEC_TIPONATUREZA",
)
async def save(
    t_censec_tiponatureza_schema: TCensecTipoNaturezaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_CENSEC_TIPONATUREZA.
    """
    response = t_censec_tiponatureza_controller.save(t_censec_tiponatureza_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_CENSEC_TIPONATUREZA
# ----------------------------------------------------
@router.put(
    "/{censec_tiponatureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_CENSEC_TIPONATUREZA",
    response_description="Atualiza um registro existente em T_CENSEC_TIPONATUREZA",
)
async def update(
    censec_tiponatureza_id: int,
    t_censec_tiponatureza_update_schema: TCensecTipoNaturezaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_CENSEC_TIPONATUREZA com base no ID informado.
    """
    t_censec_tiponatureza_update_schema.censec_tiponatureza_id = censec_tiponatureza_id
    response = t_censec_tiponatureza_controller.update(
        t_censec_tiponatureza_update_schema
    )
    return response


# ----------------------------------------------------
# Exclui um registro de T_CENSEC_TIPONATUREZA
# ----------------------------------------------------
@router.delete(
    "/{censec_tiponatureza_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_CENSEC_TIPONATUREZA",
    response_description="Remove um registro de T_CENSEC_TIPONATUREZA",
)
async def delete(
    censec_tiponatureza_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_CENSEC_TIPONATUREZA com base no ID informado.
    """
    t_censec_tiponatureza_id_schema = TCensecTipoNaturezaIdSchema(
        censec_tiponatureza_id=censec_tiponatureza_id
    )
    response = t_censec_tiponatureza_controller.delete(t_censec_tiponatureza_id_schema)
    return response
