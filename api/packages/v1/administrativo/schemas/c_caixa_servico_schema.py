from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
from actions.validations.text import Text


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class CCaixaServicoSchema(BaseModel):

    interno_sistema: Optional[str] = None
    caixa_servico_id: int
    descricao: Optional[str] = None
    situacao: Optional[str] = None
    tipo_transacao: Optional[str] = None
    sistema_id: Optional[int] = None
    selo_grupo_id: Optional[int] = None
    emitir_relatorio: Optional[str] = None
    repasse: Optional[str] = None
    repetir_descricao: Optional[str] = None
    codigo_conta: Optional[int] = None
    tipo_conta_carneleao: Optional[str] = None
    centro_de_custa_id: Optional[int] = None
    devolucao_juizo: Optional[str] = None

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para criação de novo servico (POST)
# ----------------------------------------------------
class CCaixaServicoSaveSchema(BaseModel):

    caixa_servico_id: Optional[int] = None
    tipo_transacao: Optional[str] = None
    sistema_id: Optional[int] = None
    situacao: Optional[str] = None
    interno_sistema: Optional[str] = None
    descricao: Optional[str] = None
    emitir_relatorio: Optional[str] = None
    tipo_conta_carneleao: Optional[str] = None
    centro_de_custa_id: Optional[int] = None
    repetir_descricao: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator(
        "tipo_transacao",
        "situacao",
        "interno_sistema",
        "descricao",
        "emitir_relatorio",
        "tipo_conta_carneleao",
        "repetir_descricao",
    )
    def validate_required_fields(cls, v):

        # Se for string e composta só por dígitos
        if v is None or (isinstance(v, str) and len(v.strip()) == 0):
            # Não lança exceção aqui, apenas retorna para o model_validator
            pass

        return Text.sanitize_input(v)

    # Validador para `sistema_id` e outros campos numéricos, se necessário
    @field_validator("sistema_id")
    def validate_sistema_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("O sistema precisa ser informado.")
        return v

    # Verifica se os campos foram enviados
    @model_validator(mode="after")
    def validate_all_fields(self):

        # Variavel responsavel em armaezar os erros
        errors = []

        # Validação do tipo_transacao
        if not self.tipo_transacao or len(self.tipo_transacao.strip()) == 0:
            errors.append(
                {
                    "input": "tipo_transacao",
                    "message": "O tipo transação é obrigatório.",
                }
            )

        # Validação da sistema_id
        if not self.sistema_id or self.sistema_id == 0:
            errors.append(
                {"input": "sistema_id", "message": "O sistema precisa ser informado."}
            )

        # Validação do situacao
        if not self.situacao or len(self.situacao.strip()) == 0:
            errors.append({"input": "situacao", "message": "A situação é obrigatório."})

        # Validação da interno_sistema
        if not self.interno_sistema or len(self.interno_sistema.strip()) == 0:
            errors.append(
                {"input": "interno_sistema", "message": "O uso interno é obrigatória."}
            )

        # Validação do descricao
        if not self.descricao or len(self.descricao.strip()) == 0:
            errors.append(
                {"input": "descricao", "message": "A descrição é obrigatório."}
            )

        # Validação do emitir_relatorio
        if not self.emitir_relatorio or len(self.emitir_relatorio.strip()) == 0:
            errors.append(
                {
                    "input": "emitir_relatorio",
                    "message": "Sair nos relatórios é obrigatório.",
                }
            )

        # Validação do repetir_descricao
        if not self.repetir_descricao or len(self.repetir_descricao.strip()) == 0:
            errors.append(
                {
                    "input": "repetir_descricao",
                    "message": "Repetir descrição de serviço no caixa é obrigatório.",
                }
            )

        # Se houver errors, lança uma única exceção
        if errors:
            # Lança uma exceção do FastAPI para um tratamento limpo
            # O `detail` da exceção será a lista de errors que criamos
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar caixa serviço (PUT)
# ----------------------------------------------------
class CCaixaServicoUpdateSchema(BaseModel):

    tipo_transacao: Optional[str] = None
    sistema_id: Optional[int] = None
    situacao: Optional[str] = None
    interno_sistema: Optional[str] = None
    descricao: Optional[str] = None
    emitir_relatorio: Optional[str] = None
    tipo_conta_carneleao: Optional[str] = None
    centro_de_custa_id: Optional[int] = None
    repetir_descricao: Optional[str] = None

    # Sanitiza os inputs enviados
    @field_validator(
        "tipo_transacao",
        "situacao",
        "interno_sistema",
        "descricao",
        "emitir_relatorio",
        "tipo_conta_carneleao",
        "repetir_descricao",
    )
    def validate_required_fields(cls, v):
        if not v or len(v.strip()) == 0:
            # Não lança exceção aqui. Apenas retorna para o model_validator.
            # O Pydantic já faria a checagem básica.
            # Este validador individual é mais para sanitização.
            pass
        return Text.sanitize_input(v)

    # Validador para `sistema_id` e outros campos numéricos, se necessário
    @field_validator("sistema_id")
    def validate_sistema_id(cls, v):
        if v is not None and v <= 0:
            raise ValueError("O sistema precisa ser informado.")
        return v

    # Verifica se os campos foram enviados
    @model_validator(mode="after")
    def validate_all_fields(self):

        # Variavel responsavel em armaezar os erros
        errors = []

        # Validação do tipo_transacao
        if not self.tipo_transacao or len(self.tipo_transacao.strip()) == 0:
            errors.append(
                {
                    "input": "tipo_transacao",
                    "message": "O tipo transação é obrigatório.",
                }
            )

        # Validação da sistema_id
        if not self.sistema_id or self.sistema_id == 0:
            errors.append(
                {"input": "sistema_id", "message": "O sistema precisa ser informado."}
            )

        # Validação do situacao
        if not self.situacao or len(self.situacao.strip()) == 0:
            errors.append({"input": "situacao", "message": "A situação é obrigatório."})

        # Validação da interno_sistema
        if not self.interno_sistema or len(self.interno_sistema.strip()) == 0:
            errors.append(
                {"input": "interno_sistema", "message": "O uso interno é obrigatória."}
            )

        # Validação do descricao
        if not self.descricao or len(self.descricao.strip()) == 0:
            errors.append(
                {"input": "descricao", "message": "A descrição é obrigatório."}
            )

        # Validação do emitir_relatorio
        if not self.emitir_relatorio or len(self.emitir_relatorio.strip()) == 0:
            errors.append(
                {
                    "input": "emitir_relatorio",
                    "message": "Sair nos relatórios é obrigatório.",
                }
            )

        # Validação do repetir_descricao
        if not self.repetir_descricao or len(self.repetir_descricao.strip()) == 0:
            errors.append(
                {
                    "input": "repetir_descricao",
                    "message": "Repetir descrição de serviço no caixa é obrigatório.",
                }
            )

        # Se houver errors, lança uma única exceção
        if errors:
            # Lança uma exceção do FastAPI para um tratamento limpo
            # O `detail` da exceção será a lista de errors que criamos
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para localizar um caixa serviço especifico pelo ID (GET)
# ----------------------------------------------------
class CCaixaServicoIdSchema(BaseModel):
    caixa_servico_id: int


# ----------------------------------------------------
# Schema para localizar um caixa serviço especifico pelo ID (GET)
# ----------------------------------------------------
class CCaixaServicoSistemaIdSchema(BaseModel):
    sistema_id: int


# ----------------------------------------------------
# Schema para localizar um caixa serviço pela descrição (GET)
# ----------------------------------------------------
class CCaixaServicoDescricaoSchema(BaseModel):

    # Campos utilizados
    descricao: str  # senha_api obrigatório

    # Validação e sanitização do login
    @field_validator("descricao")
    def validar_e_sanitizar_descricao(cls, v):

        # Verifica se a descrição foi informada
        if not v:

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, detail="Informe a descrição"
            )

        # Sanitiza a decrição para evitar XSS e SQL Injection
        return Text.sanitize_input(v)

    class Config:
        from_attributes = True
