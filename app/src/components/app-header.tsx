'use client';

import { BellIcon, LogOut, SearchIcon, UserIcon } from 'lucide-react';
import Link from 'next/link';
import * as React from 'react';
import { usePathname, useRouter } from 'next/navigation';

import { APP_NAV_MAIN_ITEMS, type AppNavMainItem } from '@/components/app-nav-main-data';
import { ModeToggle } from '@/components/mode-toggle';
import { Avatar, AvatarFallback } from '@/components/ui/avatar';
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from '@/components/ui/breadcrumb';
import { Button } from '@/components/ui/button';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Input } from '@/components/ui/input';
import { Separator } from '@/components/ui/separator';
import { SidebarTrigger } from '@/components/ui/sidebar';
import { cn } from '@/lib/utils';
import { GUsuarioProfileDialog } from '@/packages/administrativo/components/GUsuario/GUsuarioProfileDialog';
import { useGUsuarioLogoutHook } from '@/packages/administrativo/hooks/GUsuario/useGUsuarioLogoutHook';

type SearchablePage = {
  title: string;
  href: string;
  section?: string;
  searchableLabel: string;
};

function normalizeSearch(value: string) {
  return value
    .normalize('NFD')
    .replace(/[\u0300-\u036f]/g, '')
    .toLowerCase()
    .trim();
}

function isGroupNavItem(
  item: AppNavMainItem,
): item is AppNavMainItem & { items: NonNullable<AppNavMainItem['items']> } {
  return Boolean(item.items && item.items.length > 0);
}

function formatSegmentLabel(segment: string) {
  const decoded = decodeURIComponent(segment.replace(/\+/g, ' '));
  if (!decoded) return decoded;
  return decoded.charAt(0).toUpperCase() + decoded.slice(1);
}

