from fastapi import HTTPException, status
from packages.v1.administrativo.schemas.t_pessoa_schema import (
    TPessoaSaveFotoSchema,
)
from packages.v1.ged.actions.ged_convert_to_jpg import GEDConvertToJpg
from packages.v1.ged.actions.ged_save_action import GEDSaveAction
from packages.v1.ged.schemas.ged_schema import GEDSaveSchema


class TPessoaSaveFotoService:

    def execute(self, data: TPessoaSaveFotoSchema):

        # Cria a imagem em disco
        response_ged_save = GEDSaveAction().execute(
            GEDSaveSchema(
                base64=data.foto,
                pasta="Foto",
                registro_id=str(data.pessoa_id),
                serventia=1,
            )
        )

        # Verifica se existe a resposta válida
        if not response_ged_save:

            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Não foi possivel criar a imagem",
            )

        # converte para jpg
        response_ged_convert = GEDConvertToJpg().convert(
            serventia=1,
            record_id=data.pessoa_id,
            pasta="Foto",
            temp_dir=r"./storage/temp/",
            return_type="filename",
            page_position="last",
        )

        if not response_ged_convert:

            # Retorna uma exceção
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Não foi possivel criar a imagem",
            )

        return response_ged_convert
