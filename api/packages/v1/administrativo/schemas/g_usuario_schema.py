from pydantic import BaseModel, EmailStr, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime
import re

# Funções utilitárias para segurança (hash e verificação de senha)
from actions.security.security import Security

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text

# Funções para validar E-mail
from actions.validations.email import Email

# Funções para validar cpf
from actions.validations.cpf import CPF


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GUsuarioIndexSchema(BaseModel):
    class Config:
        extra = "allow"  # permite parâmetros dinâmicos


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class GUsuarioSchema(BaseModel):
    usuario_id: Optional[int] = None
    trocarsenha: Optional[str] = None
    login: str
    senha: Optional[str] = None
    situacao: Optional[str] = None
    nome_completo: Optional[str] = None
    funcao: Optional[str] = None
    assina: Optional[str] = None
    sigla: Optional[str] = None
    usuario_tab: Optional[str] = None
    ultimo_login: Optional[datetime] = None
    ultimo_login_regs: Optional[datetime] = None
    data_expiracao: Optional[datetime] = None
    senha_anterior: Optional[str] = None
    andamento_padrao: Optional[str] = None
    lembrete_pergunta: Optional[str] = None
    lembrete_resposta: Optional[str] = None
    andamento_padrao2: Optional[str] = None
    receber_mensagem_arrolamento: Optional[str] = None
    email: Optional[EmailStr] = None
    assina_certidao: Optional[str] = None
    receber_email_penhora: Optional[str] = None
    foto: Optional[str] = None
    nao_receber_chat_todos: Optional[str] = None
    pode_alterar_caixa: Optional[str] = None
    receber_chat_certidao_online: Optional[str] = None
    receber_chat_cancelamento: Optional[str] = None
    cpf: Optional[str] = None
    somente_leitura: Optional[str] = None
    receber_chat_envio_onr: Optional[str] = None
    tipo_usuario: Optional[str] = None
    senha_api: str

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para acesso ao sistema
# ----------------------------------------------------
class GUsuarioAuthenticateSchema(BaseModel):
    """
    Autenticação com um único identificador (login, e-mail ou CPF) + senha_api.
    Ex.: {"identificador": "admin", "senha_api": "123123"}
    """

    identificador: str
    senha_api: str
    codigo_seguranca: Optional[str] = None

    @staticmethod
    def _is_cpf_candidate(value: str) -> bool:
        digits = re.sub(r"\D", "", value)
        return len(digits) == 11

    @field_validator("identificador")
    @classmethod
    def validar_identificador(cls, v: str) -> str:
        if not v or not str(v).strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe o identificador",
            )
        identificador = Text.sanitize_input(str(v).strip())
        if cls._is_cpf_candidate(identificador) and not CPF.is_valid_cpf(identificador):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="CPF inválido",
            )
        return identificador

    @field_validator("senha_api")
    @classmethod
    def validar_e_sanitizar_senha(cls, v: str) -> str:
        if not v:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe a senha",
            )
        return Text.sanitize_input(v)

    @property
    def credential_mode(self) -> str:
        """email | cpf | login — inferido a partir de identificador."""
        if Email.is_valid_email(self.identificador):
            return "email"
        if self._is_cpf_candidate(self.identificador):
            return "cpf"
        return "login"

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um usuário especifico pelo ID (GET)
# ----------------------------------------------------
class GUsuarioIdSchema(BaseModel):
    usuario_id: int


# ----------------------------------------------------
# Schema para criação de novo usuário (POST)
# ----------------------------------------------------
class GUsuarioSaveSchema(BaseModel):
    usuario_id: Optional[int] = None
    trocarsenha: Optional[str] = None
    login: Optional[str] = None
    situacao: Optional[str] = None
    nome_completo: Optional[str] = None
    funcao: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    senha_api: Optional[str] = None
    confirma_senha_api: Optional[str] = None  # <- Campo adicionado

    @model_validator(mode="after")
    def validate_and_process(self):

        errors = []

        required_fields = {
            "nome_completo": "O nome completo é obrigatório.",
            "funcao": "A função é obrigatória.",
            "email": "O e-mail é obrigatório.",
            "cpf": "O CPF é obrigatório.",
            "senha_api": "A senha é obrigatória.",
            "confirma_senha_api": "A confirmação de senha é obrigatória."
        }

        # 1. Campos obrigatórios e sanitização
        for field, message in required_fields.items():
            value = getattr(self, field)
            if not value or (isinstance(value, str) and len(value.strip()) == 0):
                errors.append({"input": field, "message": message})
            else:
                if isinstance(value, str):
                    setattr(self, field, Text.sanitize_input(value))

        # 2. Validação de formato do e-mail
        if self.email:
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(str(self.email)):
                errors.append({"input": "email", "message": "O e-mail informado é inválido."})

        # 3. Validações de senha (só executa se senha_api foi preenchida)
        if self.senha_api:
            # 3a. Limite de caracteres
            if len(self.senha_api) > 10:
                errors.append({"input": "senha_api", "message": "A senha não pode ter mais de 10 caracteres."})

            # 3b. Confirmação de senha (só confronta se confirma_senha_api foi preenchida)
            if self.confirma_senha_api and self.senha_api != self.confirma_senha_api:
                errors.append({"input": "confirma_senha_api", "message": "As senhas não conferem."})

        # 4. Para aqui se houver erros
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        # 5. Hash da senha
        try:
            self.senha_api = Security.hash_senha_api(self.senha_api)
            self.confirma_senha_api = None  # <- Limpa o campo após o hash, não persiste no banco
        except Exception:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Erro ao processar segurança da senha."
            )

        return self


