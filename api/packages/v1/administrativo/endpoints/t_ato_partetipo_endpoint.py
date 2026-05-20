# ----------------------------------------------------
# Importação de bibliotecas e dependências
# ----------------------------------------------------
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_ato_partetipo_controller import TAtoParteTipoController
from packages.v1.administrativo.schemas.t_ato_partetipo_schema import (
    TAtoParteTipoSaveSchema,
    TAtoParteTipoUpdateSchema,
    TAtoParteTipoIdSchema
)

# ----------------------------------------------------
# Inicialização do roteador da tabela T_ATO_PARTETIPO
# ----------------------------------------------------
router = APIRouter()

# Instancia o controller da tabela T_ATO_PARTETIPO
t_ato_partetipo_controller = TAtoParteTipoController()

# ----------------------------------------------------
# Lista todos os registros de T_ATO_PARTETIPO
# ----------------------------------------------------
@router.get(
    '/',
    status_code=status.HTTP_200_OK,
    summary='Lista todos os registros de T_ATO_PARTETIPO cadastrados',
    response_description='Lista todos os registros de T_ATO_PARTETIPO cadastrados'
)
async def index(
    current_user: dict = Depends(get_current_user)
):
    """
    Lista todos os registros da tabela T_ATO_PARTETIPO de acordo com o ID de qualidade CENSEC.
    """

    # Executa a busca dos registros
    response = t_ato_partetipo_controller.index()

    # Retorna os registros localizados
    return response


# ----------------------------------------------------
# Localiza um registro de T_ATO_PARTETIPO pelo ID
# ----------------------------------------------------
@router.get(
    '/{ato_partetipo_id}',
    status_code=status.HTTP_200_OK,
    summary='Busca um registro de T_ATO_PARTETIPO em específico pelo ID',
    response_description='Busca um registro de T_ATO_PARTETIPO em específico'
)
async def show(
    ato_partetipo_id: int, 
    current_user: dict = Depends(get_current_user)
):
    """
    Localiza um registro específico de T_ATO_PARTETIPO pelo seu ID.
    """
    # Cria o schema com o ID recebido
    t_ato_partetipo_id_schema = TAtoParteTipoIdSchema(ato_partetipo_id=ato_partetipo_id)

    # Executa a busca do registro
    response = t_ato_partetipo_controller.show(t_ato_partetipo_id_schema)

    # Retorna o resultado
    return response


# ----------------------------------------------------
# Cadastra um novo registro de T_ATO_PARTETIPO
# ----------------------------------------------------
@router.post(
    '/',
    status_code=status.HTTP_201_CREATED,
    summary='Cadastra um registro de T_ATO_PARTETIPO',
    response_description='Cadastra um registro de T_ATO_PARTETIPO'
)
async def save(
    t_ato_partetipo_schema: TAtoParteTipoSaveSchema, 
    current_user: dict = Depends(get_current_user)
):
    """
    Realiza o cadastro de um novo registro na tabela T_ATO_PARTETIPO.
    """
    # Executa a operação de salvamento
    response = t_ato_partetipo_controller.save(t_ato_partetipo_schema)

    # Retorna o registro criado
    return response


# ----------------------------------------------------
# Atualiza os dados de um registro existente
# ----------------------------------------------------
@router.put(
    '/{ato_partetipo_id}',
    status_code=status.HTTP_200_OK,
    summary='Atualiza um registro de T_ATO_PARTETIPO',
    response_description='Atualiza um registro de T_ATO_PARTETIPO'
)
async def update(
    ato_partetipo_id: int,
    t_ato_partetipo_update_schema: TAtoParteTipoUpdateSchema,
    current_user: dict = Depends(get_current_user)
):
    """
    Atualiza os dados de um registro existente na tabela T_ATO_PARTETIPO.
    """
    # Define o ID no schema de atualização
    t_ato_partetipo_update_schema.ato_partetipo_id = ato_partetipo_id

    # Executa a atualização
    response = t_ato_partetipo_controller.update(t_ato_partetipo_update_schema)

    # Retorna o registro atualizado
    return response


# ----------------------------------------------------
# Exclui um registro de T_ATO_PARTETIPO
# ----------------------------------------------------
@router.delete(
    '/{ato_partetipo_id}',
    status_code=status.HTTP_200_OK,
    summary='Remove um registro de T_ATO_PARTETIPO',
    response_description='Remove um registro de T_ATO_PARTETIPO'
)
async def delete(
    ato_partetipo_id: int, 
    current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro da tabela T_ATO_PARTETIPO com base no ID informado.
    """
    # Monta o schema de exclusão
    t_ato_partetipo_schema = TAtoParteTipoIdSchema(ato_partetipo_id=ato_partetipo_id)

    # Executa a exclusão
    response = t_ato_partetipo_controller.delete(t_ato_partetipo_schema)

    # Retorna o resultado da operação
    return response
