'use client';

import { CheckCircle2, ChevronRightIcon } from 'lucide-react';

import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card';
import { TabsList, TabsTrigger } from '@/components/ui/tabs';
import { VerticalTabsSidebarInterface } from './interfaces/VerticalTabsSidebarInterface';

const triggerClassName =
  'group w-full justify-between rounded-md border border-border px-4 py-3 text-sm font-medium transition-all hover:bg-accent/50 data-[state=active]:bg-accent/50 data-[state=active]:shadow-sm data-[state=inactive]:opacity-65 hover:data-[state=inactive]:opacity-100 disabled:pointer-events-none disabled:cursor-not-allowed disabled:opacity-40';

const hideScrollbarClass =
  '[scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden';

export default function VerticalTabsSidebar({
  title,
  description,
  items,
}: VerticalTabsSidebarInterface) {
  return (
    <aside className="sticky top-0 min-w-60 lg:min-w-72 self-start">
      <Card className="shadow-sm">
        <CardHeader>
          <CardTitle>{title}</CardTitle>
          <CardDescription>{description}</CardDescription>
        </CardHeader>
        <CardContent>
          <TabsList
            className={`h-auto w-full justify-start flex-col items-stretch gap-2 bg-transparent p-0 ${hideScrollbarClass}`}
          >
            {items.map((item) => (
              <TabsTrigger key={item.value} value={item.value} className={triggerClassName} disabled={item.disabled}>
                <div className="flex items-center gap-2">
                  <span>{item.label}</span>
                  {item.completed ? <CheckCircle2 className="size-4 text-emerald-600" /> : null}
                </div>
                <ChevronRightIcon className="size-4 opacity-70 transition-opacity group-hover:opacity-100 group-data-[state=active]:opacity-100" />
              </TabsTrigger>
            ))}
          </TabsList>
        </CardContent>
      </Card>
    </aside>
  );
}
