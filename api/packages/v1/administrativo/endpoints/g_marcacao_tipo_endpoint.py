# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.g_marcacao_tipo_controller import (
    GMarcacaoTipoController,
)
from packages.v1.administrativo.schemas.g_marcacao_tipo_schema import (
    GMarcacaoTipoNomeSchema,
    GMarcacaoTipoSchema,
    GMarcacaoTipoSaveSchema,
    GMarcacaoTipoUpdateSchema,
    GMarcacaoTipoIdSchema,
    GMarcacaoTipoGrupoSchema,
)

# Inicializa o roteador para as rotas do tipo de marcação
router = APIRouter()

# Instanciamento do controller desejado
controller = GMarcacaoTipoController()


# Lista todos os registros de marcação tipo
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de marcação tipo cadastrados",
    response_description="Lista todos os registros de marcação tipo cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de marcação tipo cadastrados
    response = controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de marcação tipo pela descrição
@router.get(
    "/descricao",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de marcação tipo em específico pela descrição",
    response_description="Busca um registro de marcação tipo em específico",
)
async def get_by_descricao(
    descricao: str, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos. Nota: Assumindo que GMarcacaoTipoSchema pode ser usado para descrição.
    marcacao_tipo_schema = GMarcacaoTipoSchema(descricao=descricao)

    # Busca um registro de marcação tipo específico pela descrição
    response = controller.get_by_descricao(marcacao_tipo_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de marcação tipo pela descrição
@router.get(
    "/nome/{nome}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de marcação tipo em específico pela descrição",
    response_description="Busca um registro de marcação tipo em específico",
)
async def get_by_Nome(nome: str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos. Nota: Assumindo que GMarcacaoTipoSchema pode ser usado para descrição.
    data = GMarcacaoTipoNomeSchema(nome=nome)

    # Busca um registro de marcação tipo específico pela descrição
    response = controller.get_by_nome(data)

    # Retorna os dados localizados
    return response


# Localiza um registro de marcação tipo passando os filtros de consulta
@router.get(
    "/grupo",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de marcação tipo em específico pela descrição",
    response_description="Busca um registro de marcação tipo em específico",
)
async def get_by_grupo(
    grupo: str,
    sistema_id: int,
    situacao: str,
    current_user: dict = Depends(get_current_user),
):

    # Cria o schema com os dados recebidos. Nota: Assumindo que GMarcacaoTipoSchema pode ser usado para descrição.
    marcacao_tipo_schema = GMarcacaoTipoGrupoSchema(
        grupo=grupo, sistema_id=sistema_id, situacao=situacao
    )

    # Busca um registro de marcação tipo específico pela descrição
    response = controller.get_by_grupo(marcacao_tipo_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de marcação tipo pelo ID
@router.get(
    "/{marcacao_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de marcação tipo em específico pelo ID",
    response_description="Busca um registro de marcação tipo em específico",
)
async def show(marcacao_tipo_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    marcacao_tipo_schema = GMarcacaoTipoIdSchema(marcacao_tipo_id=marcacao_tipo_id)

    # Busca um registro de marcação tipo específico pelo ID
    response = controller.show(marcacao_tipo_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de marcação tipo
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um registro de marcação tipo",
    response_description="Cadastra um registro de marcação tipo",
)
async def save(
    marcacao_tipo_schema: GMarcacaoTipoSaveSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua o cadastro no banco de dados
    response = controller.save(marcacao_tipo_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de marcação tipo
@router.put(
    "/{marcacao_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de marcação tipo",
    response_description="Atualiza um registro de marcação tipo",
)
async def update(
    marcacao_tipo_id: int,
    marcacao_tipo_schema: GMarcacaoTipoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    marcacao_tipo_schema.marcacao_tipo_id = marcacao_tipo_id

    # Efetua a atualização dos dados
    response = controller.update(marcacao_tipo_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado registro de marcação tipo
@router.delete(
    "/{marcacao_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de marcação tipo",
    response_description="Remove um registro de marcação tipo",
)
async def delete(marcacao_tipo_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    marcacao_tipo_schema = GMarcacaoTipoIdSchema(marcacao_tipo_id=marcacao_tipo_id)

    # Efetua a exclusão do registro de marcação tipo
    response = controller.delete(marcacao_tipo_schema)

    # Retorna os dados localizados
    return response
