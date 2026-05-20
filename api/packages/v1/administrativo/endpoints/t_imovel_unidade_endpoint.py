# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_imovel_unidade_controller import (
    TImovelUnidadeController,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeIndexSchema,
    TImovelUnidadeSaveSchema,
    TImovelUnidadeUpdateSchema,
    TImovelUnidadeIdSchema,
)

# Inicializa o roteador para as rotas do tipo de reconhecimento
router = APIRouter()

# Instanciamento do controller desejado
t_imovel_unidade_controller = TImovelUnidadeController()


# Lista todos os registros de t_imovel_unidade
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de t_imovel_unidade cadastrados",
    response_description="Lista todos os registros de t_imovel_unidade cadastrados",
)
async def all(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de t_imovel_unidade cadastrados
    response = t_imovel_unidade_controller.all()

    # Retorna os dados localizados
    return response


# Lista todos os registros de t_imovel_unidade
@router.get(
    "/imovel/{imovel_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de t_imovel_unidade cadastrados",
    response_description="Lista todos os registros de t_imovel_unidade cadastrados",
)
async def index(imovel_id: int, current_user: dict = Depends(get_current_user)):

    t_imovel_unidade_index_schema = TImovelUnidadeIndexSchema(imovel_id=imovel_id)

    # Busca todos os registros de t_imovel_unidade cadastrados
    response = t_imovel_unidade_controller.index(t_imovel_unidade_index_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de t_imovel_unidade pelo ID
@router.get(
    "/{imovel_unidade_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de t_imovel_unidade em específico pelo ID",
    response_description="Busca um registro de t_imovel_unidade em específico",
)
async def show(imovel_unidade_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    t_imovel_unidade_id_schema = TImovelUnidadeIdSchema(
        imovel_unidade_id=imovel_unidade_id
    )

    # Busca um registro de t_imovel_unidade específico pelo ID
    response = t_imovel_unidade_controller.show(t_imovel_unidade_id_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de t_imovel_unidade
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um registro de t_imovel_unidade",
    response_description="Cadastra um registro de t_imovel_unidade",
)
async def save(
    t_imovel_unidade_save_schema: TImovelUnidadeSaveSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua o cadastro no banco de dados
    response = t_imovel_unidade_controller.save(t_imovel_unidade_save_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de t_imovel_unidade
@router.put(
    "/{imovel_unidade_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de t_imovel_unidade",
    response_description="Atualiza um registro de t_imovel_unidade",
)
async def update(
    imovel_unidade_id: int,
    t_imovel_unidade_update_schema: TImovelUnidadeUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Adiciona o ID do registro ao schema
    t_imovel_unidade_update_schema.imovel_unidade_id = imovel_unidade_id

    # Efetua a atualização dos dados
    response = t_imovel_unidade_controller.update(t_imovel_unidade_update_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado registro de t_imovel_unidade
@router.delete(
    "/{imovel_unidade_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de t_imovel_unidade",
    response_description="Remove um registro de t_imovel_unidade",
)
async def delete(
    imovel_unidade_id: int, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos
    t_imovel_unidade_id_schema = TImovelUnidadeIdSchema(
        imovel_unidade_id=imovel_unidade_id
    )

    # Efetua a exclusão do registro de t_imovel_unidade
    response = t_imovel_unidade_controller.delete(t_imovel_unidade_id_schema)

    # Retorna os dados localizados
    return response
