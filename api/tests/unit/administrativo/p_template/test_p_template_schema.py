import pytest
from pydantic import ValidationError

from packages.v1.administrativo.schemas.p_template_schema import (
    PTemplateIndexSchema,
    PTemplateSaveSchema,
    PTemplateUpdateSchema,
)


@pytest.mark.unit
def test_index_schema_accepts_expected_filters():
    schema = PTemplateIndexSchema(template_id="2", descricao="  Certidao  ")

    assert schema.template_id == 2
    assert schema.descricao == "Certidao"


@pytest.mark.unit
def test_index_schema_rejects_unknown_filter():
    with pytest.raises(ValidationError):
        PTemplateIndexSchema(descricao="Certidao", texto="fora do contrato")


@pytest.mark.unit
def test_save_schema_requires_descricao():
    with pytest.raises(ValidationError):
        PTemplateSaveSchema(descricao="   ")


@pytest.mark.unit
def test_save_and_update_schema_do_not_accept_texto_blob():
    with pytest.raises(ValidationError):
        PTemplateSaveSchema(descricao="Certidao", texto="blob")

    with pytest.raises(ValidationError):
        PTemplateUpdateSchema(descricao="Certidao", texto="blob")
