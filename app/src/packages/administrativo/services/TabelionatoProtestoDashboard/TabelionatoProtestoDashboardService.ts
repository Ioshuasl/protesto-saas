import { TabelionatoProtestoDashboardFunilService } from '@/packages/administrativo/services/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardFunilService';
import { TabelionatoProtestoDashboardResumoService } from '@/packages/administrativo/services/TabelionatoProtestoDashboard/TabelionatoProtestoDashboardResumoService';

export const TabelionatoProtestoDashboardService = {
  getResumo: TabelionatoProtestoDashboardResumoService,
  getFunil: TabelionatoProtestoDashboardFunilService,
};
