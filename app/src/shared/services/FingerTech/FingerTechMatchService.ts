import TBiometriaPessoaInterface from '@/packages/administrativo/interfaces/TBiometriaPessoa/TBiometriaPessoaInterface';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import { FingerTechMatchData } from '@/shared/data/fingertech/FingerTechMatchData';

export default async function executeFingerTechMatchService(data: TBiometriaPessoaInterface) {
  const response = await FingerTechMatchData(data);
  return response;
}

export const FingerTechMatchService = withClientErrorHandler(executeFingerTechMatchService);
