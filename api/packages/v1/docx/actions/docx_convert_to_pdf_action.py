from pathlib import Path

from packages.v1.docx.services.docx_convert_to_pdf_service import (
    DOCXConvertToPDFService,
)


class DOCXConvertToPDFAction:
    @staticmethod
    def execute(
        input_docx_path: str,
        *,
        output: str = "base64",
        save_disk: bool = False,
        output_dir: str | None = None,
        filename_prefix: str | None = None,
        soffice_path: str | None = None,
        convert_timeout_sec: int = 180,
    ):
        input_path = Path(input_docx_path)
        if not input_path.is_absolute():
            input_path = (Path.cwd() / input_path).resolve()

        storage_dir = output_dir or str(input_path.parent)

        return DOCXConvertToPDFService().execute(
            input_content=str(input_path),
            output=output,
            save_disk=save_disk,
            storage_dir=storage_dir,
            filename_prefix=filename_prefix,
            soffice_path=soffice_path,
            convert_timeout_sec=convert_timeout_sec,
        )
