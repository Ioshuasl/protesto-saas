from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoUpdateSchema
from packages.v1.administrativo.actions.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_update_action import UpdateAction

class TTbReconhecimentotipoUpdateService:
    """
    Serviço para a operação de atualização de um registro na tabela
    t_tb_reconhecimentotipo.
    """
    def execute(self, tb_reconhecimentotipo_id : int, reconhecimentotipo_schema: TTbReconhecimentotipoUpdateSchema):
        """
        Executa a operação de atualização no banco de dados.

        Args:
            reconhecimentotipo_schema (T_TbReconhecimentotipoUpdateSchema): O esquema com os dados a serem atualizados.

        Returns:
            O resultado da operação de atualização.
        """
        # Instanciamento de ações
        update_action = UpdateAction()

        # Retorna o resultado da operação
        return update_action.execute(tb_reconhecimentotipo_id, reconhecimentotipo_schema)
