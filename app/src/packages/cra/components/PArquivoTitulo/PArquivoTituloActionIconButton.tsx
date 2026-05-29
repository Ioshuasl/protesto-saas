"use client";

import type { MouseEvent, ReactNode } from "react";
import { Button } from "@/components/ui/button";
import { cn } from "@/lib/utils";

export function PArquivoTituloActionIconButton({
  label,
  onClick,
  className,
  disabled,
  children,
}: {
  label: string;
  onClick: (event: MouseEvent<HTMLButtonElement>) => void;
  className?: string;
  disabled?: boolean;
  children: ReactNode;
}) {
  return (
    <Button
      type="button"
      variant="ghost"
      size="sm"
      className={cn(
        "h-8 shrink-0 gap-1.5 px-2 text-xs font-normal text-muted-foreground hover:text-foreground",
        className,
      )}
      onClick={onClick}
      disabled={disabled}
    >
      <span className="inline-flex shrink-0 items-center justify-center [&_svg]:h-3.5 [&_svg]:w-3.5">
        {children}
      </span>
      <span className="whitespace-nowrap leading-none">{label}</span>
    </Button>
  );
}
