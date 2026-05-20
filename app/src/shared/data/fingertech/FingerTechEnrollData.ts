import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

/*********************************************
 * Nome: Enroll
 * Descrição: Chama o método "Enroll" da aplicação desktop,
 * responsável por chamar a tela de captura de impressão digital para mais de um dedo.
 * Este método é recomendável quando você deseja capturar a impressão digital de mais de um dedo e
 * quando é necessário identificar a qual dedo esta digital pertence.
 * Quando houver a captura de mais de uma impressão digital, elas serão armazenadas de maneira
 * codificada no mesmo "Template" (String), mas durante a comparação qualquer dedo poderá ser
 * comparado.
 * Retorno: Template (String) ou "" (Vazio)
 *********************************************/
async function executeFingerTechEnrollData() {
  const fingertechURL = process.env.NEXT_PUBLIC_ORIUS_FINGERTECH_URL;
  const response = await fetch(`${fingertechURL}captura/Enroll/1`, {
    method: 'GET',
  });

  return await response.text();
}

export const FingerTechEnrollData = withClientErrorHandler(executeFingerTechEnrollData);
