from fastapi import HTTPException, status

from abstracts.repository import BaseRepository
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema


class NfseDeleteRepository(BaseRepository):
    def execute(self, data: NfseIdSchema):
        try:
            sql = """
                DELETE FROM NFSE
                WHERE ID_NFSE = :id_nfse
                RETURNING ID_NFSE
            """
            return self.run_and_return(sql, {"id_nfse": data.id_nfse})
        except Exception as exc:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao excluir NFSE: {exc}",
            )
