from fastapi import HTTPException, status

from packages.v1.nfse.actions.nfse_delete_action import NfseDeleteAction
from packages.v1.nfse.actions.nfse_show_action import NfseShowAction
from packages.v1.nfse.schemas.nfse_schema import NfseIdSchema


class NfseDeleteService:
    def execute(self, data: NfseIdSchema):
        show_action = NfseShowAction()
        current_data = show_action.execute(data)
        if not current_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel localizar a NFSE informada.",
            )

        delete_action = NfseDeleteAction()
        deleted = delete_action.execute(data)
        if not deleted:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao foi possivel excluir a NFSE informada.",
            )
        return deleted
