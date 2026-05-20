from packages.v1.administrativo.actions.t_imovel_unidade.t_imovel_unidade_update_action import (
    TImovelUnidadeUpdateAction,
)
from packages.v1.administrativo.schemas.t_imovel_unidade_schema import (
    TImovelUnidadeUpdateSchema,
)


class TImovelUnidadeUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_censec_qualidade.
    """

    def execute(self, t_imovel_unidade_update_schema: TImovelUnidadeUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            t_imovel_unidade_schema (TCensecQualidadeUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        t_imovel_unidade_update_action = TImovelUnidadeUpdateAction()

        # Retorna o resultado da operação
        return t_imovel_unidade_update_action.execute(t_imovel_unidade_update_schema)
