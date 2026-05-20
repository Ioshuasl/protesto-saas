from fastapi import HTTPException, status

from packages.v1.administrativo.actions.t_pessoa.t_pessoa_show_action import (
    TPessoaShowAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaIdSchema,
)
from packages.v1.ged.actions.ged_convert import GEDConvert
from packages.v1.servicos.balcao.actions.t_pessoa_cartao.t_pessoa_cartao_show_ultimo_pedido_action import (
    TPessoaCartaoShoUltimoPedidoAction,
)
from packages.v1.servicos.balcao.schemas.t_pessoa_cartao_schema import (
    TPessoaCartaoIndexchema,
)


class TPessoaFilesIndexService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de listagem de registros na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):

        def _normalize_ged_result(result):
            status = getattr(result, "status", None)

            if status == 201:
                return getattr(result, "data", None)

            if status in (404, 422):
                return None

            return result

        t_pessoa_show_action = TPessoaShowAction()
        data = t_pessoa_show_action.execute(t_pessoa_id_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar a pessoa desejada",
            )

        pessoa_cartao_show_ultimo_action = TPessoaCartaoShoUltimoPedidoAction()
        pessoa_cartao_data = pessoa_cartao_show_ultimo_action.execute(
            TPessoaCartaoIndexchema(pessoa_id=data.pessoa_id)
        )

        converter = GEDConvert()

        ged = []

        ged.append(
            _normalize_ged_result(
                converter.convert(
                    serventia=1,
                    record_id=pessoa_cartao_data.pessoa_id,
                    pasta="Foto",
                    temp_dir=r"./storage/temp/",
                    return_type="object",
                    output_format="pdf",
                )
            )
        )

        ged.append(
            _normalize_ged_result(
                converter.convert(
                    serventia=1,
                    record_id=pessoa_cartao_data.pessoa_cartao_id,
                    pasta="Biometria",
                    temp_dir=r"./storage/temp/",
                    return_type="object",
                    output_format="pdf",
                )
            )
        )

        ged.append(
            _normalize_ged_result(
                converter.convert(
                    serventia=1,
                    record_id=pessoa_cartao_data.pessoa_cartao_id,
                    pasta="Cartao",
                    temp_dir=r"./storage/temp/",
                    return_type="object",
                    output_format="pdf",
                )
            )
        )

        ged.append(
            _normalize_ged_result(
                converter.convert(
                    serventia=1,
                    record_id=pessoa_cartao_data.pessoa_cartao_id,
                    pasta="Documento",
                    temp_dir=r"./storage/temp/",
                    return_type="object",
                    output_format="pdf",
                )
            )
        )

        ged.append(
            _normalize_ged_result(
                converter.convert(
                    serventia=1,
                    record_id=pessoa_cartao_data.pessoa_cartao_id,
                    pasta="Procuracao",
                    temp_dir=r"./storage/temp/",
                    return_type="object",
                    output_format="pdf",
                )
            )
        )

        return ged
