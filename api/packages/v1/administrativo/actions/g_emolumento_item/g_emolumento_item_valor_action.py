from abstracts.action import BaseAction
# O Schema precisa ser adaptado para GEmolumentoItem, talvez recebendo um ID de Emolumento
# ou um ID do próprio Item, dependendo da necessidade de listagem.
# Vamos sugerir um Schema específico para a listagem (Index) que pode receber um Emolumento ID
# para listar todos os seus itens, mantendo o padrão do arquivo original que usava um 'SistemaIdSchema'.
# Para simplificar, vamos assumir um schema de filtro ou um schema base para Index.
# Sugerimos a criação de:
# from packages.v1.administrativo.schemas.g_emolumento_item_schema import GEmolumentoItemIndexSchema 
# (ou GEmolumentoItemEmolumentoIdSchema se for o padrão da aplicação)
from packages.v1.administrativo.schemas.g_emolumento_item_schema import GEmolumentoItemValorSchema 

# O repositório ValorRepository deve ser substituído pelo GEmolumentoItemValorRepository.
from packages.v1.administrativo.repositories.g_emolumento_item.g_emolumento_item_valor_repository import ValorRepository

class ValorAction(BaseAction):
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de todos os registros na tabela G_EMOLUMENTO_ITEM,
    utilizando a DDL fornecida.
    """

    # Mantendo o padrão de nome de método do arquivo original
    def execute(self, emolumento_item_schema: GEmolumentoItemValorSchema):
        """
        Executa a operação de listagem de G_EMOLUMENTO_ITEM no banco de dados.

        Args:
            emolumento_item_schema: Esquema com parâmetros de filtro/listagem
                                    (por exemplo, ID do Emolumento pai, se a listagem for
                                    filtrada por ele, ou parâmetros de paginação).

        Returns:
            A lista de todos os registros de G_EMOLUMENTO_ITEM que satisfazem o filtro.
        """
        # Instanciamento do repositório
        # O nome do repositório foi adaptado com o prefixo 'GEmolumentoItem'
        index_repository = ValorRepository()

        # Execução do repositório
        # O nome do parâmetro foi adaptado para 'emolumento_item_schema'
        response = index_repository.execute(emolumento_item_schema)

        # Retorno da informação
        return response