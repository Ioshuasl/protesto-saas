import pytest
from fastapi import HTTPException
from packages.v1.administrativo.schemas.t_tb_cartorio_schema import TTbCartorioIdSchema, TTbCartorioSaveSchema
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_delete_service import TTbCartorioDeleteService
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_index_service import TTbCartorioIndexService
from packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_save_service import TTbCartorioSaveService
def test_t_tb_cartorio_index_deve_retornar_lista(monkeypatch):
    expected = [{"TB_CARTORIO_ID": 1}]
    def fake_execute(self):
        return expected
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_index_action.TTbCartorioIndexAction.execute",
        fake_execute,
    )
    assert TTbCartorioIndexService().execute() == expected
def test_t_tb_cartorio_index_deve_retornar_lista_vazia(monkeypatch):
    def fake_execute(self):
        return []
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_index_action.TTbCartorioIndexAction.execute",
        fake_execute,
    )
    assert TTbCartorioIndexService().execute() == []
def test_t_tb_cartorio_save_deve_salvar_com_id_existente(monkeypatch):
    payload = TTbCartorioSaveSchema(
        tb_cartorio_id=10,
        descricao="Cartorio A",
        municipio_id=1,
        descricao_municipio="Cidade A",
        cns="1234567890",
    )
    def fake_save(self, data):
        return {"TB_CARTORIO_ID": data.tb_cartorio_id}
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_save_action.TTbCartorioSaveAction.execute",
        fake_save,
    )
    response = TTbCartorioSaveService().execute(payload)
    assert response["TB_CARTORIO_ID"] == 10
def test_t_tb_cartorio_save_deve_propagar_excecao_quando_falhar(monkeypatch):
    payload = TTbCartorioSaveSchema(
        tb_cartorio_id=10,
        descricao="Cartorio A",
        municipio_id=1,
        descricao_municipio="Cidade A",
        cns="1234567890",
    )
    def fake_save(self, data):
        raise Exception("falha")
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_save_action.TTbCartorioSaveAction.execute",
        fake_save,
    )
    with pytest.raises(Exception) as exc:
        TTbCartorioSaveService().execute(payload)
    assert str(exc.value) == "falha"
def test_t_tb_cartorio_delete_deve_remover_quando_existir(monkeypatch):
    def fake_show(self, data):
        return {"TB_CARTORIO_ID": data.tb_cartorio_id}
    def fake_delete(self, data):
        return {"tb_cartorio_id": data.tb_cartorio_id}
    monkeypatch.setattr(
        "packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_show_service.TTbCartorioShowService.execute",
        fake_show,
    )
    monkeypatch.setattr(
        "packages.v1.administrativo.actions.t_tb_cartorio.t_tb_cartorio_delete_action.TTbCartorioDeleteAction.execute",
        fake_delete,
    )
    response = TTbCartorioDeleteService().execute(TTbCartorioIdSchema(tb_cartorio_id=1))
    assert response["tb_cartorio_id"] == 1
def test_t_tb_cartorio_delete_deve_propagar_404_quando_nao_existir(monkeypatch):
    def fake_show(self, data):
        raise HTTPException(status_code=404, detail="nao encontrado")
    monkeypatch.setattr(
        "packages.v1.administrativo.services.t_tb_cartorio.go.t_tb_cartorio_show_service.TTbCartorioShowService.execute",
        fake_show,
    )
    with pytest.raises(HTTPException) as exc:
        TTbCartorioDeleteService().execute(TTbCartorioIdSchema(tb_cartorio_id=1))
    assert exc.value.status_code == 404
