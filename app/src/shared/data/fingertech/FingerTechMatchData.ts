import TBiometriaPessoaInterface from '@/packages/administrativo/interfaces/TBiometriaPessoa/TBiometriaPessoaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';

async function executeFingerTechMatchData(data: TBiometriaPessoaInterface) {
  const fingertechURL = process.env.NEXT_PUBLIC_ORIUS_FINGERTECH_URL;
  const response = await fetch(`${fingertechURL}apiservice/match-one-on-one`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ template: data.objeto }),
  });
  return await response.json();
}

export const FingerTechMatchData = withClientErrorHandler(executeFingerTechMatchData);
