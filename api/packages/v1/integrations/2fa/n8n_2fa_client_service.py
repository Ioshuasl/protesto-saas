from fastapi import HTTPException, status
import logging
import os
from urllib.parse import urljoin

import requests

from actions.security.security import Security

# Logger da integração com n8n (usado para rastreio de falhas externas).
logger = logging.getLogger(__name__)


class N8NTwoFactorClientService:
    @staticmethod
    def _get_base_url() -> str:
        return (os.getenv("ORIUS_2FA_BASE_URL") or "").strip()

    @staticmethod
    def _build_url(env_key: str, default_path: str) -> str:
        direct_url = (os.getenv(env_key) or "").strip()
        if direct_url:
            return direct_url

        base_url = N8NTwoFactorClientService._get_base_url()
        if not base_url:
            return ""

        base_url = base_url if base_url.endswith("/") else f"{base_url}/"
        return urljoin(base_url, default_path)

    @staticmethod
    def _post_json(url: str, payload: dict) -> requests.Response:
        # Timeout configurável para a chamada HTTP (fallback de 20s).
        try:
            timeout = float(os.getenv("ORIUS_2FA_TIMEOUT_SECONDS", "20"))
        except ValueError:
            timeout = 20.0

        # Monta headers de autenticação (Authorization explícito tem prioridade).
        headers = {}
        auth_value = (os.getenv("ORIUS_2FA_AUTHORIZATION") or "").strip()
        if auth_value:
            headers["Authorization"] = auth_value
        else:
            # Fallback para Basic Auth calculado a partir das variáveis de ambiente.
            basic_auth_header = Security.get_basic_auth_header()
            if basic_auth_header:
                headers["Authorization"] = basic_auth_header

        # Permite desabilitar validação SSL em ambientes locais/controlados.
        verify_ssl = (
            os.getenv("ORIUS_2FA_VERIFY_SSL", "true").strip().lower()
            not in ("0", "false", "no")
        )

        # Chamada ao webhook com tratamento de falhas de rede e timeout.
        try:
            response = requests.post(
                url,
                json=payload,
                headers=headers or None,
                timeout=timeout,
                verify=verify_ssl,
            )
            return response
        except requests.Timeout:
            logger.warning("Timeout ao solicitar serviço de 2FA")
            raise HTTPException(
                status_code=status.HTTP_504_GATEWAY_TIMEOUT,
                detail="Tempo esgotado ao consultar serviço de 2FA",
            ) from None
        except requests.RequestException as exc:
            logger.warning("Falha de rede ao solicitar serviço de 2FA: %s", exc)
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Falha de comunicação ao consultar serviço de 2FA",
            ) from None

    @staticmethod
    def _parse_response_json(response: requests.Response) -> dict:
        # Regras de mapeamento de status HTTP da integração externa.
        if response.status_code == 401:
            logger.warning("Webhook 2FA retornou 401 (credencial ausente ou inválida)")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=(
                    "O webhook de 2FA recusou a requisição (401). "
                    "Confira usuário/senha do Basic Auth no n8n e no .env "
                    "(ORIUS_2FA_BASIC_USER / ORIUS_2FA_BASIC_PASSWORD ou ORIUS_2FA_AUTHORIZATION)."
                ),
            )
        if response.status_code == 403:
            logger.warning("Webhook 2FA retornou 403")
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="O webhook de 2FA recusou a requisição (403). Verifique permissões do endpoint.",
            )
        if response.status_code != 200:
            logger.warning("Webhook 2FA HTTP %s", response.status_code)
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail=f"O serviço de 2FA retornou HTTP {response.status_code}.",
            )

        # Parse do JSON retornado pelo n8n.
        try:
            data = response.json()
        except ValueError:
            logger.warning(
                "Resposta 2FA não é JSON válido (status HTTP %s)",
                response.status_code,
            )
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Resposta inválida do serviço de 2FA",
            ) from None

        # n8n pode retornar objeto direto ou lista de objetos.
        if isinstance(data, list):
            if not data:
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY,
                    detail="Resposta vazia do serviço de 2FA",
                )
            data = data[0]

        if not isinstance(data, dict):
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Formato de resposta inválido do serviço de 2FA",
            )

        return data

    # Solicita ao n8n a geração/envio do código 2FA.
    @staticmethod
    def request_code(usuario_id: int, email: str, nome_completo: str) -> None:
        # Endereço do webhook de criação de OTP.
        url = N8NTwoFactorClientService._build_url(
            "ORIUS_2FA_CREATE_URL",
            "webhook/otp/create",
        )
        if not url:
            logger.error("ORIUS_2FA_CREATE_URL/ORIUS_2FA_BASE_URL não configurada")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de criação de código de segurança indisponível",
            )

        # Canal do envio do OTP (ex.: email, whatsapp), configurado por ambiente.
        method = (os.getenv("ORIUS_2FA_METHOD") or "email").strip().lower()
        # Origem da solicitação para auditoria no workflow externo.
        origem = (os.getenv("ORIUS_2FA_ORIGEM") or "SAAS Local").strip()

        # Payload esperado pelo workflow do n8n.
        payload = {
            "usuario_id": int(usuario_id),
            "cns": os.getenv("ORIUS_CLIENT_CNS"),
            "email_usuario": str(email),
            "whatsapp": "",
            "nome": str(nome_completo),
            "list": False,
            "origem": origem,
            "method": method,
        }

        response = N8NTwoFactorClientService._post_json(url, payload)
        data = N8NTwoFactorClientService._parse_response_json(response)

        # Contrato funcional do workflow: status precisa ser 'success'.
        if data.get("status") != "success":
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Ocorreu um erro ao gerar o código de segurança",
            )

        # No fluxo atual, o OTP fica armazenado no n8n para validação posterior.
        return None

    # Solicita ao n8n a validação do código OTP informado.
    @staticmethod
    def verify_code(usuario_id: int, codigo: str) -> bool:
        url = N8NTwoFactorClientService._build_url(
            "ORIUS_2FA_VERIFY_URL",
            "webhook/otp/verify",
        )
        if not url:
            logger.error("ORIUS_2FA_VERIFY_URL/ORIUS_2FA_BASE_URL não configurada")
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Serviço de validação de código de segurança indisponível",
            )

        payload = {
            "usuario_id": int(usuario_id),
            "codigo": str(codigo),
        }

        response = N8NTwoFactorClientService._post_json(url, payload)
        data = N8NTwoFactorClientService._parse_response_json(response)

        # Contrato do Verify da collection: status=sucesso/falha e fase=verify.
        if data.get("fase") != "verify":
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY,
                detail="Resposta inválida do serviço de validação de código",
            )

        status_verify = str(data.get("status") or "").strip().lower()
        if status_verify == "sucesso":
            return True
        if status_verify == "falha":
            return False

        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Status de validação do código não reconhecido",
        )
