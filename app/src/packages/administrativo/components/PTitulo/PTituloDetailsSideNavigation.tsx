"use client";

import { cn } from "@/lib/utils";
import {
  BellRing,
  BookOpenCheck,
  ChevronRight,
  CircleDollarSign,
  ClipboardList,
  DatabaseZap,
  Globe2,
  SearchCheck,
  type LucideIcon,
} from "lucide-react";
import { PTituloSectionCard } from "./form/PTituloFormLayout";
import type { PTituloOperationalSectionId } from "./PTituloDetailsSection";

const operationalNavigationItems = [
  { id: "apontamento", title: "Apontamento", icon: ClipboardList },
  { id: "intimacao-aceite", title: "Intimação & Aceite", icon: BellRing },
  { id: "protesto", title: "Protesto", icon: BookOpenCheck },
  { id: "cancelamento-pagamento", title: "Cancelamento & Pagamento", icon: CircleDollarSign },
  { id: "cra", title: "CRA", icon: DatabaseZap },
  { id: "cenprot", title: "CENPROT", icon: Globe2 },
  { id: "serasa", title: "SERASA", icon: SearchCheck },
] satisfies ReadonlyArray<{
  id: PTituloOperationalSectionId;
  title: string;
  icon: LucideIcon;
}>;

interface PTituloDetailsSideNavigationProps {
  activeSection: PTituloOperationalSectionId;
  onNavigate: (sectionId: PTituloOperationalSectionId) => void;
}

export function PTituloDetailsSideNavigation({
  activeSection,
  onNavigate,
}: PTituloDetailsSideNavigationProps) {
  return (
    <aside className="h-fit lg:sticky lg:top-24 lg:z-10 lg:max-h-[calc(100dvh-7rem)] lg:self-start lg:overflow-y-auto">
      <PTituloSectionCard className="overflow-hidden p-0">
        <div className="border-b border-border/70 px-3 py-2.5">
          <h3 className="text-sm font-semibold tracking-tight text-foreground">Navegação</h3>
          <p className="mt-1 text-xs text-muted-foreground">Acesse rapidamente cada etapa.</p>
        </div>
        <nav className="space-y-1 p-2" aria-label="Navegação dos detalhes do título">
          {operationalNavigationItems.map((item) => {
            const Icon = item.icon;
            const isActive = activeSection === item.id;

            return (
              <button
                key={item.id}
                type="button"
                onClick={() => onNavigate(item.id)}
                className={cn(
                  "flex w-full items-center gap-2 rounded-md px-2.5 py-2 text-left text-sm transition-colors",
                  "hover:bg-muted/60 focus-visible:ring-ring/50 focus-visible:ring-2 focus-visible:outline-none",
                  isActive
                    ? "bg-[#FF6B00]/10 font-medium text-[#FF6B00]"
                    : "text-muted-foreground hover:text-foreground",
                )}
                aria-current={isActive ? "page" : undefined}
              >
                <Icon className="h-4 w-4 shrink-0" strokeWidth={1.75} />
                <span className="min-w-0 flex-1 truncate">{item.title}</span>
                <ChevronRight
                  className={cn("h-4 w-4 shrink-0 transition-transform", isActive && "translate-x-0.5")}
                  strokeWidth={1.75}
                />
              </button>
            );
          })}
        </nav>
      </PTituloSectionCard>
    </aside>
  );
}
