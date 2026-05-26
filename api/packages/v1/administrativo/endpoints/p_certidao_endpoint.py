from fastapi import APIRouter, Depends, status

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_certidao_controller import (
    PCertidaoController,
)
from packages.v1.administrativo.schemas.p_certidao_schema import (
    PCertidaoConsultaApresentanteSchema,
    PCertidaoIdSchema,
    PCertidaoIndexSchema,
    PCertidaoSaveSchema,
    PCertidaoUpdateSchema,
)

router = APIRouter()
p_certidao_controller = PCertidaoController()

_PCERTIDAO_INDEX_FILTER_KEYS = frozenset(
    {"tipo_certidao", "data_certidao", "data_inicio", "data_fim", "status", "busca"}
)


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista certidões",
    response_description="Lista certidões",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key] for key in _PCERTIDAO_INDEX_FILTER_KEYS if key in url_params
    }
    certidao_index_schema = PCertidaoIndexSchema(**filter_data)
    return p_certidao_controller.index(certidao_index_schema, query_params)


@router.get(
    "/consulta_apresentante/",
    status_code=status.HTTP_200_OK,
    summary="Consulta títulos protestados por apresentante",
    response_description="Consulta títulos protestados por apresentante",
)
async def consulta_apresentante(
    apresentante: str,
    cpfcnpj: str,
    data_inicio: str | None = None,
    data_fim: str | None = None,
    current_user: dict = Depends(get_current_user),
):
    return p_certidao_controller.consulta_apresentante(
        PCertidaoConsultaApresentanteSchema(
            apresentante=apresentante,
            cpfcnpj=cpfcnpj,
            data_inicio=data_inicio,
            data_fim=data_fim,
        )
    )


@router.get(
    "/{certidao_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca certidão pelo ID",
    response_description="Busca certidão pelo ID",
)
async def show(
    certidao_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_certidao_controller.show(PCertidaoIdSchema(certidao_id=certidao_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra certidão",
    response_description="Cadastra certidão",
)
async def save(
    certidao_schema: PCertidaoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_certidao_controller.save(certidao_schema)


@router.put(
    "/{certidao_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza certidão",
    response_description="Atualiza certidão",
)
async def update(
    certidao_id: int,
    certidao_schema: PCertidaoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_certidao_controller.update(certidao_id, certidao_schema)


@router.patch(
    "/{certidao_id}/cancelar",
    status_code=status.HTTP_200_OK,
    summary="Cancela certidão",
    response_description="Cancela certidão ativa",
)
async def cancelar(
    certidao_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_certidao_controller.cancelar(PCertidaoIdSchema(certidao_id=certidao_id))


@router.delete(
    "/{certidao_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove certidão",
    response_description="Remove certidão",
)
async def delete(
    certidao_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_certidao_controller.delete(PCertidaoIdSchema(certidao_id=certidao_id))
