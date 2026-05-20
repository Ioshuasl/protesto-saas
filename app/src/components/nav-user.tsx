'use client';

import { ChevronsUpDown, LogOut, Moon, Sparkles, Sun } from 'lucide-react';
import { useTheme } from 'next-themes';
import { useCallback, useState } from 'react';

import { Avatar, AvatarFallback, AvatarImage } from '@/components/ui/avatar';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuGroup,
  DropdownMenuItem,
  DropdownMenuLabel,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import {
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  useSidebar,
} from '@/components/ui/sidebar';
import { useGUsuarioLogoutHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioLogoutHook';
import ConfirmDialog from '@/shared/components/confirmDialog/ConfirmDialog';
import GUsuarioAuthenticatedInterface from '@/shared/interfaces/GUsuarioAuthenticatedInterface';

export function NavUser({ user }: { user: GUsuarioAuthenticatedInterface }) {
  // Hook para encerrar sessão
  const { logoutUsuario } = useGUsuarioLogoutHook();

  // Controle de exibição do formulário de confirmação
  const [isConfirmOpen, setIsConfirmOpen] = useState(false);

  const { isMobile } = useSidebar();

  // Tema (claro/escuro) - next-themes
  const { theme, setTheme } = useTheme();
  const isDark = theme === 'dark';

  const handleConfirmOpen = useCallback(() => {
    setIsConfirmOpen(true);
  }, []);

  const handleLogoutConfirm = useCallback(() => {
    logoutUsuario();
  }, [logoutUsuario]);

  const handleLogoutCancel = useCallback(() => {
    setIsConfirmOpen(false);
  }, []);

  const handleToggleTheme = useCallback(() => {
    setTheme(isDark ? 'light' : 'dark');
  }, [isDark, setTheme]);

  if (!user) {
    return 'Carregando...';
  }

  return (
    <>
      <SidebarMenu>
        <SidebarMenuItem>
          <DropdownMenu>
            <DropdownMenuTrigger asChild>
              <SidebarMenuButton
                size="lg"
                className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground cursor-pointer"
              >
                <Avatar className="h-8 w-8 rounded-lg">
                  <AvatarImage src={user.sigla} alt={user.nome} />
                  <AvatarFallback className="rounded-lg">{user.sigla}</AvatarFallback>
                </Avatar>

                <div className="grid flex-1 text-left text-sm leading-tight">
                  <span className="truncate font-medium">{user.nome}</span>
                  <span className="truncate text-xs">{user.email}</span>
                </div>

                <ChevronsUpDown className="ml-auto size-4" />
              </SidebarMenuButton>
            </DropdownMenuTrigger>

            <DropdownMenuContent
              className="w-(--radix-dropdown-menu-trigger-width) min-w-56 rounded-lg"
              side={isMobile ? 'bottom' : 'right'}
              align="end"
              sideOffset={4}
            >
              <DropdownMenuLabel className="p-0 font-normal">
                <div className="flex items-center gap-2 px-1 py-1.5 text-left text-sm">
                  <Avatar className="h-8 w-8 rounded-lg">
                    <AvatarImage src={user.sigla} alt={user.nome} />
                    <AvatarFallback className="rounded-lg">{user.sigla}</AvatarFallback>
                  </Avatar>

                  <div className="grid flex-1 text-left text-sm leading-tight">
                    <span className="truncate font-medium">{user.nome}</span>
                    <span className="truncate text-xs">{user.email}</span>
                  </div>
                </div>
              </DropdownMenuLabel>

              <DropdownMenuSeparator />

              <DropdownMenuGroup>
                {/* Alternância de tema */}
                <DropdownMenuItem className="cursor-pointer" onClick={handleToggleTheme}>
                  {isDark ? <Sun className="mr-2 h-4 w-4" /> : <Moon className="mr-2 h-4 w-4" />}
                  {isDark ? 'Modo claro' : 'Modo escuro'}
                </DropdownMenuItem>

                <DropdownMenuItem className="cursor-pointer">
                  <Sparkles className="mr-2 h-4 w-4" />
                  Configurações
                </DropdownMenuItem>
              </DropdownMenuGroup>

              <DropdownMenuSeparator />

              <DropdownMenuItem className="cursor-pointer" onClick={handleConfirmOpen}>
                <LogOut className="mr-2 h-4 w-4" />
                Log out
              </DropdownMenuItem>
            </DropdownMenuContent>
          </DropdownMenu>
        </SidebarMenuItem>
      </SidebarMenu>

      {/* Modal de confirmação */}
      <ConfirmDialog
        isOpen={isConfirmOpen}
        title="Log-out"
        description="Atenção"
        message="Deseja realmente encerrar a sessão? Dados não salvos serão perdidos."
        confirmText="Sim, sair"
        cancelText="Cancelar"
        onConfirm={handleLogoutConfirm}
        onCancel={handleLogoutCancel}
      />
    </>
  );
}
