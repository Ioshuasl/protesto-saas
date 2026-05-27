from abstracts.action import BaseAction
from packages.v1.administrativo.repositories.tabelionato_protesto.tabelionato_protesto_dashboard_funil_repository import (
    TabelionatoProtestoDashboardFunilRepository,
)


class TabelionatoProtestoDashboardFunilAction(BaseAction):
    def execute(self):
        return TabelionatoProtestoDashboardFunilRepository().execute()
