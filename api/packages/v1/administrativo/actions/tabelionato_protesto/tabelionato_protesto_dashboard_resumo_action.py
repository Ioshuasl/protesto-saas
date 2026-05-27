from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.tabelionato_protesto.tabelionato_protesto_dashboard_resumo_repository import (
    TabelionatoProtestoDashboardResumoRepository,
)


class TabelionatoProtestoDashboardResumoAction(BaseAction):
    def execute(self):
        return TabelionatoProtestoDashboardResumoRepository().execute()
