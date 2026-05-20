from fastapi import HTTPException, status

from packages.v1.nfse.actions.nfse_show_action import NfseShowAction
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema


class NfseShowService:
    def execute(self, data: NfseIdSchema):
        action = NfseShowAction()
        response = action.execute(data)
        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar a NFSE informada.",
            )
        return response
