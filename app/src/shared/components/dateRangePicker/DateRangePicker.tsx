"use client";

import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { cn } from "@/lib/utils";
import { CalendarIcon, X } from "lucide-react";
import type { DateRange } from "react-day-picker";
import { formatDateRangeDay } from "./utils/formatDateRangeLabel";

export interface DateRangePickerProps {
  value: DateRange | undefined;
  onChange: (range: DateRange | undefined) => void;
  placeholder?: string;
  clearAriaLabel?: string;
  numberOfMonths?: number;
  showOutsideDays?: boolean;
  disabled?: boolean;
  className?: string;
  triggerClassName?: string;
}

export function DateRangePicker({
  value,
  onChange,
  placeholder = "Selecione o intervalo",
  clearAriaLabel = "Limpar intervalo de datas",
  numberOfMonths = 1,
  showOutsideDays = false,
  disabled,
  className,
  triggerClassName,
}: DateRangePickerProps) {
  return (
    <Popover>
      <div className={cn("relative", className)}>
        <PopoverTrigger asChild>
          <Button
            type="button"
            variant="outline"
            disabled={disabled}
            className={cn(
              "w-full justify-start pr-10 text-left font-normal",
              !value && "text-muted-foreground",
              triggerClassName,
            )}
          >
            <CalendarIcon className="mr-2 h-4 w-4" />
            {value?.from ? (
              value.to ? (
                <>
                  {formatDateRangeDay(value.from)} - {formatDateRangeDay(value.to)}
                </>
              ) : (
                formatDateRangeDay(value.from)
              )
            ) : (
              <span>{placeholder}</span>
            )}
          </Button>
        </PopoverTrigger>
        {value ? (
          <Button
            type="button"
            variant="ghost"
            size="icon"
            className="absolute right-1 top-1 h-7 w-7 text-muted-foreground hover:text-foreground"
            onClick={(event) => {
              event.stopPropagation();
              onChange(undefined);
            }}
            aria-label={clearAriaLabel}
          >
            <X className="h-4 w-4" />
          </Button>
        ) : null}
      </div>
      <PopoverContent
        data-date-range-picker
        className="w-auto border-border/60 p-1.5 shadow-sm"
        align="start"
      >
        <Calendar
          mode="range"
          selected={value}
          onSelect={(range) => onChange(range)}
          numberOfMonths={numberOfMonths}
          showOutsideDays={showOutsideDays}
          className="gap-2 p-1.5 shadow-none"
        />
      </PopoverContent>
    </Popover>
  );
}
