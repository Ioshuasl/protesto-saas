from pydantic import BaseModel, field_validator, model_validator
from fastapi import HTTPException, status
from typing import Optional
from decimal import Decimal

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
# Assumindo que a classe Text está disponível no caminho 'actions.validations.text'
from actions.validations.text import Text


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TServicoTipoIndexSchema(BaseModel):
    class Config:
        extra = "allow"  # permite parâmetros dinâmicos


# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TServicoTipoTopServicosTipoSchema(BaseModel):
    quantity: Optional[int] = None
    servico_tipo_id: Optional[int] = None
    descricao: Optional[str] = None
    tipo_item: Optional[str] = None
    tipo_pessoa: Optional[str] = None
    requer_abonador: Optional[str] = None
    requer_biometria: Optional[str] = None
    requer_cpf: Optional[str] = None
    servico_caixa_id: Optional[int] = None
    selar: Optional[str] = None

    class Config:
        from_attributes = True


class TServicoTipoSchema(BaseModel):
    servico_tipo_id: Optional[int] = None
    descricao: Optional[str] = None
    valor: Optional[float] = None  # Numeric(14,3)
    tipo_item: Optional[str] = None  # Varchar(1)
    requer_autorizacao: Optional[str] = None  # Varchar(1)
    requer_biometria: Optional[str] = None  # Varchar(1)
    tipo_pessoa: Optional[str] = None  # Varchar(1)
    tb_reconhecimentotipo_id: Optional[int] = None  # Numeric(10,2)
    tipo_permissao_cpf: Optional[str] = None  # Varchar(1)
    requer_abonador: Optional[str] = None  # Varchar(1)
    requer_representante: Optional[str] = None  # Varchar(1)
    situacao: Optional[str] = None  # Varchar(1)
    requer_cpf: Optional[str] = None  # Varchar(1)
    servico_padrao: Optional[str] = None  # Varchar(1)
    maximo_pessoa: Optional[int] = None  # Numeric(10,2)
    alterar_valor: Optional[str] = None  # Varchar(1)
    servico_caixa_id: Optional[int] = None  # Numeric(10,2)
    lancar_taxa: Optional[str] = None  # Varchar(1)
    lancar_fundesp: Optional[str] = None  # Varchar(1)
    liberar_desconto: Optional[str] = None  # Varchar(1)
    fundesp_automatica: Optional[str] = None  # Varchar(1)
    lancar_valor_documento: Optional[str] = None  # Varchar(1)
    valor_fixo: Optional[str] = None  # Varchar(1)
    emolumento_id: Optional[int] = None  # Numeric(10,2)
    ato_praticado: Optional[str] = None  # Varchar(1)
    selar: Optional[str] = None  # Varchar(1)
    frenteverso: Optional[str] = None  # Varchar(1)
    pagina_acrescida: Optional[str] = None  # Varchar(1)
    emolumento_obrigatorio: Optional[int] = None  # Numeric(10,2)
    apresentante_selo: Optional[str] = None  # Varchar(1)
    renovacao_cartao: Optional[str] = None  # Varchar(1)
    etiqueta_unica: Optional[str] = None  # Varchar(1)
    transferencia_veiculo: Optional[str] = None  # Varchar(1)
    usar_a4: Optional[str] = None  # Varchar(1)
    averbacao: Optional[str] = None  # Varchar(1)

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um SERVICO especifico pelo ID (GET)
# ----------------------------------------------------
class TServicoTipoIdSchema(BaseModel):
    servico_tipo_id: int


# ----------------------------------------------------
# Schema para localizar um SERVICO especifico pela descrição (GET)
# ----------------------------------------------------
class TServicoTipoDescricaoSchema(BaseModel):
    descricao: str


