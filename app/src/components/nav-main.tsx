'use client';

import { ChevronRight, type LucideIcon } from 'lucide-react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';

import type { AppNavMainItem } from '@/components/app-nav-main-data';
import { Collapsible, CollapsibleContent, CollapsibleTrigger } from '@/components/ui/collapsible';
import {
  SidebarGroup,
  SidebarGroupLabel,
  SidebarMenu,
  SidebarMenuButton,
  SidebarMenuItem,
  SidebarMenuSub,
  SidebarMenuSubButton,
  SidebarMenuSubItem,
} from '@/components/ui/sidebar';

function isGroupItem(item: AppNavMainItem): item is AppNavMainItem & {
  items: NonNullable<AppNavMainItem['items']>;
} {
  return Boolean(item.items && item.items.length > 0);
}

function isPathActive(pathname: string, href: string) {
  if (href === '/') return pathname === '/';
  return pathname === href || pathname.startsWith(`${href}/`);
}

export function NavMain({ items }: { items: AppNavMainItem[] }) {
  const pathname = usePathname() ?? '/';

  return (
    <SidebarGroup>
      <SidebarGroupLabel>Protesto</SidebarGroupLabel>
      <SidebarMenu>
        {items.map((item) => {
          if (isGroupItem(item)) {
            const groupActive = item.items.some((sub) => isPathActive(pathname, sub.url));

            return (
              <Collapsible
                key={item.title}
                asChild
                defaultOpen={groupActive || item.isActive}
                className="group/collapsible"
              >
                <SidebarMenuItem>
                  <CollapsibleTrigger asChild>
                    <SidebarMenuButton
                      tooltip={item.title}
                      className="data-[state=open]:bg-sidebar-accent data-[state=open]:text-sidebar-accent-foreground"
                    >
                      {item.icon && <item.icon className="h-4 w-4" strokeWidth={1.5} />}
                      <span className="font-medium">{item.title}</span>
                      <ChevronRight className="ml-auto h-4 w-4 transition-transform duration-200 group-data-[state=open]/collapsible:rotate-90" />
                    </SidebarMenuButton>
                  </CollapsibleTrigger>
                  <CollapsibleContent>
                    <SidebarMenuSub>
                      {item.items.map((subItem) => (
                        <SidebarMenuSubItem key={subItem.title}>
                          <SidebarMenuSubButton
                            asChild
                            isActive={isPathActive(pathname, subItem.url)}
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

          return (
            <SidebarMenuItem key={item.title}>
              <SidebarMenuButton
                asChild
                isActive={isPathActive(pathname, item.url)}
                tooltip={item.title}
                className="data-[active=true]:bg-primary/10 data-[active=true]:text-primary"
              >
                <Link href={item.url}>
                  {item.icon && <item.icon className="h-4 w-4" strokeWidth={1.5} />}
                  <span className="font-medium">{item.title}</span>
                </Link>
              </SidebarMenuButton>
            </SidebarMenuItem>
          );
        })}
      </SidebarMenu>
    </SidebarGroup>
  );
}
