"use client";

import { CheckIcon, ChevronsUpDownIcon, XIcon } from "lucide-react";
import { useMemo, useState } from "react";
import { Button } from "@/components/ui/button";
import {
  Command,
  CommandEmpty,
  CommandGroup,
  CommandInput,
  CommandItem,
  CommandList,
} from "@/components/ui/command";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { comboboxSearchFilter } from "@/shared/actions/text/comboboxSearchFilter";
import { LIST_MAX_HEIGHT_CLASS } from "@/shared/const";
import { cn } from "@/lib/utils";

export type SearchComboboxOption = {
  value: string;
  label: string;
  /** Texto indexado para busca; padrão: label + value. */
  searchValue?: string;
};

export interface SearchComboboxSelectProps {
  value?: string;
  onValueChange?: (value: string) => void;
  options: SearchComboboxOption[];
  isLoading?: boolean;
  placeholder?: string;
  searchPlaceholder?: string;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
  contentClassName?: string;
  emptyMessage?: string;
  loadingMessage?: string;
  clearable?: boolean;
  clearAriaLabel?: string;
}

export function SearchComboboxSelect({
  value,
  onValueChange,
  options,
  isLoading = false,
  placeholder = "Selecione",
  searchPlaceholder = "Buscar...",
  disabled = false,
  className,
  triggerClassName,
  contentClassName,
  emptyMessage = "Nenhum registro disponível",
  loadingMessage = "Carregando...",
  clearable = true,
  clearAriaLabel = "Limpar seleção",
}: SearchComboboxSelectProps) {
  const [open, setOpen] = useState(false);

  const normalizedValue = value?.trim() ?? "";

  const selected = useMemo(
    () => options.find((option) => option.value === normalizedValue) ?? null,
    [options, normalizedValue],
  );

  const isDisabled = disabled || (isLoading && options.length === 0);

  const triggerLabel = useMemo(() => {
    if (isLoading && options.length === 0) return loadingMessage;
    if (selected) return selected.label;
    return placeholder;
  }, [isLoading, loadingMessage, options.length, selected, placeholder]);

  const emptyListMessage = useMemo(() => {
    if (isLoading) return loadingMessage;
    return emptyMessage;
  }, [isLoading, loadingMessage, emptyMessage]);

  function handleSelect(nextValue: string) {
    if (isDisabled) return;
    onValueChange?.(nextValue);
    setOpen(false);
  }

  function handleClear(event: React.MouseEvent<HTMLButtonElement>) {
    event.stopPropagation();
    event.preventDefault();
    if (isDisabled) return;
    onValueChange?.("");
    setOpen(false);
  }

  const hasValue = Boolean(normalizedValue);
  const showClear = clearable && hasValue && !isDisabled;

  return (
    <div className={cn("relative w-full", className)}>
      <Popover
        open={isDisabled ? false : open}
        onOpenChange={(nextOpen) => {
          if (isDisabled) return;
          setOpen(nextOpen);
        }}
      >
        <PopoverTrigger asChild>
          <Button
            type="button"
            variant="outline"
            role="combobox"
            aria-expanded={open}
            disabled={isDisabled}
            className={cn(
              "h-9 w-full justify-between font-normal",
              showClear && "pr-14",
              !isDisabled && "cursor-pointer",
              triggerClassName,
            )}
          >
            <span className="truncate">{triggerLabel}</span>
            <ChevronsUpDownIcon className="ml-2 h-4 w-4 shrink-0 opacity-50" />
          </Button>
        </PopoverTrigger>

        <PopoverContent
          className={cn(
            "w-[var(--radix-popover-trigger-width)] max-w-[min(100vw-2rem,32rem)] p-0",
            contentClassName,
          )}
          align="start"
        >
          <Command shouldFilter filter={comboboxSearchFilter}>
            <CommandInput placeholder={searchPlaceholder} disabled={isLoading || disabled} />
            <CommandList className={LIST_MAX_HEIGHT_CLASS}>
              <CommandEmpty>{emptyListMessage}</CommandEmpty>
              <CommandGroup>
                {options.map((option) => (
                  <CommandItem
                    key={option.value}
                    className={cn(!isDisabled && "cursor-pointer")}
                    disabled={isDisabled}
                    value={option.searchValue ?? `${option.label} ${option.value}`}
                    onSelect={() => handleSelect(option.value)}
                    title={option.label}
                  >
                    <CheckIcon
                      className={cn(
                        "mr-2 h-4 w-4 shrink-0",
                        option.value === normalizedValue ? "opacity-100" : "opacity-0",
                      )}
                    />
                    <span className="truncate">{option.label}</span>
                  </CommandItem>
                ))}
              </CommandGroup>
            </CommandList>
          </Command>
        </PopoverContent>
      </Popover>
      {showClear ? (
        <Button
          type="button"
          variant="ghost"
          size="icon"
          className="absolute right-8 top-1/2 h-7 w-7 -translate-y-1/2 text-muted-foreground hover:text-foreground"
          onClick={handleClear}
          aria-label={clearAriaLabel}
        >
          <XIcon className="h-4 w-4" />
        </Button>
      ) : null}
    </div>
  );
}
