from datetime import datetime, timedelta
from jose import jwt
from pytz import timezone

from abstracts.action import BaseAction
from actions.config.config import Config


class CreateToken(BaseAction):
    def __init__(self):

        # Busca as configurações da aplicação
        self.config = Config.get("app.json")

        # Cria o timedelta com base na config
        self.access_token_expire = timedelta(
            minutes=self.config.jwt.expire.minute,
            hours=self.config.jwt.expire.hours,
            days=self.config.jwt.expire.days,
        )

    def execute(self, tipo_token: str, data: str) -> str:

        sp = timezone("America/Sao_Paulo")
        agora = datetime.now(tz=sp)
        expira = agora + self.access_token_expire

        # Define os dados do token
        payload = {"type": tipo_token, "exp": expira, "iat": agora, "data": str(data)}

        # Retorna os dados codificados
        return jwt.encode(
            payload, self.config.jwt.token, algorithm=self.config.jwt.algorithm
        )
