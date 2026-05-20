from fastapi import HTTPException, status
# Adaptação do Schema
from packages.v1.administrativo.schemas.g_emolumento_item_schema import GEmolumentoItemValorSchema
# Importação da Action ajustada para o novo prefixo
from packages.v1.administrativo.actions.g_emolumento_item.g_emolumento_item_valor_action import ValorAction

# O nome da classe deve ser adaptado com o prefixo 'GEmolumentoItem' para manter o padrão
# de classes da aplicação no Controller, Repository, etc.
class ValorService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela G_EMOLUMENTO_ITEM.
    """

    # Mantendo o padrão de nome de método do arquivo original
    def execute(self, emolumento_item_schema: GEmolumentoItemValorSchema):
        """
        Executa a operação de busca de todos os registros de G_EMOLUMENTO_ITEM no banco de dados.

        Returns:
            A lista de registros encontrados.
        """
        # Instanciamento da ação (com o prefixo adaptado)
        valor_action = ValorAction()

        # Executa a busca de todas as ações (adaptando o nome do parâmetro)
        data = valor_action.execute(emolumento_item_schema)

        # Verifica se foram localizados registros
        if not data:
            # Retorna uma exceção (adaptando a mensagem)
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar os registros de G_EMOLUMENTO_ITEM'
            )
        
        # Retorna as informações localizadas
        return data