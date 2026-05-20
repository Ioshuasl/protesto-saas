from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.t_imovel.t_imovel_delete_repository import (
    TImovelDeleteRepository,
)
from packages.v1.administrativo.schemas.t_imovel_schema import TImovelIdSchema


class TImovelDeleteAction(BaseAction):
    
    def execute(self, t_imovel_id_schema: TImovelIdSchema):
        
        # Instanciamento do repositório
        t_imovel_delete_repository = TImovelDeleteRepository()

        # Execução do repositório
        response = t_imovel_delete_repository.execute(t_imovel_id_schema)

        return response
