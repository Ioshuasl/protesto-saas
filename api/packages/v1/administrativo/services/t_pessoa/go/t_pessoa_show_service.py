from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_pessoa.t_pessoa_show_action import (
    TPessoaShowAction,
)
from packages.v1.administrativo.schemas.t_pessoa_schema import TPessoaIdSchema
from packages.v1.ged.actions.ged_convert_to_jpg import GEDConvertToJpg


class TPessoaShowService:
    """
    Servico responsavel por encapsular a logica de negocio para a operacao
    de busca de um registro na tabela g_tb_regimebens.
    """

    def execute(self, t_pessoa_id_schema: TPessoaIdSchema):

        t_pessoa_show_action = TPessoaShowAction()
        data = t_pessoa_show_action.execute(t_pessoa_id_schema)

        if not data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar a pessoa desejada",
            )

        # converte para jpg
        data.foto = GEDConvertToJpg().convert(
            serventia=1,
            record_id=data.pessoa_id,
            pasta="Foto",
            temp_dir=r"./storage/temp/",
            return_type="filename",
            page_position="last",
        )

        if getattr(data.foto, "status", None) == 201:
            data.foto = data.foto.data

        if getattr(data.foto, "status", None) == 404:
            data.foto = None

        if getattr(data.foto, "status", None) == 422:
            data.foto = None

        return data
