 # Importação de bibliotecas
from fastapi import APIRouter, Depends, status, Request
from actions.data.get_url_params import get_url_params
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_usuario_controller import (
    GUsuarioController,
)
from packages.v1.administrativo.schemas.g_usuario_schema import (
    GUsuarioAuthenticateSchema,
    GUsuarioIndexSchema,
    GUsuarioSaveSchema,
    GUsuarioUpdateSchema,
    GUsuarioEmailSchema,
    GUsuarioCpfSchema,
    GUsuarioLoginSchema,
    GUsuarioIdSchema,
)

# Inicializa o roteador para as rotas de usuário
router = APIRouter()

# Instânciamento do controller desejado
g_usuario_controller = GUsuarioController()


# Autenticação de usuário
@router.post(
    "/authenticate",
    status_code=status.HTTP_200_OK,
    summary="Cria o token de acesso do usuário",
    response_description="Retorna o token de acesso do usuário",
)
async def authenticate(
    request: Request, g_usuario_authenticate_schema: GUsuarioAuthenticateSchema
):

    # Efetua a autenticação de um usuário junto ao sistema
    response = g_usuario_controller.authenticate(g_usuario_authenticate_schema, request)

    # Retorna os dados localizados
    return response


# Dados do usuário logado
@router.get(
    "/me",
    status_code=status.HTTP_200_OK,
    summary="Retorna os dados do usuário que efetuou o login",
    response_description="Dados do usuário que efetuou o login",
)
async def me(current_user: dict = Depends(get_current_user)):

    # Busca os dados do usuário logado
    response = g_usuario_controller.me(current_user)

    # Retorna os dados localizados
    return response


# Lista todos os usuários
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os usuário cadastrados",
    response_description="Lista todos os usuário cadastrados",
)
async def index(
    current_user: dict = Depends(get_current_user), url_params=Depends(get_url_params)
):

    # Busca todos os usuários cadastrados
    response = g_usuario_controller.index(GUsuarioIndexSchema(**url_params))

    # Retorna os dados localizados
    return response


# Localiza um usuário pelo email
@router.get(
    "/email",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico por e-mail informado",
    response_description="Busca um registro em especifico",
)
async def getEmail(email: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    usuario_schema = GUsuarioEmailSchema(email=email)

    # Busca um usuário especifico pelo e-mail
    response = g_usuario_controller.getEmail(usuario_schema)

    # Retorna os dados localizados
    return response


# Localiza um usuário pelo login
@router.get(
    "/login",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico por login informado",
    response_description="Busca um registro em especifico",
)
async def getLogin(login: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    usuario_schema = GUsuarioLoginSchema(login=login)

    # Busca um usuário especifico pelo e-mail
    response = g_usuario_controller.getLogin(usuario_schema)

    # Retorna os dados localizados
    return response


# Localiza um usuário pelo cpf
@router.get(
    "/cpf",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico por número de CPF",
    response_description="Busca um registro em especifico",
)
async def getCpf(cpf: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    usuario_schema = GUsuarioCpfSchema(cpf=cpf)

    # Busca um usuário especifico pelo e-mail
    response = g_usuario_controller.getCpf(usuario_schema)

    # Retorna os dados localizados
    return response


# Localiza um usuário pelo ID
@router.get(
    "/{usuario_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro em especifico pelo ID do usuário",
    response_description="Busca um registro em especifico",
)
async def show(usuario_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    usuario_schema = GUsuarioIdSchema(usuario_id=usuario_id)

    # Busca um usuário especifico pelo ID
    response = g_usuario_controller.show(usuario_schema)

    # Retorna os dados localizados
    return response


# Cadastro de usuários
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um usuário",
    response_description="Cadastra um usuário",
)
async def save(
    usuario_schema: GUsuarioSaveSchema, current_user: dict = Depends(get_current_user)
):

    # Efetua o cadastro do usuário junto ao banco de dados
    response = g_usuario_controller.save(usuario_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de usuário
@router.put(
    "/{usuario_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um usuário",
    response_description="Atualiza um usuário",
)
async def update(
    usuario_id: int,
    usuario_schema: GUsuarioUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua a atualização dos dados de usuário
    response = g_usuario_controller.update(usuario_id, usuario_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado usuário
@router.delete(
    "/{usuario_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um usuário",
    response_description="Remove um usuário",
)
async def delete(usuario_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    usuario_schema = GUsuarioIdSchema(usuario_id=usuario_id)

    # Efetua a exclusão de um determinado usuário
    response = g_usuario_controller.delete(usuario_schema)

    # Retorna os dados localizados
    return response
