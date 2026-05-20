from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from fastapi import APIRouter, Depends, status
from packages.v1.servicos.atos.controllers.t_ato_controller import TAtoController
from packages.v1.servicos.atos.schemas.t_ato_schema import (
    TAtoClearTextoAssinaturaSchema,
    TAtoClearTextoFinalizacaoSchema,
    TAtoClearTextoSchema,
    TAtoIdSchema,
    TAtoLavraturaSchema,
    TAtoSaveMinuta,
    TAtoSaveSchema,
    TAtoTextoAssinatura,
    TAtoTextoAssinaturaUpdateSchema,
    TAtoAnteriorClearSchema,
    TAtoAnteriorUpdateSchema,
    TAtoTextoFinalizacao,
    TAtoTextoVisualizarSchema,
    TAtoUpdateSchema,
)

router = APIRouter()
controller = TAtoController


@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista registros de T_ATO",
    response_description="Lista de registros de T_ATO",
)
async def index(current_user: dict = Depends(get_current_user)):
    return controller().index()


@router.get(
    "/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca registro de T_ATO por ID",
    response_description="Registro de T_ATO",
)
async def show(ato_id: int, current_user: dict = Depends(get_current_user)):
    ato_id_schema = TAtoIdSchema(ato_id=ato_id)
    return controller().show(ato_id_schema)


@router.get(
    "/{ato_id}/arquivos",
    status_code=status.HTTP_200_OK,
    summary="Lista arquivos vinculados ao ato",
    response_description="Arquivos do ato",
)
async def show_arquivos(ato_id: int, current_user: dict = Depends(get_current_user)):
    ato_id_schema = TAtoIdSchema(ato_id=ato_id)
    return controller().index_arquivos(ato_id_schema)


@router.get(
    "/{ato_id}/ato-anterior",
    status_code=status.HTTP_200_OK,
    summary="Busca dados do ato anterior pelo ato atual",
    response_description="Dados do ato anterior",
)
async def ato_anterior(ato_id: int, current_user: dict = Depends(get_current_user)):
    ato_id_schema = TAtoIdSchema(ato_id=ato_id)
    return controller().ato_anterior(ato_id_schema)


