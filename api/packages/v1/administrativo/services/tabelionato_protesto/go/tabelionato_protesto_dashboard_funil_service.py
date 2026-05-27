from packages.v1.administrativo.actions.tabelionato_protesto.tabelionato_protesto_dashboard_funil_action import (
    TabelionatoProtestoDashboardFunilAction,
)


class TabelionatoProtestoDashboardFunilService:
    def execute(self):
        return TabelionatoProtestoDashboardFunilAction().execute()
