"use client";

import type { ComponentPropsWithoutRef, ReactNode } from "react";
import { cn } from "@/lib/utils";

export const ptituloSectionCardClassName = "rounded-xl border bg-card p-4 shadow-xs md:p-5";
export const ptituloFieldLabelClassName = "text-sm font-medium leading-none text-foreground";
export const ptituloInputClassName = "h-9 rounded-md border-border/70 bg-background text-sm shadow-none";
export const ptituloSelectTriggerClassName = "h-9 rounded-md border-border/70 bg-background text-sm shadow-none";
export const ptituloSearchSelectTriggerClassName =
  "h-9 rounded-md border-border/70 bg-background text-sm font-normal shadow-none hover:bg-muted/40";
export const ptituloDateButtonClassName =
  "h-9 rounded-md border-border/70 bg-background text-sm shadow-none hover:bg-muted/40";
export const ptituloCheckboxRowClassName =
  "flex h-9 items-center gap-2 rounded-md border border-border/70 bg-background px-3 text-sm shadow-none";

export function PTituloSectionCard({
  className,
  children,
  ...props
}: ComponentPropsWithoutRef<"section">) {
  return (
    <section className={cn(ptituloSectionCardClassName, className)} {...props}>
      {children}
    </section>
  );
}

export function PTituloSectionHeader({
  title,
  description,
  actions,
  className,
  titleClassName,
}: {
  title: ReactNode;
  description?: ReactNode;
  actions?: ReactNode;
  className?: string;
  titleClassName?: string;
}) {
  return (
    <div className={cn("flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between", className)}>
      <div className="min-w-0 space-y-1">
        <h3 className={cn("text-base font-semibold tracking-tight text-foreground", titleClassName)}>
          {title}
        </h3>
        {description ? <p className="text-xs text-muted-foreground">{description}</p> : null}
      </div>
      {actions ? <div className="shrink-0">{actions}</div> : null}
    </div>
  );
}

export function PTituloFieldGrid({
  className,
  children,
}: {
  className?: string;
  children: ReactNode;
}) {
  return <div className={cn("grid gap-x-3 gap-y-3 md:grid-cols-3", className)}>{children}</div>;
}

export function PTituloSubsection({
  title,
  description,
  children,
  className,
}: {
  title: ReactNode;
  description?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <section className={cn("border-t border-border/70 pt-3 first:border-t-0 first:pt-0", className)}>
      <PTituloSectionHeader title={title} description={description} titleClassName="text-sm" />
      <div className="mt-2.5">{children}</div>
    </section>
  );
}

export function PTituloSubPanel({
  className,
  children,
  ...props
}: ComponentPropsWithoutRef<"div">) {
  return (
    <div className={cn("rounded-lg border border-border/70 bg-muted/10 p-4", className)} {...props}>
      {children}
    </div>
  );
}
