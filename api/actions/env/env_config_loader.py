from dotenv import dotenv_values, load_dotenv
import os


class EnvConfigLoader:
    """
    Classe para carregar todas as variaveis de ambiente (.env)
    e permitir acesso via atributo (settings.VAR).
    """

    def __init__(self, env_file: str = ".env"):
        resolved_env_file = self._resolve_env_path(env_file)

        # Garante que o .env sera carregado no ambiente do sistema
        load_dotenv(resolved_env_file)

        # Le todas as variaveis (do arquivo + sistema)
        self._values = {
            **dotenv_values(resolved_env_file),  # Conteudo do .env
            **os.environ,  # Variaveis ja existentes no ambiente
        }

    def _resolve_env_path(self, env_file: str) -> str:
        """
        Resolve o arquivo de ambiente.
        1) tenta o caminho informado (ex.: .env na raiz/cwd)
        2) se nao existir, tenta um nivel acima (../.env)
        """
        if os.path.isabs(env_file):
            return env_file

        current_path = os.path.abspath(env_file)
        if os.path.exists(current_path):
            return current_path

        parent_path = os.path.abspath(os.path.join("..", env_file))
        if os.path.exists(parent_path):
            return parent_path

        # Mantem comportamento padrao quando nenhum caminho e encontrado
        return current_path

    def __getattr__(self, name: str):
        """Permite acessar como settings.VAR"""
        # Normaliza o nome para maiusculo
        key = name.upper()
        if key in self._values:
            return self._values[key]
        raise AttributeError(f"A variavel '{name}' nao existe no .env")

    def __repr__(self):
        """Exibe todas as variaveis carregadas"""
        return f"<Settings {self._values}>"

    def all(self) -> dict:
        """Retorna todas as variaveis como dicionario"""
        return dict(self._values)
