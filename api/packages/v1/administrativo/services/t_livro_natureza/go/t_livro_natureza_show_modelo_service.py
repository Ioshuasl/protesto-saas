from fastapi import HTTPException, status
from packages.v1.administrativo.actions.t_livro_natureza.t_livro_natureza_show_modelo_action import TLivroNaturezaShowModeloAction
from packages.v1.administrativo.schemas.t_livro_natureza_schema import TLivroNaturezaShowModeloSchema
from packages.v1.docx.services.docx_process_service import DOCXProcess, DOCXProcessSchema

class TLivroNaturezaShowModeloService:

    """Servico para buscar um registro de T_LIVRO_NATUREZA."""

    def execute(self, schema: TLivroNaturezaShowModeloSchema):

        match schema.modelo:
            case 1:
                schema.coluna = "MODELO_LIVRO"
            case 2:
                schema.coluna = "MODELO_TRASLADO"
            case 3:
                schema.coluna = "MODELO_LIVRO_PDF"
            case 4:
                schema.coluna = "MODELO_TRASLADO_PDF"
            case _:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Modelo inexistente",
                )

        response = TLivroNaturezaShowModeloAction().execute(schema)

        if not response:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Não foi possível localizar o registro de T_LIVRO_NATUREZA.",
            )

        # Caso não exista conteúdo, evita erro no DOCXProcess
        response.modelo_texto = response.modelo_texto if response.modelo_texto else b""

        response.modelo_texto = DOCXProcess().execute(
            DOCXProcessSchema(
                id=str(response.livro_natureza_id),
                content=response.modelo_texto,
                save_disk=True,
            )
        )

        return response
