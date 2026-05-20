from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoUpdateSchema
from packages.v1.administrativo.repositories.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_update_repository import UpdateRepository


class UpdateAction:
    """
        Service responsável por encapsular a lógica de negócio para a atualização
        de um registro na tabela t_tb_reconhecimentotipo.
    """

    def execute(self, tb_reconhecimentotipo_id : int, reconhecimentotipo_schema: TTbReconhecimentotipoUpdateSchema):
        """
        Executa a operação de atualização.

        Args:
        reconhecimentotipo_schema (T_TbReconhecimentotipoUpdateSchema): O esquema com os dados a serem atualizados.

            Returns:
                O resultado da operação de atualização.
            """
        # Instância o repositório de atualização
        update_repository = UpdateRepository()

        # Chama o método de execução do repositório para realizar a atualização
        return update_repository.execute(tb_reconhecimentotipo_id, reconhecimentotipo_schema)
