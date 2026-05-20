# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_servico_etiqueta_controller import (
    TServicoEtiquetaController,
)
from packages.v1.administrativo.schemas.t_servico_etiqueta_schema import (
    TServicoEtiquetaSaveSchema,
    TServicoEtiquetaUpdateSchema,
    TServicoEtiquetaIdSchema,
    TServicoEtiquetaServicoTipoIdSchema,
)

# Inicializa o roteador para as rotas de etiqueta de serviço
router = APIRouter()

# Instanciamento do controller desejado
t_servico_etiqueta_controller = TServicoEtiquetaController()


# Lista todos os registros de servico etiqueta
@router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Lista todos os registros de servico etiqueta cadastrados",
    response_description="Lista todos os registros de servico etiqueta cadastrados",
)
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os registros de servico etiqueta cadastrados
    response = t_servico_etiqueta_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um registro de servico etiqueta pelo serviço tipo
@router.get(
    "/servico_tipo/{servico_tipo_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de servico etiqueta em específico pelo ID do serviço ",
    response_description="Busca um registro de servico etiqueta em específico",
)
async def showServicoTipo(
    servico_tipo_id: int, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos
    servico_tipo_schema = TServicoEtiquetaServicoTipoIdSchema(
        servico_tipo_id=servico_tipo_id
    )

    # Busca um registro de servico etiqueta específico pelo ID
    response = t_servico_etiqueta_controller.showServicoTipo(servico_tipo_schema)

    # Retorna os dados localizados
    return response


# Localiza um registro de servico etiqueta pelo ID
@router.get(
    "/{servico_etiqueta_id}",
    status_code=status.HTTP_200_OK,
    summary="Busca um registro de servico etiqueta em específico pelo ID",
    response_description="Busca um registro de servico etiqueta em específico",
)
async def show(
    servico_etiqueta_id: int, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos
    servico_etiqueta_schema = TServicoEtiquetaIdSchema(
        servico_etiqueta_id=servico_etiqueta_id
    )

    # Busca um registro de servico etiqueta específico pelo ID
    response = t_servico_etiqueta_controller.show(servico_etiqueta_schema)

    # Retorna os dados localizados
    return response


# Cadastro de registro de servico etiqueta
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Cadastra um registro de servico etiqueta",
    response_description="Cadastra um registro de servico etiqueta",
)
async def save(
    servico_etiqueta_schema: TServicoEtiquetaSaveSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua o cadastro no banco de dados
    response = t_servico_etiqueta_controller.save(servico_etiqueta_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um registro de servico etiqueta
@router.put(
    "/{servico_etiqueta_id}",
    status_code=status.HTTP_200_OK,
    summary="Atualiza um registro de servico etiqueta",
    response_description="Atualiza um registro de servico etiqueta",
)
async def update(
    servico_etiqueta_id: int,
    servico_etiqueta_schema: TServicoEtiquetaUpdateSchema,
    current_user: dict = Depends(get_current_user),
):

    # Efetua a atualização dos dados
    response = t_servico_etiqueta_controller.update(
        servico_etiqueta_id, servico_etiqueta_schema
    )

    # Retorna os dados localizados
    return response


# Exclui um determinado registro de servico etiqueta
@router.delete(
    "/{servico_etiqueta_id}",
    status_code=status.HTTP_200_OK,
    summary="Remove um registro de servico etiqueta",
    response_description="Remove um registro de servico etiqueta",
)
async def delete(
    servico_etiqueta_id: int, current_user: dict = Depends(get_current_user)
):

    # Cria o schema com os dados recebidos
    servico_etiqueta_schema = TServicoEtiquetaIdSchema(
        servico_etiqueta_id=servico_etiqueta_id
    )

    # Efetua a exclusão do registro de servico etiqueta
    response = t_servico_etiqueta_controller.delete(servico_etiqueta_schema)

    # Retorna os dados localizados
    return response
