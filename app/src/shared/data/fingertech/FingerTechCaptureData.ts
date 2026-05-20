'use client';

import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

/*********************************************
 * Nome: Capture
 * Descrição: Chama o método "Capture" da aplicação desktop,
 * responsável por chamar a tela de captura de digital para apenas um único dedo.
 * Este método é recomendável quando você deseja capturar a impressão digital de um único dedo e
 * não existe a necessidade de identificar qual dedo da mão esta digital pertence.
 * Retorno: Template (String) ou Null
 *********************************************/
async function executeFingerTechCaptureData() {
  const fingertechURL = process.env.NEXT_PUBLIC_ORIUS_FINGERTECH_URL;
  const response = await fetch(`${fingertechURL}capture-hash?img=true`, {
    method: 'GET',
  });
  return await response.text();
}

export const FingerTechCaptureData = withClientErrorHandler(executeFingerTechCaptureData);
