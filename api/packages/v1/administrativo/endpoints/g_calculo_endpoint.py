# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_calculo_controller import (
    GCalculoController,
)
from packages.v1.administrativo.schemas.g_calculo_schema import (
    GCalculoRapidoSchema,
    GCalculoServico,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela G_EMOLUMENTO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
g_calculo_controller = GCalculoController()


# ----------------------------------------------------
# Lista todos os registros de G_EMOLUMENTO
# ----------------------------------------------------
@router.post(
    "/rapido",
    status_code=status.HTTP_200_OK,
    summary="Realiza um cáculo simples dos emolumentos",
    response_description="Realiza um cáculo simples dos emolumentos",
)
async def index(
    g_calculo_rapido_schema: GCalculoRapidoSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna todos os registros da tabela G_EMOLUMENTO.
    """
    response = g_calculo_controller.rapido(g_calculo_rapido_schema)
    return response


# ----------------------------------------------------
# Lista todos os registros de G_EMOLUMENTO
# ----------------------------------------------------
@router.post(
    "/servico",
    status_code=status.HTTP_200_OK,
    summary="Realiza um cáculo simples dos emolumentos",
    response_description="Realiza um cáculo simples dos emolumentos",
)
async def servico(
    g_calculo_servico: GCalculoServico,
    current_user: dict = Depends(get_current_user),
):
    """
    Retorna todos os registros da tabela G_EMOLUMENTO.
    """
    response = g_calculo_controller.servico(g_calculo_servico)
    return response
