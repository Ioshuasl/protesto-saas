# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_censec_qualidadeato_controller import TCensecQualidadeAtoController
from packages.v1.administrativo.schemas.t_censec_qualidadeato_schema import (
    TCensecQualidadeAtoIndexSchema,
    TCensecQualidadeAtoSaveSchema,
    TCensecQualidadeAtoUpdateSchema,
    TCensecQualidadeAtoIdSchema
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_CENSEC_QUALIDADEATO
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_censec_qualidadeato_controller = TCensecQualidadeAtoController()


# ----------------------------------------------------
# Lista todos os registros de T_CENSEC_QUALIDADEATO
# ----------------------------------------------------
@router.get('/tipo-ato/{censec_tipo_ato_id}',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os registros de T_CENSEC_QUALIDADEATO cadastrados',
            response_description='Lista todos os registros de T_CENSEC_QUALIDADEATO cadastrados')
async def index(censec_tipo_ato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_CENSEC_QUALIDADEATO.
    """
    t_censec_qualidadeato_index_schema = TCensecQualidadeAtoIndexSchema(censec_tipoato_id=censec_tipo_ato_id)
    response = t_censec_qualidadeato_controller.index(t_censec_qualidadeato_index_schema)
    return response


# ----------------------------------------------------
# Busca um registro específico de T_CENSEC_QUALIDADEATO pelo ID
# ----------------------------------------------------
@router.get('/{censec_qualidadeato_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro de T_CENSEC_QUALIDADEATO pelo ID',
            response_description='Busca um registro de T_CENSEC_QUALIDADEATO em específico')
async def show(censec_qualidadeato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna um registro específico de T_CENSEC_QUALIDADEATO com base no ID informado.
    """
    t_censec_qualidadeato_id_schema = TCensecQualidadeAtoIdSchema(censec_qualidadeato_id=censec_qualidadeato_id)
    response = t_censec_qualidadeato_controller.show(t_censec_qualidadeato_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_CENSEC_QUALIDADEATO
# ----------------------------------------------------
@router.post('/',
             status_code=status.HTTP_201_CREATED,
             summary='Cadastra um novo registro em T_CENSEC_QUALIDADEATO',
             response_description='Cadastra um novo registro em T_CENSEC_QUALIDADEATO')
async def save(t_censec_qualidadeato_schema: TCensecQualidadeAtoSaveSchema, current_user: dict = Depends(get_current_user)):

    """
    Cria um novo registro na tabela T_CENSEC_QUALIDADEATO.
    """
    response = t_censec_qualidadeato_controller.save(t_censec_qualidadeato_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_CENSEC_QUALIDADEATO
# ----------------------------------------------------
@router.put('/{censec_qualidadeato_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um registro existente em T_CENSEC_QUALIDADEATO',
            response_description='Atualiza um registro existente em T_CENSEC_QUALIDADEATO')
async def update(censec_qualidadeato_id: int, t_censec_qualidadeato_update_schema: TCensecQualidadeAtoUpdateSchema, current_user: dict = Depends(get_current_user)):
    """
    Atualiza um registro existente de T_CENSEC_QUALIDADEATO com base no ID informado.
    """
    t_censec_qualidadeato_update_schema.censec_qualidadeato_id = censec_qualidadeato_id
    response = t_censec_qualidadeato_controller.update(t_censec_qualidadeato_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_CENSEC_QUALIDADEATO
# ----------------------------------------------------
@router.delete('/{censec_qualidadeato_id}',
               status_code=status.HTTP_200_OK,
               summary='Remove um registro de T_CENSEC_QUALIDADEATO',
               response_description='Remove um registro de T_CENSEC_QUALIDADEATO')
async def delete(censec_qualidadeato_id: int, current_user: dict = Depends(get_current_user)):
    """
    Remove um registro específico de T_CENSEC_QUALIDADEATO com base no ID informado.
    """
    t_censec_qualidadeato_id_schema = TCensecQualidadeAtoIdSchema(censec_qualidadeato_id=censec_qualidadeato_id)
    response = t_censec_qualidadeato_controller.delete(t_censec_qualidadeato_id_schema)
    return response
