from packages.v1.docx.schemas.docx_table_loop_schema import DOCXTableLoopSchema
from packages.v1.docx.services.docx_table_loop_service import DOCXTableLoopService


class DOCXTableLoopAction:
    @staticmethod
    def execute(data: DOCXTableLoopSchema):
        return DOCXTableLoopService().execute(data)
