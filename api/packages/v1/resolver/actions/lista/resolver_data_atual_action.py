from datetime import datetime, timezone


class ResolverDataAtual:

    @staticmethod
    def execute():

        return datetime.now(timezone.utc).strftime("%d/%m/%Y")