# ----------------------------------------------------
# Schema para criação de novo SERVICO (POST)
# ----------------------------------------------------
class TServicoTipoSaveSchema(BaseModel):
    servico_tipo_id: Optional[int] = None
    descricao: str  # Obrigatório
    valor: Optional[float] = None  # Numeric(14,3)
    tipo_item: Optional[str] = None  # Varchar(1)
    requer_autorizacao: Optional[str] = None
    requer_biometria: Optional[str] = None
    tipo_pessoa: Optional[str] = None
    tb_reconhecimentotipo_id: Optional[int] = None
    tipo_permissao_cpf: Optional[str] = None
    requer_abonador: Optional[str] = None
    requer_representante: Optional[str] = None
    situacao: Optional[str] = None
    requer_cpf: Optional[str] = None
    servico_padrao: Optional[str] = None
    maximo_pessoa: Optional[int] = None
    alterar_valor: Optional[str] = None
    servico_caixa_id: Optional[int] = None
    lancar_taxa: Optional[str] = None
    lancar_fundesp: Optional[str] = None
    liberar_desconto: Optional[str] = None
    fundesp_automatica: Optional[str] = None
    lancar_valor_documento: Optional[str] = None
    valor_fixo: Optional[str] = None
    emolumento_id: Optional[int] = None
    ato_praticado: Optional[str] = None
    selar: Optional[str] = None
    frenteverso: Optional[str] = None
    pagina_acrescida: Optional[str] = None
    emolumento_obrigatorio: Optional[Decimal] = None
    apresentante_selo: Optional[str] = None
    renovacao_cartao: Optional[str] = None
    etiqueta_unica: Optional[str] = None
    transferencia_veiculo: Optional[str] = None
    usar_a4: Optional[str] = None
    averbacao: Optional[str] = None

    # Sanitização dos campos string (para prevenir XSS e entradas inválidas)
    @field_validator(
        "descricao",
        "tipo_item",
        "requer_autorizacao",
        "requer_biometria",
        "tipo_pessoa",
        "tipo_permissao_cpf",
        "requer_abonador",
        "requer_representante",
        "situacao",
        "requer_cpf",
        "servico_padrao",
        "alterar_valor",
        "lancar_taxa",
        "lancar_fundesp",
        "liberar_desconto",
        "fundesp_automatica",
        "lancar_valor_documento",
        "valor_fixo",
        "ato_praticado",
        "selar",
        "frenteverso",
        "pagina_acrescida",
        "apresentante_selo",
        "renovacao_cartao",
        "etiqueta_unica",
        "transferencia_veiculo",
        "usar_a4",
        "averbacao",
    )
    def sanitize_fields(cls, v):
        if isinstance(v, str) and v:
            return Text.sanitize_input(v)
        return v

    # Validação de obrigatoriedade apenas para o campo 'descricao'
    @model_validator(mode="after")
    def validate_required_fields(self):
        if not self.descricao or not self.descricao.strip():
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=[
                    {"input": "descricao", "message": "A descrição é obrigatória."}
                ],
            )
        return self


