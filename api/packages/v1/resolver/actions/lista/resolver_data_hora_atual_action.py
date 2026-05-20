from datetime import datetime, timezone


class ResolverDataHoraAtual:

    @staticmethod
    def execute():

        return datetime.now(timezone.utc).strftime("%d/%m/%Y %H:%M")
