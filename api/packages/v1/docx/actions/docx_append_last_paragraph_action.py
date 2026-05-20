from packages.v1.docx.services.docx_append_last_paragraph_service import (
    DOCXAppendLastParagraphService,
)


class DOCXAppendLastParagraphAction:
    @staticmethod
    def execute(
        input_content,
        append_text,
        *,
        output: str = "binary",
        save_disk: bool = False,
        storage_dir: str = "./storage/temp",
        filename_prefix: str | None = None,
        prepend_space: bool = True,
    ):
        return DOCXAppendLastParagraphService().execute(
            input_content=input_content,
            append_text=append_text,
            output=output,
            save_disk=save_disk,
            storage_dir=storage_dir,
            filename_prefix=filename_prefix,
            prepend_space=prepend_space,
        )
