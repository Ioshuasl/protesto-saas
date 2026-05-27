from fastapi import APIRouter, Depends, status

from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.tabelionato_protesto_controller import (
    TabelionatoProtestoController,
)

router = APIRouter()
tabelionato_protesto_controller = TabelionatoProtestoController()


@router.get(
    "/dashboard/resumo",
    status_code=status.HTTP_200_OK,
    summary="Resumo de indicadores do dashboard de protesto",
    response_description="Total de títulos, tríduo, liquidados e protestados",
)
async def dashboard_resumo(
    current_user: dict = Depends(get_current_user),
):
    return tabelionato_protesto_controller.dashboard_resumo()


@router.get(
    "/dashboard/funil",
    status_code=status.HTTP_200_OK,
    summary="Funil semanal de títulos",
    response_description="Série semanal de apontados, liquidados e protestados",
)
async def dashboard_funil(
    current_user: dict = Depends(get_current_user),
):
    return tabelionato_protesto_controller.dashboard_funil()
