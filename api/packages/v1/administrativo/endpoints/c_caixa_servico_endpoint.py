# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.c_caixa_servico_controller import CCaixaServicoController
from packages.v1.administrativo.schemas.c_caixa_servico_schema import (
    CCaixaServicoSchema,
    CCaixaServicoSaveSchema,
    CCaixaServicoUpdateSchema,
    CCaixaServicoDescricaoSchema,
    CCaixaServicoSistemaIdSchema
)

# Inicializa o roteador para as rotas de usuário
router = APIRouter()

# Instânciamento do controller desejado
c_caixa_servico_controller = CCaixaServicoController()
  
# Lista todos os serviços
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os serviços cadastrados',
            response_description='Lista todos os serviços cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os usuários cadastrados
    response = c_caixa_servico_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um caixa serviço pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em especifico pela descrição',
            response_description='Busca um registro em especifico')
async def getDescricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    caixa_servico_schema = CCaixaServicoDescricaoSchema(descricao=descricao)

    # Busca um usuário especifico pelo e-mail
    response = c_caixa_servico_controller.getDescricao(caixa_servico_schema)

    # Retorna os dados localizados
    return response


# Localiza um caixa serviço pelo sistema_id
@router.get('/sistema/{sistema_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca registros pelo sistema_id',
            response_description='Busca registros pelo sistema_id')
async def getSistemaId(sistema_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    caixa_servico_schema = CCaixaServicoSistemaIdSchema(sistema_id=sistema_id)

    # Busca um usuário especifico pelo e-mail
    response = c_caixa_servico_controller.getSistemaId(caixa_servico_schema)

    # Retorna os dados localizados
    return response


# Localiza um serviço pelo ID
@router.get('/{caixa_servico_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em especifico pelo ID do serviço',
            response_description='Busca um registro em especifico')
async def show(caixa_servico_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    caixa_servico_schema = CCaixaServicoSchema(caixa_servico_id=caixa_servico_id)

    # Busca um usuário especifico pelo ID
    response = c_caixa_servico_controller.show(caixa_servico_schema)

    # Retorna os dados localizados
    return response


# Cadastro de caixa servico
@router.post('/',
            status_code=status.HTTP_200_OK,
            summary='Cadastra um caixa serviço',
            response_description='Cadastra um serviço')
async def save(caixa_servico_schema : CCaixaServicoSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro do usuário junto ao banco de dados
    response = c_caixa_servico_controller.save(caixa_servico_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de caixa serviço
@router.put('/{caixa_servico_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um caixa serviço',
            response_description='Atualiza um serviço')
async def update(caixa_servico_id : int, caixa_servico_schema : CCaixaServicoUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados de usuário
    response = c_caixa_servico_controller.update(caixa_servico_id, caixa_servico_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado usuário 
@router.delete('/{caixa_servico_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um caixa serviço',
            response_description='Remove um serviço')
async def delete(caixa_servico_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    caixa_servico_schema = CCaixaServicoSchema(caixa_servico_id=caixa_servico_id)

    # Efetua a exclusão de um determinado usuário
    response = c_caixa_servico_controller.delete(caixa_servico_schema)

    # Retorna os dados localizados
    return response