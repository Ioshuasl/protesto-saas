import GCidadeInterface from '@/packages/administrativo/interfaces/GCidade/GCidadeInterface'; // Interface tipada da cidade
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

async function executeGcidadeIndexData(data: GCidadeInterface) {
  const api = new API();
  return await api.send({
    method: Methods.GET, // GET listar todos os itens
    endpoint: `administrativo/g_cidade/${data.uf}`, // endpoint dinâmico
  });
}
export const GCidadeIndexData = withClientErrorHandler(executeGcidadeIndexData);
