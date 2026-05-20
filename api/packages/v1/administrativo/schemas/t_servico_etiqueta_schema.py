from pydantic import BaseModel, model_validator
from fastapi import HTTPException, status
from typing import Optional

# Funções para sanitização de entradas (evitar XSS, SQLi etc.)
# Assumindo que a classe Text está disponível no caminho 'actions.validations.text'

# ----------------------------------------------------
# Schema base
# ----------------------------------------------------
class TServicoEtiquetaSchema(BaseModel):
    # SERVICO_ETIQUETA_ID NUMERIC(10,2) NOT NULL (Chave Primária)
    servico_etiqueta_id: Optional[int] = None
    
    # ETIQUETA_MODELO_ID NUMERIC(10,2)
    etiqueta_modelo_id: Optional[int] = None 
    
    # SERVICO_TIPO_ID NUMERIC(10,2) (Chave Estrangeira)
    servico_tipo_id: Optional[int] = None 

    class Config:
        from_attributes = True


# ----------------------------------------------------
# Schema para localizar um SERVICO_ETIQUETA especifico pelo ID (GET)
# ----------------------------------------------------
class TServicoEtiquetaIdSchema(BaseModel):
    servico_etiqueta_id: int


# ----------------------------------------------------
# Schema para localizar um SERVICO_ETIQUETA pelo SERVICO_TIPO_ID (GET)
# Útil para buscar todas as etiquetas de um determinado tipo de serviço.
# ----------------------------------------------------
class TServicoEtiquetaServicoTipoIdSchema(BaseModel):
    servico_tipo_id: int    


# ----------------------------------------------------
# Schema para criação de novo SERVICO_ETIQUETA (POST)
# ----------------------------------------------------
class TServicoEtiquetaSaveSchema(BaseModel):
    # SERVICO_ETIQUETA_ID é geralmente definido pelo banco de dados ou é opcional para o POST
    servico_etiqueta_id: Optional[int] = None
    
    # ETIQUETA_MODELO_ID é obrigatório na criação (assumindo que deve ser associado a um modelo)
    etiqueta_modelo_id: int 
    
    # SERVICO_TIPO_ID é obrigatório na criação (assumindo que deve ser associado a um serviço)
    servico_tipo_id: int 

    # Não há campos string na DDL para sanitização, mas manter a estrutura de validação por boa prática
    
    @model_validator(mode='after')
    def validate_all_fields(self):
        errors = []
        
        required_fields = {
            'etiqueta_modelo_id': 'O ID do Modelo de Etiqueta (etiqueta_modelo_id) é obrigatório.',
            'servico_tipo_id': 'O ID do Tipo de Serviço (servico_tipo_id) é obrigatório.',
        }

        for field_name, message in required_fields.items():
            field_value = getattr(self, field_name, None)
            
            if field_value is None:
                errors.append({'input': field_name, 'message': message})
            # A DDL usa NUMERIC(10,2), então verificamos se é um número inteiro válido (e > 0 se for PK/FK)
            elif not isinstance(field_value, int) or field_value <= 0:
                 errors.append({'input': field_name, 'message': f"{message} Deve ser um número inteiro positivo."})


        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self


# ----------------------------------------------------
# Schema para atualizar SERVICO_ETIQUETA (PUT)
# ----------------------------------------------------
class TServicoEtiquetaUpdateSchema(BaseModel):

    etiqueta_modelo_id: Optional[int] = None
    servico_tipo_id: Optional[int] = None

    # Não há campos string na DDL para sanitização, mas a estrutura de validação é adaptada.
    
    # Verifica se pelo menos um campo foi enviado, se não, lança exceção.
    @model_validator(mode='after')
    def validate_all_fields(self):
        
        updatable_fields = {
            'etiqueta_modelo_id': 'O ID do Modelo de Etiqueta (etiqueta_modelo_id) não pode ser nulo ou zero.',
            'servico_tipo_id': 'O ID do Tipo de Serviço (servico_tipo_id) não pode ser nulo ou zero.',
        }

        has_data = False
        errors = []

        for field_name, message in updatable_fields.items():
            field_value = getattr(self, field_name, None)
            
            if field_value is not None:
                has_data = True
                
                # Para campos NUMERIC(10,2) que são FKs, verifica se são inteiros e positivos
                if isinstance(field_value, int) and field_value <= 0:
                     errors.append({'input': field_name, 'message': f"O campo {field_name} deve ser um número inteiro positivo."})
                

        if not has_data:
            errors.append({'message': 'Pelo menos um campo deve ser fornecido para a atualização.'})

        if errors:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=errors
            )

        return self