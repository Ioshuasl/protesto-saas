from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_minuta.t_minuta_show_texto_action import TMinutaShowTextoAction
from packages.v1.administrativo.schemas.t_minuta_schema import TMinutaIdSchema
from packages.v1.administrativo.actions.t_minuta.t_minuta_show_action import ShowAction
from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema

class TMinutaShowTextoService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de busca de um registro na tabela t_minuta.
    """

    def execute(self, data: TMinutaIdSchema):
        """
        Executa a operação de busca no banco de dados.

        Args:
            minuta_schema (TMinutaIdSchema): O esquema com o ID a ser buscado.

        Returns:
            O resultado da busca.
        """

        # Executa a ação em questão
        data = TMinutaShowTextoAction().execute(data)

        if not data:
            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail='Não foi possível localizar o registro de MINUTA'
            )

        # Caso não exista conteúdo, evita erro no DOCXProcess
        content = data.texto if data.texto else b""

        # Cria o arquivo em disco
        data.texto = DOCXProcess().execute(
                DOCXProcessSchema(
                    id=str(data.minuta_id),
                    content=data.texto,
                    save_disk=True,
                )
            )

        # Retorno da informação
        return data