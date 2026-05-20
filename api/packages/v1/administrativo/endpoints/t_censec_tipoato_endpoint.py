# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_censec_tipoato_controller import TCensecTipoAtoController
from packages.v1.administrativo.schemas.t_censec_tipoato_schema import (
    TCensecTipoAtoSaveSchema,
    TCensecTipoAtoUpdateSchema,
    TCensecTipoAtoIdSchema
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_CENSEC_TIPOATO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_censec_tipoato_controller = TCensecTipoAtoController()


# ----------------------------------------------------
# Lista todos os registros de T_CENSEC_TIPOATO
# ----------------------------------------------------
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de T_CENSEC_TIPOATO cadastrados',
            response_description='Lista todos os registros de T_CENSEC_TIPOATO cadastrados')
async def index(current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_CENSEC_TIPOATO.
    """
    response = t_censec_tipoato_controller.index()
    return response


# ----------------------------------------------------
# Busca um registro específico de T_CENSEC_TIPOATO pelo ID
# ----------------------------------------------------
@router.get('/{censec_tipoato_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de T_CENSEC_TIPOATO pelo ID',
            response_description='Busca um registro de T_CENSEC_TIPOATO em específico')
async def show(censec_tipoato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_CENSEC_TIPOATO com base no ID informado.
    """
    t_censec_tipoato_id_schema = TCensecTipoAtoIdSchema(censec_tipoato_id=censec_tipoato_id)
    response = t_censec_tipoato_controller.show(t_censec_tipoato_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_CENSEC_TIPOATO
# ----------------------------------------------------
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Cadastra um novo registro em T_CENSEC_TIPOATO',
             response_description='Cadastra um novo registro em T_CENSEC_TIPOATO')
async def save(t_censec_tipoato_schema: TCensecTipoAtoSaveSchema, current_user: dict = Depends(get_current_user)):
    """
    Cria um novo registro na tabela T_CENSEC_TIPOATO.
    """
    response = t_censec_tipoato_controller.save(t_censec_tipoato_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_CENSEC_TIPOATO
# ----------------------------------------------------
@router.put('/{censec_tipoato_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro existente em T_CENSEC_TIPOATO',
            response_description='Atualiza um registro existente em T_CENSEC_TIPOATO')
async def update(censec_tipoato_id: int, t_censec_tipoato_update_schema: TCensecTipoAtoUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Atualiza um registro existente de T_CENSEC_TIPOATO com base no ID informado.
    """
    t_censec_tipoato_update_schema.censec_tipoato_id = censec_tipoato_id
    response = t_censec_tipoato_controller.update(t_censec_tipoato_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_CENSEC_TIPOATO
# ----------------------------------------------------
@router.delete('/{censec_tipoato_id}',
               status_code=status.HTTP_200_OK,
               summary='Remove um registro de T_CENSEC_TIPOATO',
               response_description='Remove um registro de T_CENSEC_TIPOATO')
async def delete(censec_tipoato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de T_CENSEC_TIPOATO com base no ID informado.
    """
    t_censec_tipoato_id_schema = TCensecTipoAtoIdSchema(censec_tipoato_id=censec_tipoato_id)
    response = t_censec_tipoato_controller.delete(t_censec_tipoato_id_schema)
    return response