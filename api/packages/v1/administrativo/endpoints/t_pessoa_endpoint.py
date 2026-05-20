# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.query_params_parser import QueryParamsParser
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_pessoa_controller import TPessoaController
from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaCpfSchema,
    TPessoaEmailSchema,
    TPessoaIdSchema,
    TPessoaNameSchema,
    TPessoaSaveFotoSchema,
    TPessoaSaveSchema,
    TPessoaUpdateSchema,
    TPessoaTipoSchema,
)

# Inicializa o roteador para as rotas de pessoa (TPessoa)
router = APIRouter()

# Instânciamento do controller desejado
controller = TPessoaController()


# Lista pessoas filtrando pelo tipo (física, jurídica, etc.)
@router.get(
    "/tipo/{pessoa_tipo}",
    status_code=status.HTTP_200_OK,
    summary="Lista todos as pessoas cadastrados",
    response_description="Lista todos as pessoas cadastrados",
)
async def index(
    pessoa_tipo: str,
    current_user: dict = Depends(dependency=get_current_user),
    query_params=Depends(QueryParamsParser.parse),
):

    # Cria o schema com os dados recebidos
    data = TPessoaTipoSchema(pessoa_tipo=pessoa_tipo, query_params=query_params)

    # Busca todos as pessoas cadastrados
    response = controller.index(data)

    # Retorna os dados localizados
    return response


# Localiza pessoa pelo nome
@router.get(
    "/nome",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em específico pelo nome",
    response_description="Busca um registro em específico",
)
async def get_by_nome(nome: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    data = TPessoaNameSchema(nome=nome)

    # Busca um regime de bens específico pela descrição
    response = controller.get_by_nome(data)

    # Retorna os dados localizados
    return response


# Localiza pessoa pelo e-mail
@router.get(
    "/email",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em específico pelo e-mail",
    response_description="Busca um registro em específico",
)
async def get_by_email(email: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    data = TPessoaEmailSchema(email=email)

    # Busca uma pessoa específica pelo e-mail
    response = controller.get_by_email(data)

    # Retorna os dados localizados
    return response


# Localiza pessoa pelo CPF
@router.get(
    "/cpf",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em específico pelo CPF",
    response_description="Busca um registro em específico",
)
async def get_by_cpf(cpf: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    data = TPessoaCpfSchema(cpf=cpf)

    # Busca uma pessoa específica pelo CPF
    response = controller.get_by_cpf(data)

    # Retorna os dados localizados
    return response


# Localiza dados completos de uma pessoa pelo ID (inclui foto/biometria em JPG para exibição)
@router.get(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em específico pelo ID da pessoa",
    response_description="Busca um registro em específico",
)
async def show(pessoa_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    data = TPessoaIdSchema(pessoa_id=pessoa_id)

    # Busca um regime de bens específico pelo ID
    response = controller.show(data)

    # Retorna os dados localizados
    return response


# Lista arquivos (PDFs) da pessoa (Foto, Biometria, Cartão, Documento, Procuração em PDF)
@router.get(
    "/{pessoa_id}/files",
    status_code=status.HTTP_200_OK,
    summary="Lista arquivos (PDFs) da pessoa",
    response_description="Arquivos da pessoa",
)
async def files_index(
    pessoa_id: int,
    current_user: dict = Depends(dependency=get_current_user),
    query_params=Depends(QueryParamsParser.parse),
):

    # Cria o schema com os dados recebidos
    data = TPessoaIdSchema(pessoa_id=pessoa_id)

    response = controller.files_index(data)

    return response


# Cadastro de pessoa
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra uma pessoa",
    response_description="Pessoa cadastrada com sucesso",
)
async def save(
    t_pessoa_save_schema: TPessoaSaveSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua o cadastro da pessoa no banco de dados
    response = controller.save(t_pessoa_save_schema)

    # Retorna os dados localizados
    return response


# Cadastro/atualização de foto da pessoa
@router.put(
    "/{pessoa_id}/foto/salvar",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra ou atualiza a foto da pessoa",
    response_description="Foto da pessoa cadastrada ou atualizada com sucesso",
)
async def save_foto(
    data: TPessoaSaveFotoSchema,
    current_user: dict = Depends(get_current_user),
):

    # Salva a foto da pessoa no banco de dados
    response = controller.save_foto(data)

    # Retorna os dados localizados
    return response


# Atualiza os dados de uma pessoa
@router.put(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza os dados de uma pessoa",
    response_description="Pessoa atualizada com sucesso",
)
async def update(
    pessoa_id: int,
    data: TPessoaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Adiciona o ID do registro ao schema
    data.pessoa_id = pessoa_id

    # Efetua a atualização dos dados da pessoa
    response = controller.update(data)

    # Retorna os dados localizados
    return response


# Exclui uma pessoa
@router.delete(
    "/{pessoa_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove uma pessoa",
    response_description="Pessoa removida com sucesso",
)
async def delete(pessoa_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    data = TPessoaIdSchema(pessoa_id=pessoa_id)

    # Efetua a exclusão da pessoa
    response = controller.delete(data)

    # Retorna os dados localizados
    return response
