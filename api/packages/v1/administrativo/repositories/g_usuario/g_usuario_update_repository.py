from abstracts.repository import BaseRepository
from packages.v1.administrativo.schemas.g_usuario_schema import GUsuarioUpdateSchema
from fastapi import HTTPException, status

class UpdateRepository(BaseRepository):

    def execute(self, usuario_id: int, usuario_schema: GUsuarioUpdateSchema):
        try:
            updates = []
            params = {}

            if usuario_schema.trocarsenha is not None:
                updates.append("TROCARSENHA = :trocarsenha")
                params["trocarsenha"] = usuario_schema.trocarsenha

            if usuario_schema.login is not None:
                updates.append("LOGIN = :login")
                params["login"] = usuario_schema.login

            if usuario_schema.situacao is not None:
                updates.append("SITUACAO = :situacao")
                params["situacao"] = usuario_schema.situacao

            if usuario_schema.nome_completo is not None:
                updates.append("NOME_COMPLETO = :nome_completo")
                params["nome_completo"] = usuario_schema.nome_completo

            if usuario_schema.funcao is not None:
                updates.append("FUNCAO = :funcao")
                params["funcao"] = usuario_schema.funcao

            if usuario_schema.email is not None:
                updates.append("EMAIL = :email")
                params["email"] = usuario_schema.email

            if usuario_schema.cpf is not None:
                updates.append("CPF = :cpf")
                params["cpf"] = usuario_schema.cpf

            if usuario_schema.senha_api is not None:
                updates.append("SENHA_API = :senha_api")
                params["senha_api"] = usuario_schema.senha_api

            if not updates:
                return False

            params["usuario_id"] = usuario_id
            sql = f"UPDATE G_USUARIO SET {', '.join(updates)} WHERE USUARIO_ID = :usuario_id RETURNING *;"

            # Executa a query
            result = self.run_and_return(sql, params)

            if not result.usuario_id:

                # Informa que não existe usuário a ser modificado
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                    detail='Nenhum usuário localizado para esta solicitação'
                )                
            
            # Verifica o resultado da execução
            if result:
                # Se houver um resultado, a atualização foi bem-sucedida
                return result


        except Exception as e:
        
            # Informa que houve  uma falha na atualização do usuário
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail=f"Erro ao atualizar usuário: {e}"
            )         