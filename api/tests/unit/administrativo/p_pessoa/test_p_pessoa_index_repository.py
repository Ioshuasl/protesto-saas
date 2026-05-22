import pytest

from packages.v1.administrativo.repositories.p_pessoa.p_pessoa_index_repository import (
    _varchar15_like_prefix,
)


@pytest.mark.unit
def test_varchar15_like_prefix_cnpj_14_digitos():
    assert _varchar15_like_prefix("07158428000106") == "07158428000106%"


@pytest.mark.unit
def test_varchar15_like_prefix_nao_usa_curinga_inicial():
    pattern = _varchar15_like_prefix("07158428000106")
    assert not pattern.startswith("%")
    assert len(pattern) <= 15


@pytest.mark.unit
def test_varchar15_like_prefix_remove_mascara():
    assert _varchar15_like_prefix("07.158.428/0001-06") == "07158428000106%"


@pytest.mark.unit
@pytest.mark.integration
def test_busca_unificada_cnpj_sem_erro_varchar15():
    from actions.data.query_params_parser import Pagination, QueryParams, Sort
    from packages.v1.administrativo.actions.p_pessoa.p_pessoa_index_action import (
        IndexAction,
    )
    from packages.v1.administrativo.schemas.p_pessoa_schema import PPessoaIndexSchema

    qp = QueryParams(
        pagination=Pagination(page=1, per_page=10),
        sort=Sort(field="pessoa_id", direction="desc"),
        filters=[],
    )
    result = IndexAction().execute(
        PPessoaIndexSchema(busca="07158428000106"),
        qp,
    )
    assert result["pagination"]["total"] >= 0
    assert isinstance(result["rows"], list)
