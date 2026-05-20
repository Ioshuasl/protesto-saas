# Importação de bibliotecas
from fastapi import APIRouter, Depends, status
from actions.jwt.get_current_user import get_current_user
from packages.v1.administrativo.controllers.t_tb_andamentoservico_controller import TTbAndamentoservicoController
from packages.v1.administrativo.schemas.t_tb_andamentoservico_schema import (
    TTbAndamentoservicoSchema,
    TTbAndamentoservicoSaveSchema,
    TTbAndamentoservicoUpdateSchema,
    TTbAndamentoservicoIdSchema
)

# Inicializa o roteador para as rotas de andamento de serviço
router = APIRouter()

# Instânciamento do controller desejado
t_tb_andamentoservico_controller = TTbAndamentoservicoController()

# Lista todos os andamentos de serviço
@router.get('/',
            status_code=status.HTTP_200_OK,
            summary='Lista todos os andamentos de serviço cadastrados',
            response_description='Lista todos os andamentos de serviço cadastrados')
async def index(current_user: dict = Depends(get_current_user)):

    # Busca todos os andamentos de serviço cadastrados
    response = t_tb_andamentoservico_controller.index()

    # Retorna os dados localizados
    return response


# Localiza um andamento de serviço pela descrição
@router.get('/descricao',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em específico pela descrição',
            response_description='Busca um registro em específico')
async def get_by_descricao(descricao : str, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    andamentoservico_schema = TTbAndamentoservicoSchema(descricao=descricao)

    # Busca um andamento de serviço específico pela descrição
    response = t_tb_andamentoservico_controller.get_by_descricao(andamentoservico_schema)

    # Retorna os dados localizados
    return response


# Localiza um andamento de serviço pelo ID
@router.get('/{tb_andamentoservico_id}',
            status_code=status.HTTP_200_OK,
            summary='Busca um registro em específico pelo ID do andamento de serviço',
            response_description='Busca um registro em específico')
async def show(tb_andamentoservico_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    andamentoservico_schema = TTbAndamentoservicoIdSchema(tb_andamentoservico_id=tb_andamentoservico_id)

    # Busca um andamento de serviço específico pelo ID
    response = t_tb_andamentoservico_controller.show(andamentoservico_schema)

    # Retorna os dados localizados
    return response


# Cadastro de andamento de serviço
@router.post('/',
            status_code=status.HTTP_201_CREATED,
            summary='Cadastra um andamento de serviço',
            response_description='Cadastra um andamento de serviço')
async def save(andamentoservico_schema : TTbAndamentoservicoSaveSchema, current_user: dict = Depends(get_current_user)):

    # Efetua o cadastro no banco de dados
    response = t_tb_andamentoservico_controller.save(andamentoservico_schema)

    # Retorna os dados localizados
    return response


# Atualiza os dados de um andamento de serviço
@router.put('/{tb_andamentoservico_id}',
            status_code=status.HTTP_200_OK,
            summary='Atualiza um andamento de serviço',
            response_description='Atualiza um andamento de serviço')
async def update(tb_andamentoservico_id : int, andamentoservico_schema : TTbAndamentoservicoUpdateSchema, current_user: dict = Depends(get_current_user)):

    # Efetua a atualização dos dados
    response = t_tb_andamentoservico_controller.update(tb_andamentoservico_id, andamentoservico_schema)

    # Retorna os dados localizados
    return response

# Exclui um determinado andamento de serviço
@router.delete('/{tb_andamentoservico_id}',
            status_code=status.HTTP_200_OK,
            summary='Remove um andamento de serviço',
            response_description='Remove um andamento de serviço')
async def delete(tb_andamentoservico_id : int, current_user: dict = Depends(get_current_user)):

    # Cria o schema com os dados recebidos
    andamentoservico_schema = TTbAndamentoservicoIdSchema(tb_andamentoservico_id=tb_andamentoservico_id)

    # Efetua a exclusão do andamento de serviço
    response = t_tb_andamentoservico_controller.delete(andamentoservico_schema)

    # Retorna os dados localizados
    return response