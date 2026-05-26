"use client";

import type { ReactNode } from "react";
import { AccordionContent, AccordionItem, AccordionTrigger } from "@/components/ui/accordion";
import { cn } from "@/lib/utils";
import { ptituloSectionCardClassName } from "./form/PTituloFormLayout";

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
        ptituloSectionCardClassName,
        "overflow-hidden p-0 transition-colors",
        isHighlighted && "border-[#FF6B00]",
      )}
    >
      <AccordionTrigger className="border-b border-border/70 px-3 py-2.5 hover:no-underline md:px-4">
        <div className="flex flex-1 flex-col items-start gap-1">
          <div className="flex items-center gap-3">
            <h3 className="text-lg font-semibold tracking-tight text-foreground">{title}</h3>
          </div>
          <p className="text-sm text-muted-foreground">{description}</p>
        </div>
      </AccordionTrigger>

      <AccordionContent className="px-3 py-3 md:px-4 [&_[role=combobox]]:h-9 [&_[role=combobox]]:text-sm [&_input]:h-9 [&_input]:text-sm [&_label]:text-sm [&_label]:font-medium [&_label]:leading-none">
        <div className="grid gap-x-3 gap-y-3 md:grid-cols-2 xl:grid-cols-3">{children}</div>
      </AccordionContent>
    </AccordionItem>
  );
}
