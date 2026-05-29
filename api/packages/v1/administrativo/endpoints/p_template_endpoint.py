from fastapi import APIRouter, Depends, Request, status

from actions.data.get_url_params import get_url_params
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.p_template_controller import (
    PTemplateController,
)
from packages.v1.administrativo.services.p_template.go.p_template_save_editor_callback_service import (
    SaveEditorCallbackService,
)
from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateEditorCallbackSchema,
    PTemplateEditorOpenSchema,
    PTemplateIdSchema,
    PTemplateIndexSchema,
    PTemplateSaveSchema,
    PTemplateUpdateSchema,
)

router = APIRouter()
p_template_controller = PTemplateController()

_PTEMPLATE_INDEX_FILTER_KEYS = frozenset({"template_id", "descricao"})


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista templates",
    response_description="Lista templates",
)
async def index(
    current_user: dict = Depends(get_current_user),
    url_params=Depends(get_url_params),
    query_params=Depends(QueryParamsParser.parse),
):
    filter_data = {
        key: url_params[key] for key in _PTEMPLATE_INDEX_FILTER_KEYS if key in url_params
    }
    template_index_schema = PTemplateIndexSchema(**filter_data)
    return p_template_controller.index(template_index_schema, query_params)


@router.get(
    "/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca template pelo ID",
    response_description="Busca template pelo ID",
)
async def show(
    template_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_template_controller.show(PTemplateIdSchema(template_id=template_id))


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra template",
    response_description="Cadastra template",
)
async def save(
    template_schema: PTemplateSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_template_controller.save(template_schema)


@router.put(
    "/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza template",
    response_description="Atualiza template",
)
async def update(
    template_id: int,
    template_schema: PTemplateUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    return p_template_controller.update(template_id, template_schema)


@router.delete(
    "/{template_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove template",
    response_description="Remove template",
)
async def delete(
    template_id: int,
    current_user: dict = Depends(get_current_user),
):
    return p_template_controller.delete(PTemplateIdSchema(template_id=template_id))


@router.get(
    "/{template_id}/texto/editor",
    status_code=status.HTTP_200_OK,
    summary="Carrega configuração do editor de texto do template",
    response_description="Configuração do editor de texto do template",
)
async def open_text_editor(
    template_id: int,
    request: Request,
    mode: str = "edit",
    highlight_markers: bool = True,
    current_user: dict = Depends(get_current_user),
):
    return p_template_controller.open_editor(
        template_id,
        request,
        PTemplateEditorOpenSchema(mode=mode, highlight_markers=highlight_markers),
    )


@router.post(
    "/{template_id}/texto/callback",
    name="p_template_texto_callback",
    status_code=status.HTTP_200_OK,
    summary="Recebe callback de edição de texto do template",
    response_description="Callback de edição de texto processado",
)
async def texto_callback(
    template_id: int,
    request: Request,
    token: str | None = None,
):
    data = await request.json()
    SaveEditorCallbackService().execute(
        PTemplateEditorCallbackSchema(
            template_id=template_id,
            data=data,
            callback_token=token,
        )
    )
    # OnlyOffice exige payload exato para confirmar persistência.
    return {"error": 0}
