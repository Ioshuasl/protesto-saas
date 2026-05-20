"use client";

import * as React from "react";
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarGroup,
  SidebarGroupContent,
  SidebarGroupLabel,
  SidebarHeader,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from "@/components/ui/sidebar";
import {
  LayoutDashboard,
  FileText,
  ArrowLeftRight,
  Database,
  Cpu,
  ChevronRight,
  GalleryVerticalEnd,
} from "lucide-react";
import Image from "next/image";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from "@/components/ui/collapsible";

type NavIcon = React.ComponentType<{ className?: string; strokeWidth?: number }>;

export type ProtestoLeafNavItem = {
  title: string;
  url: string;
  icon: NavIcon;
};

export type ProtestoGroupNavItem = {
  title: string;
  icon: NavIcon;
  items: ReadonlyArray<{ title: string; url: string }>;
};

export type ProtestoNavItem = ProtestoLeafNavItem | ProtestoGroupNavItem;

export const protestoNavItems: ReadonlyArray<ProtestoNavItem> = [
  { title: "Dashboard", url: "/", icon: LayoutDashboard },
  { title: "Títulos", url: "/titulos", icon: FileText },
  {
    title: "CRA",
    icon: ArrowLeftRight,
    items: [
      { title: "Importação", url: "/cra/importacao" },
      { title: "Confirmação", url: "/cra/confirmacao" },
      { title: "Andamento/Diário", url: "/cra/andamento" },
      { title: "Retorno", url: "/cra/retorno" },
    ],
  },
  { title: "Certidão", url: "/certidao", icon: FileText },
  { title: "Apontar Títulos", url: "/apontamento-lote", icon: FileText },
  { title: "Intimar Títulos", url: "/intimacao-lote", icon: FileText },
  { title: "Protestar Títulos", url: "/protesto-lote", icon: FileText },
  {
    title: "Cadastro",
    icon: Database,
    items: [
      { title: "Pessoas", url: "/cadastro/pessoas" },
      { title: "Ocorrência", url: "/cadastro/ocorrencia" },
      { title: "Motivo de Apontamento", url: "/cadastro/motivo-apontamento" },
      { title: "Motivo de Cancelamento", url: "/cadastro/motivo-cancelamento" },
      { title: "Espécie", url: "/cadastro/especie" },
      { title: "Feriado", url: "/cadastro/feriado" },
      { title: "Banco", url: "/cadastro/banco" },
      { title: "Livro Andamento", url: "/cadastro/livro-andamento" },
      { title: "Livro Natureza", url: "/cadastro/livro-natureza" },
    ],
  },
  {
    title: "Integração",
    icon: Cpu,
    items: [
      { title: "Serasa", url: "/integracao/serasa" },
      { title: "Cenprot", url: "/integracao/cenprot" },
      { title: "Cenprot Emolumentos", url: "/integracao/cenprot-emolumentos" },
      { title: "Coaf", url: "/integracao/coaf" },
    ],
  },
];

function NavCollapsibleItem({
  item,
  pathname,
}: {
  item: ProtestoGroupNavItem;
  pathname: string;
}) {
  const [isOpen, setIsOpen] = React.useState(() =>
    item.items.some((sub) => pathname === sub.url || pathname.startsWith(sub.url + "/")),
  );

  return (
    <Collapsible open={isOpen} onOpenChange={setIsOpen} className="group/collapsible">
      <SidebarMenuItem>
        <CollapsibleTrigger asChild>
          <SidebarMenuButton
            tooltip={item.title}
            className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
          >
            <item.icon className="h-4 w-4" strokeWidth={1.5} />
            <span className="font-medium">{item.title}</span>
            <ChevronRight className="ml-auto h-4 w-4 transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" strokeWidth={1.5} />
          </SidebarMenuButton>
        </CollapsibleTrigger>
        <CollapsibleContent className="overflow-hidden data-[state=closed]:animate-collapsible-up data-[state=open]:animate-collapsible-down">
          <SidebarMenuSub>
            {item.items.map((subItem) => (
              <SidebarMenuSubItem key={subItem.title}>
                <SidebarMenuSubButton
                  asChild
                  isActive={pathname === subItem.url}
                  className="data-[active=true]:bg-primary/10 data-[active=true]:text-primary"
                >
                  <Link href={subItem.url}>
                    <span className="font-normal">{subItem.title}</span>
                  </Link>
                </SidebarMenuSubButton>
              </SidebarMenuSubItem>
            ))}
          </SidebarMenuSub>
        </CollapsibleContent>
      </SidebarMenuItem>
    </Collapsible>
  );
}

export function ProtestoSidebar() {
  const pathname = usePathname() ?? "/";

  return (
    <Sidebar>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <a href="#">
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center rounded-lg">
                  <GalleryVerticalEnd className="size-4" />
                  <Image
                    src="/logo-abb.png"
                    alt="Logo do site"
                    width={100}
                    height={100}
                    unoptimized
                    className="rounded-lg"
                  />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">Orius Tecnologia</span>
                  <span>25.9.1</span>
                </div>
              </a>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <SidebarGroup>
          <SidebarGroupLabel>Protesto</SidebarGroupLabel>
          <SidebarGroupContent>
            <SidebarMenu>
              {protestoNavItems.map((item) => (
                <React.Fragment key={item.title}>
                  {"items" in item ? (
                    <NavCollapsibleItem item={item} pathname={pathname} />
                  ) : (
                    <SidebarMenuItem>
                      <SidebarMenuButton
                        asChild
                        isActive={pathname === item.url}
                        tooltip={item.title}
                        className="data-[active=true]:bg-primary/10 data-[active=true]:text-primary"
                      >
                        <Link href={item.url!}>
                          <item.icon className="h-4 w-4" strokeWidth={1.5} />
                          <span className="font-medium">{item.title}</span>
                        </Link>
                      </SidebarMenuButton>
                    </SidebarMenuItem>
                  )}
                </React.Fragment>
              ))}
            </SidebarMenu>
          </SidebarGroupContent>
        </SidebarGroup>
      </SidebarContent>
      <SidebarFooter className="p-4">
        <div className="text-center text-xs text-muted-foreground">ORIUS Protesto (Next)</div>
      </SidebarFooter>
    </Sidebar>
  );
}
