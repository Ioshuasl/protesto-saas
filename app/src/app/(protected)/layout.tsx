import { AppHeader } from '@/components/app-header';
import { AppSidebar } from '@/components/app-sidebar';
import { SidebarInset, SidebarProvider } from '@/components/ui/sidebar';
import { Toaster } from '@/components/ui/sonner';
import { AtendimentoOnlineHelpButton } from '@/shared/components/atendimentoOnline/AtendimentoOnlineHelpButton';
import Response from '@/shared/components/response/response';
import { ResponseProvider } from '@/shared/components/response/ResponseContext';

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return (
    <SidebarProvider>
      <AppSidebar />
      <SidebarInset>
        <ResponseProvider>
          <AppHeader />
          <div className="flex flex-1 flex-col overflow-auto px-4 py-4 sm:px-6 lg:px-8 lg:py-6">
            <div className="mx-auto flex w-full max-w-screen-2xl flex-1 flex-col gap-4">
              {children}
              <Toaster richColors position="top-center" />
              <Response />
            </div>
          </div>
          <AtendimentoOnlineHelpButton />
        </ResponseProvider>
      </SidebarInset>
    </SidebarProvider>
  );
}
