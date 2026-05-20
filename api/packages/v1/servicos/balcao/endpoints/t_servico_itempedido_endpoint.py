from fastapi import APIRouter, Depends, Request, status

from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.balcao.controllers.t_servico_itempedido_controller import (
    TServicoItemPedidoController,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemIndexSchema,
    TServicoItemPedidoCertidaoSaveSchema,
    TServicoItemPedidoIdSchema,
    TServicoItemPedidoQuantidadeSchema,
    TServicoItemPedidoSaveSchema,
    TServicoItemPedidoSituacaoSchema,
    TServicoItemPedidoUpdateSchema,
)


router = APIRouter()
controller = TServicoItemPedidoController()


@router.get(
    "/pedido/{servico_pedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Listar itens do pedido de servico",
    response_description="Itens do pedido de servico localizados com sucesso.",
)
async def index(servico_pedido_id: int, current_user: dict = Depends(get_current_user)):
    data = TServicoItemIndexSchema(servico_pedido_id=servico_pedido_id)
    return controller.index(data)


@router.get(
    "/pedido/{servico_pedido_id}/selos-livres",
    status_code=status.HTTP_200_OK,
    summary="Listar selos livres dos itens do pedido",
    response_description="Selos livres dos itens do pedido localizados com sucesso.",
)
async def selos_livres(
    servico_pedido_id: int, current_user: dict = Depends(get_current_user)
):
    current_user = dict_to_namespace(current_user)
    data = TServicoItemIndexSchema(
        servico_pedido_id=servico_pedido_id,
        usuario_id=current_user.data.usuario_id,
    )

    return controller.selos_livres(data)


@router.get(
    "/{servico_itempedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Buscar item do pedido de servico por ID",
    response_description="Item do pedido de servico localizado com sucesso.",
)
async def show(
    servico_itempedido_id: int, current_user: dict = Depends(get_current_user)
):
    data = TServicoItemPedidoIdSchema(servico_itempedido_id=servico_itempedido_id)
    return controller.show(data)


@router.get(
    "/{servico_itempedido_id}/certidao/exibir",
    status_code=status.HTTP_200_OK,
    summary="Exibir texto da certidao do item",
    response_description="Texto da certidao localizado com sucesso.",
)
async def certidao_show(
    servico_itempedido_id: int, current_user: dict = Depends(get_current_user)
):
    data = TServicoItemPedidoIdSchema(servico_itempedido_id=servico_itempedido_id)
    return controller.certidao_show(data)


@router.get(
    "/{servico_itempedido_id}/certidao/editar",
    status_code=status.HTTP_200_OK,
    summary="Preparar edicao da certidao do item",
    response_description="Arquivo de edicao da certidao gerado com sucesso.",
)
async def certidao_edit(
    servico_itempedido_id: int, current_user: dict = Depends(get_current_user)
):
    data = TServicoItemPedidoIdSchema(servico_itempedido_id=servico_itempedido_id)
    return controller.certidao_edit(data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastrar item do pedido de servico",
    response_description="Item do pedido de servico cadastrado com sucesso.",
)
async def save(
    data: TServicoItemPedidoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    return controller.save(data)


@router.put(
    "/{servico_itempedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualizar item do pedido de servico",
    response_description="Item do pedido de servico atualizado com sucesso.",
)
async def update(
    servico_itempedido_id: int,
    data: TServicoItemPedidoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.servico_itempedido_id = servico_itempedido_id
    return controller.update(data)


@router.put(
    "/{servico_itempedido_id}/cancelar",
    status_code=status.HTTP_200_OK,
    summary="Cancelar item do pedido de servico",
    response_description="Item do pedido de servico cancelado com sucesso.",
)
async def cancelar(
    servico_itempedido_id: int,
    current_user: dict = Depends(dependency=get_current_user),
):
    current_user = dict_to_namespace(current_user)
    return controller.cancelar(
        TServicoItemPedidoSituacaoSchema(
            servico_itempedido_id=servico_itempedido_id,
            usuario_id=current_user.data.usuario_id,
        )
    )


@router.put(
    "/{servico_itempedido_id}/ativar",
    status_code=status.HTTP_200_OK,
    summary="Ativar item do pedido de servico",
    response_description="Item do pedido de servico ativado com sucesso.",
)
async def ativar(
    servico_itempedido_id: int,
    current_user: dict = Depends(dependency=get_current_user),
):
    current_user = dict_to_namespace(current_user)
    return controller.ativar(
        TServicoItemPedidoSituacaoSchema(
            servico_itempedido_id=servico_itempedido_id,
            usuario_id=current_user.data.usuario_id,
        )
    )


@router.put(
    "/{servico_itempedido_id}/quantidade/atualizar",
    status_code=status.HTTP_200_OK,
    summary="Atualizar quantidade do item do pedido",
    response_description="Quantidade do item do pedido atualizada com sucesso.",
)
async def atualiza_quantidade(
    servico_itempedido_id: int,
    data: TServicoItemPedidoQuantidadeSchema,
    current_user: dict = Depends(dependency=get_current_user),
):
    current_user = dict_to_namespace(current_user)
    data.servico_itempedido_id = servico_itempedido_id
    data.usuario_id = current_user.data.usuario_id

    return controller.quantidade_atualizar(data)


@router.post(
    "/{servico_itempedido_id}/certidao/salvar",
    status_code=status.HTTP_200_OK,
    summary="Salvar texto da certidao do item",
    response_description="Texto da certidao salvo com sucesso.",
)
async def certidao_save(servico_itempedido_id: int, request: Request):
    payload = await request.json()
    return controller.certidao_save(
        TServicoItemPedidoCertidaoSaveSchema(
            servico_itempedido_id=servico_itempedido_id,
            data=payload,
        )
    )


@router.delete(
    "/{servico_itempedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Remover item do pedido de servico",
    response_description="Item do pedido de servico removido com sucesso.",
)
async def delete(
    servico_itempedido_id: int, current_user: dict = Depends(get_current_user)
):
    data = TServicoItemPedidoIdSchema(servico_itempedido_id=servico_itempedido_id)
    return controller.delete(data)
