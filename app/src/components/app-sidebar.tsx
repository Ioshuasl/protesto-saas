'use client';

import {
  Bot,
  Frame,
  GalleryVerticalEnd,
  HouseIcon,
  SquareMousePointer,
  SquareTerminal,
  UsersIcon,
} from 'lucide-react';
import Image from 'next/image';
import * as React from 'react';

import { NavMain } from '@/components/nav-main';
import { NavProjects } from '@/components/nav-projects';
import { NavUser } from '@/components/nav-user';
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarRail,
} from '@/components/ui/sidebar';
import useGUsuarioGetJWTHook from '@/shared/hooks/auth/useGUsuarioGetJWTHook';

// This is sample data.
const data = {
  teams: [],
  navMain: [
    {
      title: 'Administrativo',
      url: '#',
      icon: SquareTerminal,
      isActive: false,
      items: [
        {
          title: 'Usuários',
          url: '/usuarios/',
        },
      ],
    },
    {
      title: 'Servicos',
      url: '#',
      icon: SquareMousePointer,
      isActive: false,
      items: [
        {
          title: 'Dashboard',
          url: '/servicos/dashboard/',
        },
        {
          title: 'Pedidos',
          url: '/servicos/pedidos/',
        },
        {
          title: 'Atos',
          url: '/servicos/atos/',
        },
        {
          title: 'Configurações',
          url: '/servicos/configuracoes/',
        },
        {
          title: 'Tipos/Serviços',
          url: '/administrativo/tipos-servicos',
        },
      ],
    },
    {
      title: 'Pessoas',
      url: '#',
      icon: UsersIcon,
      isActive: false,
      items: [
        {
          title: 'Dashboard',
          url: '/administrativo/pessoas/dashboard',
        },
        {
          title: 'Físicas',
          url: '/administrativo/pessoas/fisicas',
        },
        {
          title: 'Jurídicas',
          url: '/administrativo/pessoas/juridicas',
        },
        {
          title: 'Públicas',
          url: '/administrativo/pessoas/publicas',
        },
      ],
    },
    {
      title: 'Imóveis',
      url: '#',
      icon: HouseIcon,
      isActive: false,
      items: [
        {
          title: 'Dashboard',
          url: '/administrativo/imoveis/dashboard',
        },
        {
          title: 'Urbanos',
          url: '/administrativo/imoveis/urbanos',
        },
        {
          title: 'Rurais',
          url: '/administrativo/imoveis/rurais',
        },
      ],
    },
    {
      title: 'Cadastros',
      url: '#',
      icon: Bot,
      items: [
        {
          title: 'Reconhecimentos',
          url: '/administrativo/reconhecimentos/',
        },
        {
          title: 'Andamentos',
          url: '/administrativo/andamentos/',
        },
        {
          title: 'Profissões',
          url: '/administrativo/pessoas/profissoes/',
        },
        {
          title: 'Regimes/Bens',
          url: '/administrativo/pessoas/regimes-bens/',
        },
        {
          title: 'Tipos de Logradouros',
          url: '/administrativo/imoveis/tipos-logradouro',
        },
        {
          title: 'Estado Civil',
          url: '/administrativo/pessoas/estados-civis',
        },
        {
          title: 'Regimes/Comunhão',
          url: '/administrativo/pessoas/regimes-comunhao/',
        },
        {
          title: 'Tipo de Medida',
          url: '/administrativo/medidas/tipos',
        },
        {
          title: 'Cidades',
          url: '/administrativo/cidades/',
        },
        {
          title: 'Bairro',
          url: '/administrativo/bairros',
        },
        {
          title: 'Minuta',
          url: '/administrativo/minutas/',
        },
        {
          title: 'Minuta/Naturezas',
          url: '/administrativo/minutas/naturezas',
        },
        {
          title: 'Censec/Tipo do Ato',
          url: '/administrativo/centrais/censec/tipos-atos',
        },
        {
          title: 'Censec/Qualidades',
          url: '/administrativo/centrais/censec/qualidades',
        },
        {
          title: 'Censec/Centrais',
          url: '/administrativo/centrais/censec/centrais',
        },
        {
          title: 'Censec/Natureza Litígio',
          url: '/administrativo/centrais/censec/naturezas-litigios',
        },
        {
          title: 'Atos/Partes Tipos',
          url: '/administrativo/atos/partes-tipos',
        },
        {
          title: 'Valores de Serviços',
          url: '/administrativo/valores-de-servicos',
        },
        {
          title: 'Gramatica',
          url: '/administrativo/gramatica',
        },
        {
          title: 'Configuracoes',
          url: '/administrativo/configuracoes',
        },
        {
          title: 'Cartório',
          url: '/administrativo/cartorio',
        },
        {
          title: 'Financeiro/Periodo',
          url: '/administrativo/financeiro/periodos',
        },
        {
          title: 'Financeiro/Emolumentos',
          url: '/administrativo/financeiro/emolumentos',
        },
        {
          title: 'Selos/Grupos',
          url: '/administrativo/selos/grupos',
        },
        {
          title: 'Financeiro/Cálculo Rápido',
          url: '/administrativo/financeiro/calculo-rapido',
        },
        {
          title: 'Tipos de Marcação',
          url: '/administrativo/tipos-marcacao',
        },
        {
          title: 'Sinal Publico',
          url: '/administrativo/sinal-publico',
        },
        {
          title: 'Usuários',
          url: '/administrativo/usuarios',
        },
      ],
    },
  ],
  projects: [
    {
      name: 'Escritura Pública de Compra e Venda',
      url: '#',
      icon: Frame,
    },
  ],
};

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { userAuthenticated, fetchToken } = useGUsuarioGetJWTHook();
  React.useEffect(() => {
    fetchToken();
  }, []);
  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <GalleryVerticalEnd className="size-4" />
                  <Image
                    src="/images/logo-abb.png"
                    alt="Logo do site"
                    width={100}
                    height={100}
                    className="rounded-lg"
                  />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">Orius Tecnologia</span>
                  <span className="">25.9.1</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={data.navMain} />
        <NavProjects projects={data.projects} />
      </SidebarContent>
      <SidebarFooter>
        {userAuthenticated?.data ? <NavUser user={userAuthenticated.data} /> : 'Carregando...'}
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
