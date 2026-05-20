# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_biometria_pessoa_controller import (
    TBiometriaPessoaController,
)
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaSaveSchema,
    TBiometriaPessoaUpdateSchema,
    TBiometriaPessoaIdSchema,
    TBiometriaPessoaIndexSchema,
)

# ----------------------------------------------------
# Inicializa o roteador para as rotas da tabela T_BIOMETRIA_PESSOA
# ----------------------------------------------------
router = APIRouter()

# Instanciamento do controller
t_biometria_pessoa_controller = TBiometriaPessoaController()


# ----------------------------------------------------
# Lista todos os registros de T_BIOMETRIA_PESSOA
# ----------------------------------------------------
@router.get(
    "/pessoa/{chave_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de T_BIOMETRIA_PESSOA cadastrados",
    response_description="Lista todos os registros de T_BIOMETRIA_PESSOA cadastrados",
)
async def index(chave_id: int, current_user: dict = Depends(get_current_user)):
    """
    Retorna todos os registros da tabela T_BIOMETRIA_PESSOA.
    """
    response = t_biometria_pessoa_controller.index(
        TBiometriaPessoaIndexSchema(chave_id=chave_id)
    )
    return response


# ----------------------------------------------------
# Busca um registro específico de T_BIOMETRIA_PESSOA pelo ID
# ----------------------------------------------------
@router.get(
    "/{biometria_pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de T_BIOMETRIA_PESSOA pelo ID",
    response_description="Busca um registro de T_BIOMETRIA_PESSOA em específico",
)
async def show(
    biometria_pessoa_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Retorna um registro específico de T_BIOMETRIA_PESSOA com base no ID informado.
    """
    t_biometria_pessoa_id_schema = TBiometriaPessoaIdSchema(
        biometria_pessoa_id=biometria_pessoa_id
    )
    response = t_biometria_pessoa_controller.show(t_biometria_pessoa_id_schema)
    return response


# ----------------------------------------------------
# Cadastra um novo registro em T_BIOMETRIA_PESSOA
# ----------------------------------------------------
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um novo registro em T_BIOMETRIA_PESSOA",
    response_description="Cadastra um novo registro em T_BIOMETRIA_PESSOA",
)
async def save(
    t_biometria_pessoa_schema: TBiometriaPessoaSaveSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Cria um novo registro na tabela T_BIOMETRIA_PESSOA.
    """
    response = t_biometria_pessoa_controller.save(t_biometria_pessoa_schema)
    return response


# ----------------------------------------------------
# Atualiza um registro existente de T_BIOMETRIA_PESSOA
# ----------------------------------------------------
@router.put(
    "/{biometria_pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro existente em T_BIOMETRIA_PESSOA",
    response_description="Atualiza um registro existente em T_BIOMETRIA_PESSOA",
)
async def update(
    biometria_pessoa_id: int,
    t_biometria_pessoa_update_schema: TBiometriaPessoaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):
    """
    Atualiza um registro existente de T_BIOMETRIA_PESSOA com base no ID informado.
    """
    t_biometria_pessoa_update_schema.biometria_pessoa_id = biometria_pessoa_id
    response = t_biometria_pessoa_controller.update(t_biometria_pessoa_update_schema)
    return response


# ----------------------------------------------------
# Exclui um registro de T_BIOMETRIA_PESSOA
# ----------------------------------------------------
@router.delete(
    "/{biometria_pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de T_BIOMETRIA_PESSOA",
    response_description="Remove um registro de T_BIOMETRIA_PESSOA",
)
async def delete(
    biometria_pessoa_id: int, current_user: dict = Depends(get_current_user)
):
    """
    Remove um registro específico de T_BIOMETRIA_PESSOA com base no ID informado.
    """
    t_biometria_pessoa_id_schema = TBiometriaPessoaIdSchema(
        biometria_pessoa_id=biometria_pessoa_id
    )
    response = t_biometria_pessoa_controller.delete(t_biometria_pessoa_id_schema)
    return response
