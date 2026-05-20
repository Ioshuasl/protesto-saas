from pathlib import Path
import tempfile
import os
import requests

from fastapi import HTTPException, status

from actions.data.text import Text
from packages.v1.servicos.balcao.actions.t_servico_itempedido.t_servico_itempedido_certidao_save_action import (
    TServicoItemPedidoCertidaSaveAction,
)
from packages.v1.servicos.balcao.schemas.t_servico_itempedido_schema import (
    TServicoItemPedidoCertidaoSaveSchema,
)


class TServicoItemPedidoCertidaoSaveService:
    """
    Serviço responsável por receber o callback do OnlyOffice,
    persistir o documento no banco e ATUALIZAR o arquivo em disco
    de forma segura (atomic write).

    O nome do arquivo em disco é baseado em:
        data.servico_itempedido_id
    """

    def execute(self, data: TServicoItemPedidoCertidaoSaveSchema):
        # 1. Processa apenas STATUS FINAL (save concluído)
        # Status 2 = documento salvo definitivamente no OnlyOffice
        if data.data.get("status") != 2:
            return {"error": 0}
        # 2. Obtém a URL do arquivo final
        file_url = data.data.get("url")
        if not file_url:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="URL do arquivo não informada.",
            )
        # 3. Download do arquivo (binário)
        response = requests.get(file_url, timeout=30)
        response.raise_for_status()

        arquivo_bytes = response.content

        if not arquivo_bytes:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Arquivo retornado está vazio.",
            )
        # 4. Persistência no banco (conteúdo comprimido)
        # Salva o conteúdo final do DOCX no banco
        data.certidao_texto = Text.compress(arquivo_bytes)

        save_action = TServicoItemPedidoCertidaSaveAction()

        if not save_action.execute(data):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao salvar certidão no banco.",
            )
        # 5. Escrita em disco (ATUALIZAÇÃO ATÔMICA)
        # Diretório onde ficam os documentos editáveis
        destino = Path("./storage/temp").resolve()
        destino.mkdir(parents=True, exist_ok=True)

        # Nome FINAL do arquivo baseado no ID do domínio
        # (sempre o mesmo → sobrescreve o existente)
        arquivo_final = destino / f"{data.servico_itempedido_id}.docx"

        # Escrita atômica:
        # 1) grava em arquivo temporário
        # 2) substitui o arquivo final
        with tempfile.NamedTemporaryFile(delete=False, dir=destino) as tmp:
            tmp.write(arquivo_bytes)
            tmp.flush()
            temp_name = tmp.name

        # Substitui o arquivo antigo pelo novo (atomic)
        os.replace(temp_name, arquivo_final)
        # 6. Retorno esperado pelo OnlyOffice
        # error = 0 indica sucesso no callback
        return {"error": 0}
