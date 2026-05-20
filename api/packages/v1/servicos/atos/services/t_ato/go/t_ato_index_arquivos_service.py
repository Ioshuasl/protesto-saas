from packages.v1.ged.actions.ged_convert import GEDConvert
from packages.v1.servicos.atos.actions.t_ato.t_ato_show_action import (
    TAtoShowAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from fastapi import HTTPException, status


class TAtoIndexrquivosService:
    """
    Servico responsavel por encapsular a logica de negocio para a operacao
    de busca de um registro na tabela T_ATO.
    """

    def execute(self, data: TAtoIdSchema):

        # ----------------------------------------------------
        # Execucao da acao
        # ----------------------------------------------------
        response = TAtoShowAction().execute(data)

        # ----------------------------------------------------
        # Verificacao de resultado
        # ----------------------------------------------------
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        arquivo = GEDConvert().convert(
            serventia=1,
            record_id=response.ato_id,
            pasta="Ato",
            temp_dir=r"./storage/temp/",
            return_type="object",
            output_format="pdf",
        )

        if arquivo is None:
            return None

        # ----------------------------------------------------
        # Retorno da informacao
        # ----------------------------------------------------
        return [arquivo]
