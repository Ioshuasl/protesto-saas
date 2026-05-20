
from fastapi import HTTPException, status
from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioSaveSchema

class SaveRepository(BaseRepository):

    def execute(self, usuario_schema : GUsuarioSaveSchema):
            
        try:

            # Montagem do SQL
            sql = """ UPDATE OR INSERT INTO G_USUARIO(
                        USUARIO_ID,
                        TROCARSENHA,
                        SITUACAO,
                        NOME_COMPLETO,
                        FUNCAO,
                        EMAIL,
                        CPF,
                        SENHA_API
                        ) VALUES (
                            :usuario_id,
                            :trocarsenha,
                            :situacao,
                            :nome_completo,
                            :funcao,
                            :email,
                            :cpf,
                            :senha_api
                        ) MATCHING (usuario_id) RETURNING *;"""
            
            # Preenchimento de parâmetros
            params = {
                'usuario_id': usuario_schema.usuario_id,
                'trocarsenha': usuario_schema.trocarsenha,
                'login': usuario_schema.login,
                'situacao': usuario_schema.situacao,
                'nome_completo': usuario_schema.nome_completo,
                'funcao': usuario_schema.funcao,
                'email': usuario_schema.email,
                'cpf': usuario_schema.cpf,
                'senha_api': usuario_schema.senha_api
            }

            # Excução do sql
            return self.run_and_return(sql, params)
    
        except Exception as e:
        
            # Informa que houve  uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao salvar usuário: {e}"
            )     