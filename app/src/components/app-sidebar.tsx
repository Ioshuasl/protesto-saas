'use client';

import Image from 'next/image';
import Link from 'next/link';
import * as React from 'react';

import { APP_NAV_MAIN_ITEMS } from '@/components/app-nav-main-data';
import { NavMain } from '@/components/nav-main';
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

export function AppSidebar({ ...props }: React.ComponentProps<typeof Sidebar>) {
  const { userAuthenticated, fetchToken } = useGUsuarioGetJWTHook();

  React.useEffect(() => {
    void fetchToken();
    // Carrega o usuário uma vez ao montar o layout (fetchToken é estável via useCallback).
  }, [fetchToken]);

  return (
    <Sidebar collapsible="icon" {...props}>
      <SidebarHeader>
        <SidebarMenu>
          <SidebarMenuItem>
            <SidebarMenuButton size="lg" asChild>
              <Link href="/">
                <div className="bg-sidebar-primary text-sidebar-primary-foreground flex aspect-square size-8 items-center justify-center overflow-hidden rounded-lg">
                  <Image
                    src="/logo.svg"
                    alt="Orius Protesto"
                    width={32}
                    height={32}
                    className="size-8 object-contain"
                  />
                </div>
                <div className="flex flex-col gap-0.5 leading-none">
                  <span className="font-semibold">Orius Tecnologia</span>
                  <span className="text-muted-foreground text-xs">Protesto</span>
                </div>
              </Link>
            </SidebarMenuButton>
          </SidebarMenuItem>
        </SidebarMenu>
      </SidebarHeader>
      <SidebarContent>
        <NavMain items={APP_NAV_MAIN_ITEMS} />
      </SidebarContent>
      <SidebarFooter>
        {userAuthenticated?.data ? (
          <NavUser user={userAuthenticated.data} />
        ) : (
          <span className="text-muted-foreground px-2 text-xs">Carregando...</span>
        )}
      </SidebarFooter>
      <SidebarRail />
    </Sidebar>
  );
}
