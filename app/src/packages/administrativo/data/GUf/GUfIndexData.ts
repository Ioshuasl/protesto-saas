// Importa a classe API responsável por centralizar chamadas HTTP
import API from '@/shared/services/api/Api';

// Importa o enum de métodos HTTP (GET, POST, PUT, DELETE, etc.)
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

// Exporta por padrão a função assíncrona GUfIndexData
export default async function GUfIndexData() {
  // Cria uma instância da classe API para executar a requisição
  const api = new API();

  // Executa a chamada GET para o endpoint "administrativo/g_uf/" e retorna a resposta
  return await api.send({
    method: Methods.GET, // Define que o método HTTP é GET
    endpoint: `administrativo/g_uf/`, // Define o endpoint a ser acessado
  });
}
