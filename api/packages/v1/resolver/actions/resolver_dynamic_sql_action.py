from packages.v1.resolver.repositories.resolver_dynamic_sql_repository import (
    ResolverDynamicSqlRepository,
)


class ResolverDynamicSqlAction:

    def execute(sefl, data):

        # Classe que busca em qualquer tabela
        dynamic_sql_repository = ResolverDynamicSqlRepository()

        # Montaa e executa os valores
        response = dynamic_sql_repository.execute(data)

        # retorna o valor da operação
        return getattr(response, "valor", None)
