from actions.dynamic_import.dynamic_import import DynamicImport
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService
from packages.v1.administrativo.schemas.t_tb_reconhecimentotipo_schema import TTbReconhecimentotipoSaveSchema, TTbReconhecimentotipoDescricaoSchema
from packages.v1.administrativo.actions.t_tb_reconhecimentotipo.t_tb_reconhecimentotipo_save_action import SaveAction
from fastapi import HTTPException, status

class TTbReconhecimentotipoSaveService:

    def __init__(self):
        # Ação responsável por carregar as services de acordo com o estado
        self.dynamic_import = DynamicImport()

        # Define o pacote que deve ser carregado
        self.dynamic_import.set_package("administrativo")

        # Define a tabela que o pacote pertence
        self.dynamic_import.set_table("t_tb_reconhecimentotipo")
        pass

    # Cadastra o novo tipo de reconhecimento
    def execute(self, reconhecimentotipo_schema: TTbReconhecimentotipoSaveSchema):

        # Armazena possíveis erros
        errors = []

        # Verifica se a descrição já está sendo utilizada
        # Importação de service
        descricao_service = self.dynamic_import.service("t_tb_reconhecimentotipo_get_descricao_service", "GetByDescricaoService")

        # Instanciamento da service
        self.descricao_service = descricao_service()

        # Verifica se a descrição já está sendo utilizada
        self.response = self.descricao_service.execute(TTbReconhecimentotipoDescricaoSchema(descricao=reconhecimentotipo_schema.descricao), False)

        # Se houver retorno significa que a descrição já está sendo utilizada
        if self.response:
            errors.append({'input': 'descricao', 'message': 'a descrição informada já está sendo utilizada.'})

        # Se houver erros, lança a exceção
        if errors:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=errors
            )

        # Verifica se precisa gerar o ID de sequência
        if not reconhecimentotipo_schema.tb_reconhecimentotipo_id:

            # Crio um objeto de sequencia
            sequencia_schema = GSequenciaSchema()

            # Define os dados para atualizar a sequencia
            sequencia_schema.tabela = 'T_TB_RECONHECIMENTOTIPO'

            # Busco a sequência atualizada
            generate = GenerateService()

            # Busco a sequência atualizada
            sequencia = generate.execute(sequencia_schema)

            # Atualiza os dados da chave primária
            reconhecimentotipo_schema.tb_reconhecimentotipo_id = sequencia.sequencia

        # Instanciamento de ações
        save_action = SaveAction()

        # Retorna o resultado da operação
        return save_action.execute(reconhecimentotipo_schema)
