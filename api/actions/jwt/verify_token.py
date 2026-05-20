from jose import jwt, JWTError, ExpiredSignatureError

from actions.config.config import Config


class VerifyToken:
    def __init__(self):
        # Carrega configurações
        self.config = Config.get('app.json')

    def execute(self, token: str, expected_type: str = 'access-token') -> dict:
        try:
            # Decodifica o token
            payload = jwt.decode(
                token,
                self.config.jwt.token,
                algorithms=[self.config.jwt.algorithm]
            )

            # Valida expiração
            exp_timestamp = payload.get("exp")
            if exp_timestamp is None:
                raise ValueError("O token não possui data de expiração.")

            # Verifica o tipo de token
            token_type = payload.get("type")
            if token_type != expected_type:
                raise ValueError("Tipo de token inválido.")

            # Verificação opcional: validar campo "data"
            if "data" not in payload:
                raise ValueError("Token malformado: campo 'data' ausente.")

            return {
                "status": "valid",
                "payload": payload
            }

        except ExpiredSignatureError:
            return {
                "status": "expired",
                "message": "O token expirou."
            }

        except JWTError as e:
            return {
                "status": "invalid",
                "message": f"Token inválido: {str(e)}"
            }

        except Exception as e:
            return {
                "status": "error",
                "message": f"Erro na validação do token: {str(e)}"
            }