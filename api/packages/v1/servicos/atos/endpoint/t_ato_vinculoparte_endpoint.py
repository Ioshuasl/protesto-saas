# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.atos.controllers.t_ato_vinculoparte_controller import (
    TAtoVinculoParteController,
)
from packages.v1.servicos.atos.schemas.t_ato_vinculoparte_schema import (
    TAtoVinculoParteIndexSchema,
    TAtoVinculoParteSaveSchema,
    TAtoVinculoParteUpdateSchema,
    TAtoVinculoParteIdSchema,
    TAtoVinculoParteTextoQualificacaoUpdateSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_ATO_VINCULOPARTE
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_ato_vinculoparte_controller = TAtoVinculoParteController()


# ----------------------------------------------------
# Lista todos os registros de T_ATO_VINCULOPARTE
# ----------------------------------------------------
@router.get(
    "/ato/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_ATO_VINCULOPARTE cadastrados",
    response_description="Lista todos os registros de T_ATO_VINCULOPARTE cadastrados",
)
async def index(ato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_ATO_VINCULOPARTE.
    """
    data = TAtoVinculoParteIndexSchema(ato_id=ato_id)
    response = t_ato_vinculoparte_controller.index(data)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_ATO_VINCULOPARTE pelo ID
# ----------------------------------------------------
@router.get(
    "/{ato_vinculoparte_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_ATO_VINCULOPARTE pelo ID",
    response_description="Busca um registro de T_ATO_VINCULOPARTE em específico",
)
async def show(
    ato_vinculoparte_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de T_ATO_VINCULOPARTE com base no ID informado.
    """
    ato_vinculoparte_id_schema = TAtoVinculoParteIdSchema(
        ato_vinculoparte_id=ato_vinculoparte_id
    )
    response = t_ato_vinculoparte_controller.show(ato_vinculoparte_id_schema)
    return response


@router.get(
    "/{ato_vinculoparte_id}/texto/qualificacao",
    status_code=status.HTTP_200_OK,
    summary="Busca TEXTO_QUALIFICACAO de T_ATO_VINCULOPARTE pelo ID",
    response_description="Busca TEXTO_QUALIFICACAO de um vínculo de parte",
)
async def show_texto_qualificacao(
    ato_vinculoparte_id: int, current_user: dict = Depends(get_current_user)
):
    data = TAtoVinculoParteIdSchema(ato_vinculoparte_id=ato_vinculoparte_id)
    response = t_ato_vinculoparte_controller.show_texto_qualificacao(data)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_ATO_VINCULOPARTE
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO_VINCULOPARTE",
    response_description="Cadastra um novo registro em T_ATO_VINCULOPARTE",
)
async def save(
    t_ato_vinculoparte_schema: TAtoVinculoParteSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_ATO_VINCULOPARTE.
    """
    response = t_ato_vinculoparte_controller.save(t_ato_vinculoparte_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_ATO_VINCULOPARTE
# ----------------------------------------------------
@router.put(
    "/{ato_vinculoparte_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO_VINCULOPARTE",
    response_description="Atualiza um registro existente em T_ATO_VINCULOPARTE",
)
async def update(
    ato_vinculoparte_id: int,
    t_ato_vinculoparte_update_schema: TAtoVinculoParteUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_ATO_VINCULOPARTE com base no ID informado.
    """
    t_ato_vinculoparte_update_schema.ato_vinculoparte_id = ato_vinculoparte_id
    response = t_ato_vinculoparte_controller.update(t_ato_vinculoparte_update_schema)
    return response


@router.put(
    "/{ato_vinculoparte_id}/texto/qualificacao",
    status_code=status.HTTP_200_OK,
    summary="Atualiza TEXTO_QUALIFICACAO de T_ATO_VINCULOPARTE",
    response_description="Atualiza o TEXTO_QUALIFICACAO de um vínculo de parte",
)
async def update_texto_qualificacao(
    ato_vinculoparte_id: int,
    data: TAtoVinculoParteTextoQualificacaoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.ato_vinculoparte_id = ato_vinculoparte_id
    response = t_ato_vinculoparte_controller.update_texto_qualificacao(data)
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_VINCULOPARTE
# ----------------------------------------------------
@router.delete(
    "/{ato_vinculoparte_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO_VINCULOPARTE",
    response_description="Remove um registro de T_ATO_VINCULOPARTE",
)
async def delete(
    ato_vinculoparte_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_ATO_VINCULOPARTE com base no ID informado.
    """
    current_user = dict_to_namespace(current_user)
    ato_vinculoparte_id_schema = TAtoVinculoParteIdSchema(
        ato_vinculoparte_id=ato_vinculoparte_id,
        usuario_id=current_user.data.usuario_id,
    )
    response = t_ato_vinculoparte_controller.delete(ato_vinculoparte_id_schema)
    return response
