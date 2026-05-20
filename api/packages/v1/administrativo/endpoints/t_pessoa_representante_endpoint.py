# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_pessoa_representante_controller import (
    TPessoaRepresentanteController,
)
from packages.v1.administrativo.schemas.t_pessoa_representante_schema import (
    TPessoaRepresentanteIdSchema,
    TPessoaRepresentantePessoaIdSchema,
    TPessoaRepresentanteSaveSchema,
    TPessoaRepresentanteUpdateSchema,
)

# Inicializa o roteador para as rotas do regime de bens
router = APIRouter()

# Instânciamento do controller desejado
t_pessoa_representante_controller = TPessoaRepresentanteController()


# Lista todos as pessoas
@router.get(
    "/pessoa/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos as pessoas cadastrados",
    response_description="Lista todos as pessoas cadastrados",
)
async def index(pessoa_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    t_pessoa_representante_pessoa_id_schema = TPessoaRepresentantePessoaIdSchema(
        pessoa_id=pessoa_id
    )

    # Busca todos as pessoas cadastrados
    response = t_pessoa_representante_controller.index(
        t_pessoa_representante_pessoa_id_schema
    )

    # Retorna os dados localizados
    return response


# Localiza um regime de bens pelo ID
@router.get(
    "/{pessoa_representante_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em específico pelo ID da pessoa",
    response_description="Busca um registro em específico",
)
async def show(
    pessoa_representante_id: int, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos
    t_pessoa_representante_id_schema = TPessoaRepresentanteIdSchema(
        pessoa_representante_id=pessoa_representante_id
    )

    # Busca um regime de bens específico pelo ID
    response = t_pessoa_representante_controller.show(t_pessoa_representante_id_schema)

    # Retorna os dados localizados
    return response


# Cadastro de regime de bens
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um regime de bens",
    response_description="Cadastra um regime de bens",
)
async def save(
    t_pessoa_representante_save_schema: TPessoaRepresentanteSaveSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua o cadastro no banco de dados
    response = t_pessoa_representante_controller.save(
        t_pessoa_representante_save_schema
    )

    # Retorna os dados localizados
    return response


# Atualiza os dados de um regime de bens
@router.put(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um regime de bens",
    response_description="Atualiza um regime de bens",
)
async def update(
    pessoa_id: int,
    t_pessoa_representante_update_schema: TPessoaRepresentanteUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Adiciona o ID do registro ao schema
    t_pessoa_representante_update_schema.pessoa_id = pessoa_id

    # Efetua a atualização dos dados
    response = t_pessoa_representante_controller.update(
        t_pessoa_representante_update_schema
    )

    # Retorna os dados localizados
    return response


# Exclui um determinado regime de bens
@router.delete(
    "/{pessoa_representante_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um regime de bens",
    response_description="Remove um regime de bens",
)
async def delete(
    pessoa_representante_id: int, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos
    t_pessoa_representante_id_schema = TPessoaRepresentanteIdSchema(
        pessoa_representante_id=pessoa_representante_id
    )

    # Efetua a exclusão do regime de bens
    response = t_pessoa_representante_controller.delete(
        t_pessoa_representante_id_schema
    )

    # Retorna os dados localizados
    return response
