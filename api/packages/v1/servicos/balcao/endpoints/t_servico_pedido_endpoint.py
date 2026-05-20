from fastapi import APIRouter, Depends, status
from actions.data.dict_to_namespace import dict_to_namespace
from actions.jwt.get_current_user import get_current_user
from packages.v1.servicos.balcao.controllers.t_servico_pedido_controller import (
    TServicoPedidoController,
)
from packages.v1.servicos.balcao.schemas.t_servico_pedido_schema import (
    TServicoPedidoSaveSchema,
    TServicoPedidoSituacaoSchema,
    TServicoPedidoUpdateSchema,
    TServicoPedidoIdSchema,
)

router = APIRouter()
controller = TServicoPedidoController()

# Endpoints T_SERVICO_PEDIDO
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista pedidos de serviço",
    response_description="Lista de pedidos de serviço",
)
async def index(current_user: dict = Depends(get_current_user)):
    return controller.index()


@router.get(
    "/load-params",
    status_code=status.HTTP_200_OK,
    summary="Carrega parâmetros para pedidos de serviço",
    response_description="Parâmetros necessários para pedidos de serviço",
)
async def load_params(current_user: dict = Depends(get_current_user)):
    return controller.load_params()


@router.get(
    "/{servico_pedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca pedido de serviço por ID",
    response_description="Pedido de serviço encontrado",
)
async def show(servico_pedido_id: int, current_user: dict = Depends(get_current_user)):
    data = TServicoPedidoIdSchema(servico_pedido_id=servico_pedido_id)
    return controller.show(data)


@router.get(
    "/{servico_pedido_id}/recibo",
    status_code=status.HTTP_200_OK,
    summary="Busca recibo do pedido de serviço",
    response_description="Recibo do pedido de serviço",
)
async def show_recibo(
    servico_pedido_id: int, current_user: dict = Depends(get_current_user)
):
    data = TServicoPedidoIdSchema(servico_pedido_id=servico_pedido_id)
    return controller.show_recibo(data)


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cria pedido de serviço",
    response_description="Pedido de serviço criado",
)
async def save(
    data: TServicoPedidoSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    current_user = dict_to_namespace(current_user)

    data.usuario_id = current_user.data.usuario_id

    return controller.save(data)


@router.put(
    "/{servico_pedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza pedido de serviço",
    response_description="Pedido de serviço atualizado",
)
async def update(
    servico_pedido_id: int,
    data: TServicoPedidoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    data.servico_pedido_id = servico_pedido_id
    return controller.update(data)


@router.put(
    "/{servico_pedido_id}/finalizar",
    status_code=status.HTTP_200_OK,
    summary="Finaliza pedido de serviço",
    response_description="Pedido de serviço finalizado",
)
async def finalizar(
    servico_pedido_id: int,
    current_user: dict = Depends(dependency=get_current_user),
):
    current_user = dict_to_namespace(current_user)

    return controller.finalizar(
        TServicoPedidoSituacaoSchema(
            servico_pedido_id=servico_pedido_id,
            usuario_id=current_user.data.usuario_id,
        )
    )


@router.put(
    "/{servico_pedido_id}/cancelar",
    status_code=status.HTTP_200_OK,
    summary="Cancela pedido de serviço",
    response_description="Pedido de serviço cancelado",
)
async def cancelar(
    servico_pedido_id: int,
    current_user: dict = Depends(dependency=get_current_user),
):
    current_user = dict_to_namespace(current_user)

    return controller.cancelar(
        TServicoPedidoSituacaoSchema(
            servico_pedido_id=servico_pedido_id,
            usuario_id=current_user.data.usuario_id,
        )
    )


@router.put(
    "/{servico_pedido_id}/ativar",
    status_code=status.HTTP_200_OK,
    summary="Ativa pedido de serviço",
    response_description="Pedido de serviço ativado",
)
async def ativar(
    servico_pedido_id: int,
    current_user: dict = Depends(dependency=get_current_user),
):
    current_user = dict_to_namespace(current_user)

    return controller.ativar(
        TServicoPedidoSituacaoSchema(
            servico_pedido_id=servico_pedido_id,
            usuario_id=current_user.data.usuario_id,
        )
    )


@router.delete(
    "/{servico_pedido_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove pedido de serviço",
    response_description="Pedido de serviço removido",
)
async def delete(
    servico_pedido_id: int, current_user: dict = Depends(get_current_user)
):
    data = TServicoPedidoIdSchema(servico_pedido_id=servico_pedido_id)
    return controller.delete(data)
