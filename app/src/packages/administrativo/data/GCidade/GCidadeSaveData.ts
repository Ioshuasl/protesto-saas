// Importa o serviço de API que será utilizado para realizar requisições HTTP
import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';

// Importa o enum que contém os métodos HTTP disponíveis (GET, POST, PUT, DELETE)
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

// Importa a interface tipada que define a estrutura dos dados de uma cidade

// Importa função que encapsula chamadas assíncronas e trata erros automaticamente

// Função assíncrona que implementa a lógica de salvar (criar/atualizar) uma cidade
async function executeGcidadeSaveData(data: GCidadeInterface) {
  // Verifica se existe ID da cidade para decidir se é atualização (PUT) ou criação (POST)
  const isUpdate = Boolean(data.cidade_id);

  // Instancia o cliente da API para enviar a requisição
  const api = new API();

  // Executa a requisição para a API com o método apropriado e envia os dados no corpo
  return await api.send({
    method: isUpdate ? Methods.PUT : Methods.POST, // PUT se atualizar, POST se criar
    endpoint: `administrativo/g_cidade/${data.cidade_id || ''}`, // endpoint dinâmico
    body: data, // payload enviado para a API
  });
}

// Exporta a função de salvar cidade já encapsulada com tratamento de erros
export const GCidadeSaveData = withClientErrorHandler(executeGcidadeSaveData);
