import json
import base64

from packages.v1.administrativo.actions.t_biometria_pessoa.t_biometria_pessoa_save_action import (
    TBiometriaPessoaSaveAction,
)
from packages.v1.ged.actions.ged_convert_to_jpg import GEDConvertToJpg
from packages.v1.ged.actions.ged_save_action import GEDSaveAction
from packages.v1.ged.schemas.ged_schema import GEDSaveSchema
from packages.v1.sequencia.schemas.g_sequencia import GSequenciaSchema
from packages.v1.administrativo.schemas.t_biometria_pessoa_schema import (
    TBiometriaPessoaSaveSchema,
)
from packages.v1.sequencia.services.g_sequencia.generate_service import GenerateService


class TBiometriaPessoaSaveService:
    """
    Serviço responsável por encapsular a lógica de negócio para a operação
    de criação de registros na tabela T_BIOMETRIA_PESSOA.
    """

    def execute(self, data: TBiometriaPessoaSaveSchema):
        """
        Executa a operação de salvamento do registro no banco de dados.

        Args:
            data (TBiometriaPessoaSaveSchema):
                O esquema com os dados a serem salvos.

        Returns:
            O registro recém-criado.
        """
        if getattr(data, "objeto", False):

            # Converte para objeto o objeto que esta em string
            objeto = json.loads(data.objeto)

            # Percorre todas as imagens localizadas
            for finger in objeto["fingers-id"]:

                # Guarda o template da biometria COMO BASE64 (bytes)
                data.objeto = objeto["template"].encode("ascii")

                # Converte para binário a imagem de acordo com o id do dedo
                data.imagem_biometria = base64.b64decode(objeto["images"][finger - 1])

                # Define o id da biometria
                data.digital_id = finger

                # Define o id da pessoa
                data.chave_id = data.pessoa_id

                # ----------------------------------------------------
                # Geração automática de ID (sequência)
                # ----------------------------------------------------
                # Cria o schema de sequência
                sequencia_schema = GSequenciaSchema()
                sequencia_schema.tabela = "T_BIOMETRIA_PESSOA"

                # Gera a sequência atualizada
                generate = GenerateService()
                sequencia = generate.execute(sequencia_schema)

                # Atualiza o ID no schema
                data.biometria_pessoa_id = sequencia.sequencia

                # ----------------------------------------------------
                # Instanciamento e execução da Action de salvamento
                # ----------------------------------------------------
                t_biometria_pessoa_save_action = TBiometriaPessoaSaveAction()

                # Executa a ação
                response = t_biometria_pessoa_save_action.execute(data)

                # Salva a biometria em disco
                if response:

                    ged_save_action = GEDSaveAction()

                    ged_save_action.execute(
                        GEDSaveSchema(
                            base64=base64.b64encode(data.imagem_biometria),
                            pasta="Biometria",
                            registro_id=str(data.pessoa_id),
                            serventia=1,
                        )
                    )

                converter = GEDConvertToJpg()

                response.imagem_biometria = converter.convert(
                    serventia=1,
                    record_id=data.pessoa_id,
                    pasta="Biometria",
                    temp_dir=r"./storage/temp/",
                    return_type="filename",
                )

                response.objeto = ""

        return response
