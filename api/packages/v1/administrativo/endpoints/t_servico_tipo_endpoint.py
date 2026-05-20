# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.data.get_url_params import get_url_params
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_servico_tipo_controller import (
    TServicoTipoController,
)
from packages.v1.administrativo.schemas.t_servico_tipo_schema import (
    TServicoTipoIndexSchema,
    TServicoTipoSchema,
    TServicoTipoSaveSchema,
    TServicoTipoUpdateSchema,
    TServicoTipoIdSchema,
)

# Inicializa o roteador para as rotas do tipo de serviço
router = APIRouter()

# Instanciamento do controller desejado
t_servico_tipo_controller = TServicoTipoController()


# Lista todos os registros de servico tipo
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de servico tipo cadastrados",
    response_description="Lista todos os registros de servico tipo cadastrados",
)
async def index(
    current_user: dict = Depends(get_current_user), url_params=Depends(get_url_params)
):

    # Busca todos os registros de servico tipo cadastrados
    response = t_servico_tipo_controller.index(TServicoTipoIndexSchema(**url_params))

    # Retorna os dados localizados
    return response


# Localiza um registro de servico tipo pela descrição
@router.get(
    "/descricao",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de servico tipo em específico pela descrição",
    response_description="Busca um registro de servico tipo em específico",
)
async def get_by_descricao(
    descricao: str, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos. Nota: Assumindo que TServicoTipoSchema pode ser usado para descrição na rota get.
    servico_tipo_schema = TServicoTipoSchema(descricao=descricao)

    # Busca um registro de servico tipo específico pela descrição
    response = t_servico_tipo_controller.get_by_descricao(servico_tipo_schema)

    # Retorna os dados localizados
    return response


@router.get(
    "/top-servicos-tipo",
    status_code=status.HTTP_200_OK,
    summary="Lista os 4 servicos tipo mais utilizados",
    response_description="Lista os 4 servicos tipo mais utilizados",
)
async def top_servicos_tipo(current_user: dict = Depends(get_current_user)):

    response = t_servico_tipo_controller.top_servicos_tipo()
    return response


# Localiza um registro de servico tipo pelo ID
@router.get(
    "/{servico_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de servico tipo em específico pelo ID",
    response_description="Busca um registro de servico tipo em específico",
)
async def show(servico_tipo_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    servico_tipo_schema = TServicoTipoIdSchema(servico_tipo_id=servico_tipo_id)

    # Busca um registro de servico tipo específico pelo ID
    response = t_servico_tipo_controller.show(servico_tipo_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de servico tipo
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um registro de servico tipo",
    response_description="Cadastra um registro de servico tipo",
)
async def save(
    servico_tipo_schema: TServicoTipoSaveSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua o cadastro no banco de dados
    response = t_servico_tipo_controller.save(servico_tipo_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de servico tipo
@router.put(
    "/{servico_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de servico tipo",
    response_description="Atualiza um registro de servico tipo",
)
async def update(
    servico_tipo_id: int,
    servico_tipo_schema: TServicoTipoUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua a atualização dos dados
    response = t_servico_tipo_controller.update(servico_tipo_id, servico_tipo_schema)

    # Retorna os dados localizados
    return response


# Exclui um determinado registro de servico tipo
@router.delete(
    "/{servico_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de servico tipo",
    response_description="Remove um registro de servico tipo",
)
async def delete(servico_tipo_id: int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    servico_tipo_schema = TServicoTipoIdSchema(servico_tipo_id=servico_tipo_id)

    # Efetua a exclusão do registro de servico tipo
    response = t_servico_tipo_controller.delete(servico_tipo_schema)

    # Retorna os dados localizados
    return response
