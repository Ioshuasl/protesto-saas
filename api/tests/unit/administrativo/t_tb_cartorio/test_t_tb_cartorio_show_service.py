import pytest
from fastapi import HTTPException
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_show_service import TTbCartorioShowService
def test_t_tb_cartorio_show_deve_retornar_registro_quando_existir(monkeypatch):
    expected = {"TB_CARTORIO_ID": 1}
    def fake_execute(self, data):
        return expected
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_show_action.TTbCartorioShowAction.execute",
        fake_execute,
    )
    response = TTbCartorioShowService().execute(TTbCartorioIdSchema(tb_cartorio_id=1))
    assert response == expected
def test_t_tb_cartorio_show_deve_retornar_404_quando_nao_existir(monkeypatch):
    def fake_execute(self, data):
        return None
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_show_action.TTbCartorioShowAction.execute",
        fake_execute,
    )
    with pytest.raises(HTTPException) as exc:
        TTbCartorioShowService().execute(TTbCartorioIdSchema(tb_cartorio_id=999))
    assert exc.value.status_code == 404
