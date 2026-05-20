from pathlib import Path

from fastapi import HTTPException, status
from packages.v1.resolver.schemas.resolver_schema import ResolverSchema
from packages.v1.resolver.services.resolver_gramatica_main_service import (
    ResolverGramaticaMainService,
)
from packages.v1.resolver.services.resolver_main_service import ResolverMainService
from packages.v1.servicos.atos.actions.t_ato.t_ato_get_texto_corpo_action import (
    TAtoGetTextoCorpoAction,
)
from packages.v1.servicos.atos.schemas.t_ato_schema import TAtoIdSchema
from packages.v1.servicos.atos.services.t_ato.go.t_ato_build_gramatica_context_service import (
    TAtoBuildGramaticaContextService,
)


class TAtoGetTextoCorpoService:
    """
    ServiÃ§o responsÃ¡vel por encapsular a lÃ³gica de negÃ³cio para a operaÃ§Ã£o
    de busca de um registro na tabela T_ATO.
    """

    def execute(self, data: TAtoIdSchema):
        """
        Executa a operaÃ§Ã£o de busca no banco de dados.

        Args:
            data (TAtoIdSchema):
                O esquema com o ID do registro a ser buscado.

        Returns:
            O resultado da busca.
        """
        response = TAtoGetTextoCorpoAction().execute(data)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Nao encontramos o ato informado. Verifique o codigo e tente novamente.",
            )

        response.texto = ResolverMainService().execute(
            ResolverSchema(
                id=response.ato_id,
                campo_id_valor=response.ato_id,
                sitema_id=2,
                texto=response.texto,
            )
        )

        texto_resolvido_path = Path("./storage/temp") / str(response.texto)
        if texto_resolvido_path.exists():
            response.texto = ResolverGramaticaMainService().execute(
                ResolverSchema(
                    id=response.ato_id,
                    campo_id_valor=response.ato_id,
                    sitema_id=2,
                    texto=texto_resolvido_path.read_bytes(),
                    gramatica=TAtoBuildGramaticaContextService().execute(
                        response.ato_id
                    ),
                )
            )

        return response
