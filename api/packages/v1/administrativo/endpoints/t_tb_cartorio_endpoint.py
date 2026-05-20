from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_tb_cartorio_controller import TTbCartorioController
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema, TTbCartorioSaveSchema
router = APIRouter()
controller = TTbCartorioController()
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista cartorios",
    response_description="Lista cartorios",
)
async def index(current_user: dict = Depends(get_current_user)):
    return controller.index()
@router.get(
    "/{tb_cartorio_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca cartorio por ID",
    response_description="Busca cartorio por ID",
)
async def show(tb_cartorio_id: float, current_user: dict = Depends(get_current_user)):
    return controller.show(TTbCartorioIdSchema(tb_cartorio_id=tb_cartorio_id))
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Salva cartorio",
    response_description="Salva cartorio",
)
async def save(cartorio_schema: TTbCartorioSaveSchema, current_user: dict = Depends(get_current_user)):
    return controller.save(cartorio_schema)
@router.delete(
    "/{tb_cartorio_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove cartorio",
    response_description="Remove cartorio",
)
async def delete(tb_cartorio_id: float, current_user: dict = Depends(get_current_user)):
    return controller.delete(TTbCartorioIdSchema(tb_cartorio_id=tb_cartorio_id))
