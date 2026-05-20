from fastapi import HTTPException, status

from packages.v1.administrativo.actions.p_banco.p_banco_show_action import ShowAction
from packages.v1.administrativo.actions.p_banco.p_banco_update_action import UpdateAction
from packages.v1.administrativo.repositories.p_banco.p_banco_get_by_codigo_repository import (
    GetByCodigoRepository,
)
from packages.v1.administrativo.repositories.p_banco.p_banco_layout_exists_repository import (
    LayoutExistsRepository,
)
from packages.v1.administrativo.schemas.p_banco_schema import (
    PBancoCodigoSchema,
    PBancoIdSchema,
    PBancoLayoutIdSchema,
    PBancoUpdateSchema,
)


class UpdateService:
    @staticmethod
    def _row_value(row, key: str):
        if row is None:
            return None
        lower = key.lower()
        return row.get(lower) or row.get(key) or row.get(key.upper())

    def _ensure_codigo_unique(
        self, codigo_banco: str, banco_id: int
    ):
        duplicate = GetByCodigoRepository().execute(
            PBancoCodigoSchema(codigo_banco=codigo_banco, banco_id=banco_id)
        )
        if duplicate:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=[
                    {
                        "input": "codigo_banco",
                        "message": "Já existe banco cadastrado com este código.",
                    }
                ],
            )

    def _ensure_layout_exists(self, layout_id: int):
        if not LayoutExistsRepository().execute(PBancoLayoutIdSchema(layout_id=layout_id)):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=[
                    {
                        "input": "layout_id",
                        "message": "Layout informado não foi encontrado.",
                    }
                ],
            )

    def execute(self, banco_id: int, banco_schema: PBancoUpdateSchema):
        current = ShowAction().execute(PBancoIdSchema(banco_id=banco_id))
        if not current:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o banco.",
            )

        codigo = (
            banco_schema.codigo_banco
            if banco_schema.codigo_banco is not None
            else self._row_value(current, "codigo_banco")
        )
        if codigo:
            self._ensure_codigo_unique(str(codigo), banco_id)

        layout_id = (
            banco_schema.layout_id
            if banco_schema.layout_id is not None
            else self._row_value(current, "layout_id")
        )
        if layout_id is not None:
            self._ensure_layout_exists(int(layout_id))

        return UpdateAction().execute(banco_id, banco_schema)
