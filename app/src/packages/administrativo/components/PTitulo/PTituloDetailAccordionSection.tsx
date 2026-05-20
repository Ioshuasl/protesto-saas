"use client";

import type { ReactNode } from "react";
import { AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { cn } from "@/lib/utils";

interface PTituloDetailAccordionSectionProps {
  sectionKey: string;
  title: string;
  description: string;
  children: ReactNode;
  isHighlighted?: boolean;
}

export function PTituloDetailAccordionSection({
  sectionKey,
  title,
  description,
  children,
  isHighlighted = false,
}: PTituloDetailAccordionSectionProps) {
  return (
    <AccordionItem
      value={sectionKey}
      className={cn(
        "overflow-hidden rounded-xl border bg-card px-4 shadow-xs transition-colors",
        isHighlighted && "border-[#FF6B00]",
      )}
    >
      <AccordionTrigger className="py-4 hover:no-underline">
        <div className="flex flex-1 flex-col items-start gap-1">
          <div className="flex items-center gap-3">
            <h3 className="text-sm font-semibold text-foreground">{title}</h3>
          </div>
          <p className="text-xs text-muted-foreground">{description}</p>
        </div>
      </AccordionTrigger>

      <AccordionContent className="border-t pt-4">
        <div className="grid gap-3 md:grid-cols-2 xl:grid-cols-3">{children}</div>
      </AccordionContent>
    </AccordionItem>
  );
}
