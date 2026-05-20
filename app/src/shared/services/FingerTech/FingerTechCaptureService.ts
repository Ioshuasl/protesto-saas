'use client';

import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import { FingerTechCaptureData } from '@/shared/data/fingertech/FingerTechCaptureData';

export default async function executeFingerTechCaputreService() {
  const response = await FingerTechCaptureData();
  return response;
}

export const FingerTechCaptureService = withClientErrorHandler(executeFingerTechCaputreService);