@router.put(
    "/{ato_id}/ato-anterior",
    status_code=status.HTTP_200_OK,
    summary="Atualiza dados do ato anterior pelo ato atual",
    response_description="Dados do ato anterior atualizados",
)
async def update_ato_anterior(
    ato_id: int,
    data: TAtoAnteriorUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.ato_id = ato_id
    return controller().update_ato_anterior(data)


@router.put(
    "/{ato_id}/ato-anterior/limpar",
    status_code=status.HTTP_200_OK,
    summary="Limpa dados do ato anterior pelo ato atual",
    response_description="Dados do ato anterior limpos",
)
async def clear_ato_anterior(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    data = TAtoAnteriorClearSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().clear_ato_anterior(data)


@router.get(
    "/{ato_id}/texto",
    status_code=status.HTTP_200_OK,
    summary="Busca texto corpo do ato",
    response_description="Texto corpo do ato",
)
async def get_texto(ato_id: int, current_user: dict = Depends(get_current_user)):
    ato_id_schema = TAtoIdSchema(ato_id=ato_id)
    return controller().get_texto(ato_id_schema)


@router.put(
    "/{ato_id}/texto/limpar",
    status_code=status.HTTP_200_OK,
    summary="Limpa texto corpo do ato",
    response_description="Texto corpo do ato definido como nulo",
)
async def clear_texto(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    data = TAtoClearTextoSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().clear_texto(data)


@router.get(
    "/{ato_id}/texto/visualizar/{tipo_visualizacao}",
    status_code=status.HTTP_200_OK,
    summary="Busca texto para livro",
    response_description="Texto de livro",
)
async def display_texto(
    ato_id: int, tipo_visualizacao: int, current_user: dict = Depends(get_current_user)
):
    ato_id_schema = TAtoTextoVisualizarSchema(ato_id=ato_id, tipo_visualizacao=tipo_visualizacao)
    return controller().display_texto(ato_id_schema)


@router.get(
    "/{ato_id}/texto/finalizacao/{tipo_finalizacao}",
    status_code=status.HTTP_200_OK,
    summary="Busca texto de finalizacao",
    response_description="Texto de finalizacao",
)
async def get_texto_finalizacao(
    ato_id: int,
    tipo_finalizacao: int,
    current_user: dict = Depends(get_current_user),
):
    data = TAtoTextoFinalizacao(ato_id=ato_id, tipo_finalizacao=tipo_finalizacao)
    return controller().show_finalizacao(data)


@router.put(
    "/{ato_id}/texto/finalizacao/{tipo_finalizacao}/limpar",
    status_code=status.HTTP_200_OK,
    summary="Limpa texto de finalizacao do ato",
    response_description="Texto de finalizacao do ato definido como nulo",
)
async def clear_finalizacao(
    ato_id: int,
    tipo_finalizacao: int,
    current_user: dict = Depends(get_current_user),
):
    current_user = dict_to_namespace(current_user)
    data = TAtoClearTextoFinalizacaoSchema(
        ato_id=ato_id,
        tipo_finalizacao=tipo_finalizacao,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().clear_finalizacao(data)


@router.get(
    "/{ato_id}/recibo-protocolo",
    status_code=status.HTTP_200_OK,
    summary="Dados para recibo de protocolo",
    response_description="Dados do ato para geracao do recibo de protocolo",
)
async def recibo_protocolo(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    ato_id_schema = TAtoIdSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().recibo_protocolo(ato_id_schema)


@router.post(
    "/{ato_id}/lavrar-ato",
    status_code=status.HTTP_200_OK,
    summary="Lavra o ato",
    response_description="Ato atualizado para status lavrado",
)
async def lavrar_ato(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    ato_id_schema = TAtoLavraturaSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().lavrar_ato(ato_id_schema)


@router.post(
    "/{ato_id}/retirar-lavratura",
    status_code=status.HTTP_200_OK,
    summary="Retira a lavratura do ato",
    response_description="Ato atualizado apos limpar dados de lavratura",
)
async def retirar_lavratura(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    ato_id_schema = TAtoIdSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().retirar_lavratura(ato_id_schema)


@router.post(
    "/{ato_id}/cancelar-ato",
    status_code=status.HTTP_200_OK,
    summary="Cancela o ato",
    response_description="Ato com situacao cancelada e data de cancelamento",
)
async def cancelar_ato(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    ato_id_schema = TAtoIdSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().cancelar_ato(ato_id_schema)


@router.post(
    "/{ato_id}/reativar-ato",
    status_code=status.HTTP_200_OK,
    summary="Reativa o ato cancelado",
    response_description="Ato reativado",
)
async def reativar_ato(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    ato_id_schema = TAtoIdSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().reativar_ato(ato_id_schema)


@router.post(
    "/{ato_id}/protocolar",
    status_code=status.HTTP_200_OK,
    summary="Protocola um ato",
    response_description="Registro atualizado com numero de protocolo",
)
async def protocolar(ato_id: int, current_user: dict = Depends(get_current_user)):
    current_user = dict_to_namespace(current_user)
    ato_id_schema = TAtoIdSchema(
        ato_id=ato_id,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().protocolar(ato_id_schema)


@router.get(
    "/{ato_id}/texto/assinatura/{tipo_assinatura}",
    status_code=status.HTTP_200_OK,
    summary="Busca texto de assinatura do ato",
    response_description="Texto de assinatura do ato",
)
async def get_texto_assinatura(
    ato_id: int,
    tipo_assinatura: int,
    current_user: dict = Depends(get_current_user),
):
    data = TAtoTextoAssinatura(ato_id=ato_id, tipo_assinatura=tipo_assinatura)
    return controller().show_assinatura(data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_ATO",
    response_description="Registro de T_ATO criado",
)
async def save(
    t_ato_schema: TAtoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    current_user = dict_to_namespace(current_user)
    t_ato_schema.usuario_id = current_user.data.usuario_id
    return controller().save(t_ato_schema)


@router.put(
    "/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_ATO",
    response_description="Registro de T_ATO atualizado",
)
async def update(
    ato_id: int,
    t_ato_update_schema: TAtoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    t_ato_update_schema.ato_id = ato_id
    return controller().update(t_ato_update_schema)


@router.put(
    "/{ato_id}/texto/minuta",
    status_code=status.HTTP_200_OK,
    summary="Atualiza texto de minuta do ato",
    response_description="Ato atualizado com nova minuta",
)
async def update_minuta(
    ato_id: int,
    data: TAtoSaveMinuta,
    current_user: dict = Depends(get_current_user),
):
    data.ato_id = ato_id
    return controller().update_minuta(data)


@router.put(
    "/{ato_id}/texto/assinatura/{tipo_assinatura}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza texto de assinatura do ato",
    response_description="Ato atualizado com novo texto de assinatura",
)
async def update_assinatura(
    ato_id: int,
    tipo_assinatura: int,
    data: TAtoTextoAssinaturaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.ato_id = ato_id
    data.tipo_finalizacao = tipo_assinatura
    return controller().update_assinatura(data)


@router.put(
    "/{ato_id}/texto/assinatura/{tipo_assinatura}/limpar",
    status_code=status.HTTP_200_OK,
    summary="Limpa texto de assinatura do ato",
    response_description="Texto de assinatura do ato definido como nulo",
)
async def clear_assinatura(
    ato_id: int,
    tipo_assinatura: int,
    current_user: dict = Depends(get_current_user),
):
    current_user = dict_to_namespace(current_user)
    data = TAtoClearTextoAssinaturaSchema(
        ato_id=ato_id,
        tipo_assinatura=tipo_assinatura,
        usuario_id=current_user.data.usuario_id,
    )
    return controller().clear_assinatura(data)


@router.delete(
    "/{ato_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_ATO",
    response_description="Registro de T_ATO removido",
)
async def delete(ato_id: int, current_user: dict = Depends(get_current_user)):
    ato_id_schema = TAtoIdSchema(ato_id=ato_id)
    return controller().delete(ato_id_schema)