export function AppHeader({ className }: { className?: string }) {
  const router = useRouter();
  const pathname = usePathname() ?? '/';
  const paths = pathname.split('/').filter(Boolean);

  const { logoutUsuario } = useGUsuarioLogoutHook();

  const [searchValue, setSearchValue] = React.useState('');
  const [isSearchOpen, setIsSearchOpen] = React.useState(false);
  const [profileDialogOpen, setProfileDialogOpen] = React.useState(false);
  const [userMenuOpen, setUserMenuOpen] = React.useState(false);

  const menuCloseTimerRef = React.useRef<number | null>(null);

  const cancelMenuClose = React.useCallback(() => {
    if (menuCloseTimerRef.current !== null) {
      window.clearTimeout(menuCloseTimerRef.current);
      menuCloseTimerRef.current = null;
    }
  }, []);

  const scheduleMenuClose = React.useCallback(() => {
    cancelMenuClose();
    menuCloseTimerRef.current = window.setTimeout(() => {
      setUserMenuOpen(false);
      menuCloseTimerRef.current = null;
    }, 140);
  }, [cancelMenuClose]);

  React.useEffect(() => () => cancelMenuClose(), [cancelMenuClose]);

  const searchablePages = React.useMemo<SearchablePage[]>(() => {
    return APP_NAV_MAIN_ITEMS.flatMap((item) => {
      if (isGroupNavItem(item)) {
        return item.items.map((subItem) => ({
          title: subItem.title,
          href: subItem.url,
          section: item.title,
          searchableLabel: `${item.title} ${subItem.title}`,
        }));
      }

      return [
        {
          title: item.title,
          href: item.url,
          searchableLabel: item.title,
        },
      ];
    });
  }, []);

  const filteredPages = React.useMemo(() => {
    const normalizedTerm = normalizeSearch(searchValue);

    if (!normalizedTerm) {
      return searchablePages.slice(0, 8);
    }

    return searchablePages
      .map((page) => {
        const normalizedTitle = normalizeSearch(page.title);
        const normalizedSection = normalizeSearch(page.section ?? '');
        const normalizedHref = normalizeSearch(page.href.replaceAll('/', ' '));
        const score =
          (normalizedTitle.startsWith(normalizedTerm) ? 4 : 0) +
          (normalizedTitle.includes(normalizedTerm) ? 3 : 0) +
          (normalizedSection.includes(normalizedTerm) ? 2 : 0) +
          (normalizedHref.includes(normalizedTerm) ? 1 : 0);

        return { page, score };
      })
      .filter((result) => result.score > 0)
      .sort((a, b) => b.score - a.score || a.page.title.localeCompare(b.page.title))
      .slice(0, 8)
      .map((result) => result.page);
  }, [searchValue, searchablePages]);

  const navigateToPage = React.useCallback(
    (href: string) => {
      setSearchValue('');
      setIsSearchOpen(false);
      router.push(href);
    },
    [router],
  );

  React.useEffect(() => {
    setSearchValue('');
    setIsSearchOpen(false);
  }, [pathname]);

  return (
    <header
      className={cn(
        'bg-background mb-4 flex h-16 shrink-0 items-center gap-4 border-b px-4 transition-[width,height] ease-linear sm:px-6 lg:px-8 group-has-data-[collapsible=icon]/sidebar-wrapper:h-12',
        className,
      )}
    >
      <SidebarTrigger className="-ml-2 shrink-0" />
      <Separator orientation="vertical" className="hidden h-4 sm:block" />

      <Breadcrumb className="hidden min-w-0 md:flex">
        <BreadcrumbList className="flex-nowrap">
          <BreadcrumbItem>
            <BreadcrumbLink asChild>
              <Link href="/">Home</Link>
            </BreadcrumbLink>
          </BreadcrumbItem>
          {paths.map((segment, index) => {
            const href = `/${paths.slice(0, index + 1).join('/')}`;
            const isLast = index === paths.length - 1;
            const title = formatSegmentLabel(segment);

            return (
              <React.Fragment key={href}>
                <BreadcrumbSeparator />
                <BreadcrumbItem>
                  {isLast ? (
                    <BreadcrumbPage className="max-w-[12rem] truncate sm:max-w-xs">{title}</BreadcrumbPage>
                  ) : (
                    <BreadcrumbLink asChild>
                      <Link href={href} className="max-w-[10rem] truncate">
                        {title}
                      </Link>
                    </BreadcrumbLink>
                  )}
                </BreadcrumbItem>
              </React.Fragment>
            );
          })}
        </BreadcrumbList>
      </Breadcrumb>

      <div className="flex min-w-0 flex-1 items-center justify-end gap-4">
        <div className="relative hidden w-full max-w-sm lg:flex">
          <SearchIcon className="text-muted-foreground absolute top-2.5 left-2.5 size-4" aria-hidden />
          <Input
            type="search"
            placeholder="Buscar página..."
            className="bg-background w-full pl-8 shadow-none"
            value={searchValue}
            onFocus={() => setIsSearchOpen(true)}
            onBlur={() => {
              window.setTimeout(() => setIsSearchOpen(false), 120);
            }}
            onChange={(event) => setSearchValue(event.target.value)}
            onKeyDown={(event) => {
              if (event.key !== 'Enter' || filteredPages.length === 0) {
                return;
              }

              event.preventDefault();
              navigateToPage(filteredPages[0].href);
            }}
          />
          {isSearchOpen && filteredPages.length > 0 && (
            <div className="bg-popover absolute top-full right-0 left-0 z-50 mt-2 rounded-md border shadow-md">
              <ul className="max-h-72 overflow-auto py-1" role="listbox">
                {filteredPages.map((page) => (
                  <li key={`${page.href}-${page.title}`} role="option">
                    <button
                      type="button"
                      className="hover:bg-accent hover:text-accent-foreground flex w-full items-center justify-between gap-2 px-3 py-2 text-left text-sm"
                      onMouseDown={(event) => event.preventDefault()}
                      onClick={() => navigateToPage(page.href)}
                    >
                      <span className="min-w-0 truncate">{page.title}</span>
                      {page.section ? (
                        <span className="text-muted-foreground shrink-0 text-xs">{page.section}</span>
                      ) : null}
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          )}
        </div>
      </div>

      <div className="flex shrink-0 items-center gap-2 sm:gap-4">
        <ModeToggle />
        <Button type="button" variant="ghost" size="icon" className="relative" aria-label="Notificações">
          <BellIcon className="size-5" />
          <span className="bg-primary absolute top-1.5 right-1.5 size-2 rounded-full" aria-hidden />
        </Button>
        <DropdownMenu modal={false} open={userMenuOpen} onOpenChange={setUserMenuOpen}>
          <DropdownMenuTrigger asChild>
            <Button
              type="button"
              variant="ghost"
              size="icon"
              className="rounded-full"
              aria-label="Menu da conta"
              aria-haspopup="menu"
              onPointerEnter={() => {
                cancelMenuClose();
                setUserMenuOpen(true);
              }}
              onPointerLeave={() => scheduleMenuClose()}
            >
              <Avatar className="size-8">
                <AvatarFallback>
                  <UserIcon className="size-4" aria-hidden />
                </AvatarFallback>
              </Avatar>
            </Button>
          </DropdownMenuTrigger>
          <DropdownMenuContent
            align="end"
            sideOffset={6}
            className="w-52"
            onPointerEnter={cancelMenuClose}
            onPointerLeave={() => scheduleMenuClose()}
            onCloseAutoFocus={(event) => event.preventDefault()}
          >
            <DropdownMenuItem
              className="cursor-pointer gap-2"
              onSelect={() => {
                setUserMenuOpen(false);
                setProfileDialogOpen(true);
              }}
            >
              <UserIcon className="size-4" />
              Minha conta
            </DropdownMenuItem>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              variant="destructive"
              className="cursor-pointer gap-2"
              onSelect={() => {
                void logoutUsuario();
              }}
            >
              <LogOut className="size-4" />
              Sair
            </DropdownMenuItem>
          </DropdownMenuContent>
        </DropdownMenu>
      </div>

      <GUsuarioProfileDialog open={profileDialogOpen} onOpenChange={setProfileDialogOpen} />
    </header>
  );
}