# ----------------------------------------------------
# Schema para atualizar usuário (PUT)
# ----------------------------------------------------
class GUsuarioUpdateSchema(BaseModel):

    trocarsenha: Optional[str] = None
    login: Optional[str] = None
    situacao: Optional[str] = None
    nome_completo: Optional[str] = None
    funcao: Optional[str] = None
    email: Optional[str] = None
    cpf: Optional[str] = None
    senha_api: Optional[str] = None
    confirma_senha_api: Optional[str] = None

    @model_validator(mode="after")
    def validate_and_process(self):

        errors = []

        required_fields = {
            "nome_completo": "O nome completo é obrigatório.",
            "funcao": "A função é obrigatória.",
            "email": "O e-mail é obrigatório.",
            "cpf": "O CPF é obrigatório.",
        }

        # 1. Validação de campos obrigatórios + sanitização
        for field, message in required_fields.items():
            value = getattr(self, field)

            if not value or (isinstance(value, str) and len(value.strip()) == 0):
                errors.append({"input": field, "message": message})
            else:
                if isinstance(value, str):
                    setattr(self, field, Text.sanitize_input(value))

        # 2. Validação de formato do e-mail
        if self.email:
            email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
            if not email_pattern.match(str(self.email)):
                errors.append({"input": "email", "message": "O e-mail informado é inválido."})

        # 3. Validação da senha (SOMENTE se informada)
        if self.senha_api:

            # sanitiza senha
            self.senha_api = Text.sanitize_input(self.senha_api)

            # limite de caracteres
            if len(self.senha_api) > 10:
                errors.append({
                    "input": "senha_api",
                    "message": "A senha não pode ter mais de 10 caracteres."
                })

            # confirmação obrigatória se senha foi enviada
            if not self.confirma_senha_api:
                errors.append({
                    "input": "confirma_senha_api",
                    "message": "Confirme a senha para realizar a alteração."
                })

            elif self.senha_api != self.confirma_senha_api:
                errors.append({
                    "input": "confirma_senha_api",
                    "message": "As senhas não conferem."
                })

        # 4. Interrompe se houver erros
        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        # 5. Hash da senha apenas se ela existir
        if self.senha_api:
            try:
                self.senha_api = Security.hash_senha_api(self.senha_api)
                self.confirma_senha_api = None
            except Exception:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Erro ao processar segurança da senha."
                )

        return self


# ----------------------------------------------------
# Schema para localizar usuário pelo e-mail
# ----------------------------------------------------
class GUsuarioEmailSchema(BaseModel):
    # Use EmailStr para garantir a validação automática do formato
    email: Optional[EmailStr] = None

    # Sanitiza o input
    @field_validator("email")
    def sanitize_email(cls, v):
        # A sanitização é feita apenas se o valor não for None ou vazio
        if v:
            return Text.sanitize_input(v)
        return v

    # Verifica se o e-mail é válido
    @field_validator("email")
    def check_email(cls, v):
        # A verificação é feita apenas se o valor não for None ou vazio
        if not Email.is_valid_email(v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe um e-mail válido",
            )
        return v

    # Valida se o campo não está vazio
    @model_validator(mode="after")
    def validate_email(self):
        if not self.email or len(self.email.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe um e-mail",
            )
        return self

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar usuário pelo CPF
# ----------------------------------------------------
class GUsuarioCpfSchema(BaseModel):
    # Use EmailStr para garantir a validação automática do formato
    cpf: Optional[str] = None

    # Sanitiza o input
    @field_validator("cpf")
    def sanitize_cpf(cls, v):
        # A sanitização é feita apenas se o valor não for None ou vazio
        if v:
            return Text.sanitize_input(v)
        return v

    # Verifica se o e-mail é válido
    @field_validator("cpf")
    def check_email(cls, v):
        # A verificação é feita apenas se o valor não for None ou vazio
        if not CPF.is_valid_cpf(v):
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe um CPF válido",
            )
        return v

    # Valida se o campo não está vazio
    @model_validator(mode="after")
    def validate_cpf(self):
        if not self.cpf or len(self.cpf.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe um CPF",
            )
        return self

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar usuário pelo Login
# ----------------------------------------------------
class GUsuarioLoginSchema(BaseModel):
    # Use EmailStr para garantir a validação automática do formato
    login: Optional[str] = None

    # Sanitiza o input
    @field_validator("login")
    def sanitize_login(cls, v):
        # A sanitização é feita apenas se o valor não for None ou vazio
        if v:
            return Text.sanitize_input(v)
        return v

    # Valida se o campo não está vazio
    @model_validator(mode="after")
    def validate_login(self):
        if not self.login or len(self.login.strip()) == 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Informe um Login",
            )
        return self

    class Config:
        from_attributes = True
