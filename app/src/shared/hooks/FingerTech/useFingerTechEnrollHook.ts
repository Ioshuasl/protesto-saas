'use client';

import { useState } from 'react';

import { FingerTechEnrollService } from '@/shared/services/FingerTech/FingerTechEnrollService';

export const useFingerTechEnrollHook = () => {
  const [base64, setBase64] = useState<string>('');

  const enrollFingerTech = async () => {
    const response = await FingerTechEnrollService();

    const base64Data = response?.data ?? '';

    setBase64(base64Data);

    return response;
  };

  return {
    base64,
    enrollFingerTech,
  };
};
