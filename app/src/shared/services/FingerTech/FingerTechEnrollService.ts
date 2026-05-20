import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import { FingerTechEnrollData } from '@/shared/data/fingertech/FingerTechEnrollData';

export default async function executeFingerTechCEnrollService() {
  const response = await FingerTechEnrollData();
  return response;
}

export const FingerTechEnrollService = withClientErrorHandler(executeFingerTechCEnrollService);
