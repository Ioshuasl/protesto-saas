'use client';

import { FingerTechCaptureService } from '@/shared/services/FingerTech/FingerTechCaptureService';

export const useFingerTechCaptureHook = () => {
  const captureFingerTech = async () => {
    const response = await FingerTechCaptureService();
    return response;
  };
  return {
    captureFingerTech,
  };
};
