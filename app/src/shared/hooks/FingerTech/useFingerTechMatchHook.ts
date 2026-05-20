'use client';

import TBiometriaPessoaInterface from '@/packages/administrativo/interfaces/TBiometriaPessoa/TBiometriaPessoaInterface';
import { FingerTechMatchService } from '@/shared/services/FingerTech/FingerTechMatchService';

export const useFingerTechMatchHook = () => {
  const matchFingerTech = async (data: TBiometriaPessoaInterface) => {
    const response = await FingerTechMatchService(data);
    return response;
  };
  return {
    matchFingerTech,
  };
};