# ----------------------------------------------------
# Schema para atualizar SERVICO (PUT)
# ----------------------------------------------------
class TServicoTipoUpdateSchema(BaseModel):

    descricao: Optional[str] = None
    valor: Optional[float] = None
    tipo_item: Optional[str] = None
    requer_autorizacao: Optional[str] = None
    requer_biometria: Optional[str] = None
    tipo_pessoa: Optional[str] = None
    tb_reconhecimentotipo_id: Optional[int] = None
    tipo_permissao_cpf: Optional[str] = None
    requer_abonador: Optional[str] = None
    requer_representante: Optional[str] = None
    situacao: Optional[str] = None
    requer_cpf: Optional[str] = None
    servico_padrao: Optional[str] = None
    maximo_pessoa: Optional[int] = None
    alterar_valor: Optional[str] = None
    servico_caixa_id: Optional[int] = None
    lancar_taxa: Optional[str] = None
    lancar_fundesp: Optional[str] = None
    liberar_desconto: Optional[str] = None
    fundesp_automatica: Optional[str] = None
    lancar_valor_documento: Optional[str] = None
    valor_fixo: Optional[str] = None
    emolumento_id: Optional[int] = None
    ato_praticado: Optional[str] = None
    selar: Optional[str] = None
    frenteverso: Optional[str] = None
    pagina_acrescida: Optional[str] = None
    emolumento_obrigatorio: Optional[Decimal] = None
    apresentante_selo: Optional[str] = None
    renovacao_cartao: Optional[str] = None
    etiqueta_unica: Optional[str] = None
    transferencia_veiculo: Optional[str] = None
    usar_a4: Optional[str] = None
    averbacao: Optional[str] = None

    # Campos que devem ser sanitizados (strings)
    @field_validator(
        "descricao",
        "tipo_item",
        "requer_autorizacao",
        "requer_biometria",
        "tipo_pessoa",
        "tipo_permissao_cpf",
        "requer_abonador",
        "requer_representante",
        "situacao",
        "requer_cpf",
        "servico_padrao",
        "alterar_valor",
        "lancar_taxa",
        "lancar_fundesp",
        "liberar_desconto",
        "fundesp_automatica",
        "lancar_valor_documento",
        "valor_fixo",
        "ato_praticado",
        "selar",
        "frenteverso",
        "pagina_acrescida",
        "apresentante_selo",
        "renovacao_cartao",
        "etiqueta_unica",
        "transferencia_veiculo",
        "usar_a4",
        "averbacao",
    )
    def sanitize_fields(cls, v):
        if isinstance(v, str) and v:
            return Text.sanitize_input(v)
        return v

    # Verifica se pelo menos um campo foi enviado, se não, lança exceção.
    # Se algum campo for enviado, ele deve ser válido (ex: 'descricao' não pode ser string vazia).
    @model_validator(mode="after")
    def validate_all_fields(self):
        # Campos que, se fornecidos, não podem ser None ou strings vazias/apenas espaços.
        # Todos os campos da DDL, exceto os IDs que são Opcionais (FKs), são verificados.

        updatable_fields = {
            "descricao": "A descrição não pode ser vazia.",
            "valor": "O valor não pode ser vazio.",
            "tipo_item": "O Tipo do Item não pode ser vazio.",
            "requer_autorizacao": "O Requer Autorização não pode ser vazio.",
            "requer_biometria": "O Requer Biometria não pode ser vazio.",
            "tipo_pessoa": "O Tipo Pessoa não pode ser vazio.",
            "tipo_permissao_cpf": "O Tipo Permissão CPF não pode ser vazio.",
            "requer_abonador": "O Requer Abonador não pode ser vazio.",
            "requer_representante": "O Requer Representante não pode ser vazio.",
            "situacao": "A situação não pode ser vazia.",
            "requer_cpf": "O Requer CPF não pode ser vazio.",
            "servico_padrao": "O Serviço Padrão não pode ser vazio.",
            "maximo_pessoa": "O Máximo Pessoa não pode ser vazio.",
            "alterar_valor": "O Alterar Valor não pode ser vazio.",
            "servico_caixa_id": "O Servico Caixa ID não pode ser vazio.",
            "lancar_taxa": "O Lançar Taxa não pode ser vazio.",
            "lancar_fundesp": "O Lançar FUNDESP não pode ser vazio.",
            "liberar_desconto": "O Liberar Desconto não pode ser vazio.",
            "fundesp_automatica": "O FUNDESP Automática não pode ser vazio.",
            "lancar_valor_documento": "O Lançar Valor Documento não pode ser vazio.",
            "valor_fixo": "O Valor Fixo não pode ser vazio.",
            "emolumento_id": "O Emolumento ID não pode ser vazio.",
            "ato_praticado": "O Ato Praticado não pode ser vazio.",
            "selar": "O Selar não pode ser vazio.",
            "frenteverso": "O FrenteVerso não pode ser vazio.",
            "pagina_acrescida": "A Página Acrescida não pode ser vazia.",
            "emolumento_obrigatorio": "O Emolumento Obrigatório não pode ser vazio.",
            "apresentante_selo": "O Apresentante Selo não pode ser vazio.",
            "renovacao_cartao": "A Renovação Cartão não pode ser vazia.",
            "etiqueta_unica": "A Etiqueta Única não pode ser vazia.",
            "transferencia_veiculo": "A Transferência Veículo não pode ser vazia.",
            "usar_a4": "O Usar A4 não pode ser vazio.",
            "averbacao": "A Averbação não pode ser vazia.",
        }

        has_data = False
        errors = []

        for field_name, message in updatable_fields.items():
            field_value = getattr(self, field_name, None)

            if field_value is not None:
                has_data = True
                # Verifica se o campo é uma string vazia ou só espaços
                if isinstance(field_value, str) and len(field_value.strip()) == 0:
                    errors.append({"input": field_name, "message": message})
                # Caso seja um campo numérico, verifica se é zero (opcional: a regra de negócio pode permitir zero)
                # elif isinstance(field_value, (int, float)) and field_value <= 0:
                #     errors.append({'input': field_name, 'message': message})

        if not has_data:
            errors.append(
                {
                    "message": "Pelo menos um campo deve ser fornecido para a atualização."
                }
            )

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=errors
            )

        return self
