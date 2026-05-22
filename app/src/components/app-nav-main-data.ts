import type { LucideIcon } from 'lucide-react';
import {
  ArrowLeftRight,
  Cpu,
  Database,
  FileText,
  LayoutDashboard,
} from 'lucide-react';

export type AppNavMainItem = {
  title: string;
  url: string;
  icon?: LucideIcon;
  isActive?: boolean;
  items?: {
    title: string;
    url: string;
  }[];
};

/** Fonte única para o menu lateral (`NavMain`) e busca do `AppHeader`. */
export const APP_NAV_MAIN_ITEMS: AppNavMainItem[] = [
  { title: 'Dashboard', url: '/', icon: LayoutDashboard },
  { title: 'Títulos', url: '/titulos', icon: FileText },
  {
    title: 'CRA',
    url: '#',
    icon: ArrowLeftRight,
    items: [
      { title: 'Importação', url: '/cra/importacao' },
      { title: 'Confirmação', url: '/cra/confirmacao' },
      { title: 'Andamento/Diário', url: '/cra/andamento' },
      { title: 'Retorno', url: '/cra/retorno' },
    ],
  },
  { title: 'Certidão', url: '/certidao', icon: FileText },
  { title: 'Apontar Títulos', url: '/apontamento-lote', icon: FileText },
  { title: 'Intimar Títulos', url: '/intimacao-lote', icon: FileText },
  { title: 'Protestar Títulos', url: '/protesto-lote', icon: FileText },
  {
    title: 'Cadastro',
    url: '#',
    icon: Database,
    items: [
      { title: 'Pessoas', url: '/cadastro/pessoas' },
      { title: 'Ocorrência', url: '/cadastro/ocorrencia' },
      { title: 'Ocorrência de Andamento', url: '/cadastro/ocorrencia-andamento' },
      { title: 'Motivo de Apontamento', url: '/cadastro/motivo-apontamento' },
      { title: 'Motivo de Cancelamento', url: '/cadastro/motivo-cancelamento' },
      { title: 'Espécie', url: '/cadastro/especie' },
      { title: 'Feriado', url: '/cadastro/feriado' },
      { title: 'Banco', url: '/cadastro/banco' },
      { title: 'Livro Andamento', url: '/cadastro/livro-andamento' },
      { title: 'Livro Natureza', url: '/cadastro/livro-natureza' },
    ],
  },
  {
    title: 'Integração',
    url: '#',
    icon: Cpu,
    items: [
      { title: 'Serasa', url: '/integracao/serasa' },
      { title: 'Cenprot', url: '/integracao/cenprot' },
      { title: 'Cenprot Emolumentos', url: '/integracao/cenprot-emolumentos' },
      { title: 'Coaf', url: '/integracao/coaf' },
    ],
  },
];
