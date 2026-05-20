import { AlertCircleIcon, BadgeCheckIcon, FileTextIcon, RotateCcwIcon, XIcon } from 'lucide-react';

import { SituacoesAtoValue } from '@/shared/enums/SituacoesAtoEnum';

export const SituacoesAtosBadgeMap: Record<
  SituacoesAtoValue,
  {
    label: string;
    icon: any;
    color: string;
    bg: string;
  }
> = {
  0: {
    label: 'Doc. Pendente',
    icon: FileTextIcon,
    color: 'text-gray-700 dark:text-gray-300',
    bg: 'bg-gray-50 dark:bg-gray-900/30',
  },
  1: {
    label: 'Montagem',
    icon: AlertCircleIcon,
    color: 'text-blue-700 dark:text-blue-300',
    bg: 'bg-blue-50 dark:bg-blue-900/20',
  },
  2: {
    label: 'Pré-lavrado',
    icon: AlertCircleIcon,
    color: 'text-indigo-700 dark:text-indigo-300',
    bg: 'bg-indigo-50 dark:bg-indigo-900/20',
  },
  3: {
    label: 'Lavrado',
    icon: BadgeCheckIcon,
    color: 'text-emerald-700 dark:text-emerald-300',
    bg: 'bg-emerald-50 dark:bg-emerald-900/20',
  },
  4: {
    label: 'Cancelado',
    icon: XIcon,
    color: 'text-red-700 dark:text-red-300',
    bg: 'bg-red-50 dark:bg-red-900/20',
  },
  6: {
    label: 'Substabelecido',
    icon: RotateCcwIcon,
    color: 'text-purple-700 dark:text-purple-300',
    bg: 'bg-purple-50 dark:bg-purple-900/20',
  },
  7: {
    label: 'Revogado',
    icon: XIcon,
    color: 'text-rose-700 dark:text-rose-300',
    bg: 'bg-rose-50 dark:bg-rose-900/20',
  },
  8: {
    label: 'Reratificado',
    icon: RotateCcwIcon,
    color: 'text-cyan-700 dark:text-cyan-300',
    bg: 'bg-cyan-50 dark:bg-cyan-900/20',
  },
  9: {
    label: 'Renunciado',
    icon: XIcon,
    color: 'text-orange-700 dark:text-orange-300',
    bg: 'bg-orange-50 dark:bg-orange-900/20',
  },
  10: {
    label: 'Renúncia',
    icon: XIcon,
    color: 'text-orange-800 dark:text-orange-400',
    bg: 'bg-orange-100 dark:bg-orange-900/30',
  },
  11: {
    label: 'Renúncia Parcial',
    icon: XIcon,
    color: 'text-yellow-700 dark:text-yellow-300',
    bg: 'bg-yellow-50 dark:bg-yellow-900/20',
  },
};
