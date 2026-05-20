from docx.enum.section import WD_ORIENTATION
from docx.shared import Mm

from packages.v1.ged.schemas.ged_schema import GEDDocxPageSetupSchema


class GEDDocxPageSetupAction:
    @staticmethod
    def execute(section, data: GEDDocxPageSetupSchema) -> None:
        orientation = (data.orientation or "").strip().lower()
        if orientation == "portrait":
            section.orientation = WD_ORIENTATION.PORTRAIT
        elif orientation == "landscape":
            section.orientation = WD_ORIENTATION.LANDSCAPE
        else:
            raise ValueError(f"Orientacao de pagina invalida: {data.orientation}")

        section.page_width = Mm(data.page_width_mm)
        section.page_height = Mm(data.page_height_mm)
        section.top_margin = Mm(data.top_margin_mm)
        section.bottom_margin = Mm(data.bottom_margin_mm)
        section.left_margin = Mm(data.left_margin_mm)
        section.right_margin = Mm(data.right_margin_mm)
