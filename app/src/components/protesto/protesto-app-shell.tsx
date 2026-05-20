"use client";

import * as React from "react";
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { ProtestoSidebar } from "@/components/protesto/protesto-sidebar";
import { protestoNavItems } from "@/components/protesto/protesto-sidebar";
import type { ProtestoNavItem } from "@/components/protesto/protesto-sidebar";
import { ModeToggle } from "@/components/mode-toggle";
import { Input } from "@/components/ui/input";
import { Search, Bell, User } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Avatar, AvatarFallback, AvatarImage } from "@/components/ui/avatar";
import {
  Breadcrumb,
  BreadcrumbItem,
  BreadcrumbLink,
  BreadcrumbList,
  BreadcrumbPage,
  BreadcrumbSeparator,
} from "@/components/ui/breadcrumb";
import { Separator } from "@/components/ui/separator";
import { SidebarProvider, SidebarTrigger } from "@/components/ui/sidebar";
import { ResponseProvider } from "@/shared/components/response/ResponseContext";
import Response from "@/shared/components/response/response";

type SearchablePage = {
  title: string;
  href: string;
  section?: string;
  searchableLabel: string;
};

function normalizeSearch(value: string) {
  return value
    .normalize("NFD")
    .replace(/[\u0300-\u036f]/g, "")
    .toLowerCase()
    .trim();
}

function isGroupNavItem(item: ProtestoNavItem): item is Extract<ProtestoNavItem, { items: unknown }> {
  return "items" in item;
}

export function ProtestoAppShell({ children }: { children: React.ReactNode }) {
  const router = useRouter();
  const pathname = usePathname() ?? "/";
  const paths = pathname.split("/").filter(Boolean);
  const [searchValue, setSearchValue] = React.useState("");
  const [isSearchOpen, setIsSearchOpen] = React.useState(false);

  const searchablePages = React.useMemo<SearchablePage[]>(() => {
    return protestoNavItems.flatMap((item) => {
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
        const normalizedSection = normalizeSearch(page.section ?? "");
        const normalizedHref = normalizeSearch(page.href.replaceAll("/", " "));
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
      setSearchValue("");
      setIsSearchOpen(false);
      router.push(href);
    },
    [router],
  );

  React.useEffect(() => {
    setSearchValue("");
    setIsSearchOpen(false);
  }, [pathname]);

  return (
    <ResponseProvider>
    <SidebarProvider>
      <div className="bg-background flex min-h-screen w-full">
        <ProtestoSidebar />
        <div className="flex min-w-0 flex-1 flex-col">
          <header className="bg-background flex h-16 shrink-0 items-center gap-4 border-b px-4 sm:px-6 lg:px-8">
            <SidebarTrigger className="-ml-2" />
            <Separator orientation="vertical" className="mr-2 h-4" />
            <Breadcrumb className="hidden md:flex">
              <BreadcrumbList>
                <BreadcrumbItem>
                  <BreadcrumbLink asChild>
                    <Link href="/">Home</Link>
                  </BreadcrumbLink>
                </BreadcrumbItem>
                {paths.map((segment, index) => {
                  const href = `/${paths.slice(0, index + 1).join("/")}`;
                  const isLast = index === paths.length - 1;
                  const title = segment.charAt(0).toUpperCase() + segment.slice(1);
                  return (
                    <React.Fragment key={href}>
                      <BreadcrumbSeparator />
                      <BreadcrumbItem>
                        {isLast ? (
                          <BreadcrumbPage>{title}</BreadcrumbPage>
                        ) : (
                          <BreadcrumbLink asChild>
                            <Link href={href}>{title}</Link>
                          </BreadcrumbLink>
                        )}
                      </BreadcrumbItem>
                    </React.Fragment>
                  );
                })}
              </BreadcrumbList>
            </Breadcrumb>
            <div className="flex flex-1 items-center justify-end gap-4">
              <div className="relative hidden w-full max-w-sm lg:flex">
                <Search className="text-muted-foreground absolute top-2.5 left-2.5 h-4 w-4" />
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
                    if (event.key !== "Enter" || filteredPages.length === 0) {
                      return;
                    }

                    event.preventDefault();
                    navigateToPage(filteredPages[0].href);
                  }}
                />
                {isSearchOpen && filteredPages.length > 0 && (
                  <div className="bg-popover absolute top-full right-0 left-0 z-50 mt-2 rounded-md border shadow-md">
                    <ul className="max-h-72 overflow-auto py-1">
                      {filteredPages.map((page) => (
                        <li key={page.href}>
                          <button
                            type="button"
                            className="hover:bg-accent hover:text-accent-foreground flex w-full items-center justify-between px-3 py-2 text-left text-sm"
                            onMouseDown={(event) => event.preventDefault()}
                            onClick={() => navigateToPage(page.href)}
                          >
                            <span>{page.title}</span>
                            <span className="text-muted-foreground text-xs">{page.section ?? page.href}</span>
                          </button>
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            </div>
            <div className="flex items-center gap-4">
              <ModeToggle />
              <Button variant="ghost" size="icon" className="relative">
                <Bell className="h-5 w-5" />
                <span className="bg-primary absolute top-1.5 right-1.5 h-2 w-2 rounded-full" />
              </Button>
              <Avatar className="h-8 w-8 cursor-pointer">
                <AvatarImage src="https://github.com/shadcn.png" alt="Usuário" />
                <AvatarFallback>
                  <User className="h-4 w-4" />
                </AvatarFallback>
              </Avatar>
            </div>
          </header>
          <main className="flex-1 overflow-auto px-4 py-4 sm:px-6 lg:px-8 lg:py-6">
            <div className="mx-auto w-full max-w-screen-2xl">{children}</div>
          </main>
        </div>
      </div>
      <Response />
    </SidebarProvider>
    </ResponseProvider>
  );
}
