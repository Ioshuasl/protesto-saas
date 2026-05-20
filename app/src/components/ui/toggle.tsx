"use client";

import * as SwitchPrimitives from "@radix-ui/react-switch";
import { cva, type VariantProps } from "class-variance-authority";
import * as React from "react";

import { cn } from "@/lib/utils";

const toggleTrackVariants = cva(
  [
    "peer relative inline-flex shrink-0 cursor-pointer items-center rounded-full border border-transparent shadow-inner outline-none transition-colors duration-200 ease-out",
    "focus-visible:ring-[3px] focus-visible:ring-[#FF6B00]/35",
    "disabled:cursor-not-allowed disabled:opacity-50",
    "data-[state=unchecked]:bg-muted dark:data-[state=unchecked]:bg-input/80",
    "data-[state=checked]:border-[#FF6B00]/80 data-[state=checked]:bg-[#FF6B00]",
    "hover:data-[state=checked]:bg-[#E56000]",
  ].join(" "),
  {
    variants: {
      variant: {
        default: "",
        outline:
          "border-input shadow-xs data-[state=unchecked]:border-border/70 data-[state=unchecked]:bg-muted/50 dark:data-[state=unchecked]:bg-input/60",
      },
      size: {
        default: "h-6 min-h-6 w-11 min-w-[2.75rem]",
        sm: "h-[1.25rem] min-h-[1.25rem] w-9 min-w-9",
        lg: "h-7 min-h-7 w-[3.25rem] min-w-[3.25rem]",
      },
    },
    defaultVariants: {
      variant: "default",
      size: "default",
    },
  },
);

const toggleThumbVariants = cva(
  [
    "pointer-events-none absolute top-1/2 block -translate-y-1/2 rounded-full bg-white shadow-md ring-0",
    "transition-[left] duration-200 ease-[cubic-bezier(0.4,0,0.2,1)] will-change-[left]",
    "dark:data-[state=unchecked]:bg-background",
  ].join(" "),
  {
    variants: {
      size: {
        default:
          "left-[3px] size-[1.125rem] data-[state=checked]:left-[calc(100%-1.125rem-3px)]",
        sm: "left-[3px] size-3.5 data-[state=checked]:left-[calc(100%-0.875rem-3px)]",
        lg: "left-[3px] size-[1.375rem] data-[state=checked]:left-[calc(100%-1.375rem-3px)]",
      },
    },
    defaultVariants: {
      size: "default",
    },
  },
);

export type ToggleProps = Omit<
  React.ComponentPropsWithoutRef<typeof SwitchPrimitives.Root>,
  "checked" | "defaultChecked" | "onCheckedChange"
> &
  VariantProps<typeof toggleTrackVariants> & {
    /** API compatível com Radix Toggle: estado ligado/desligado. */
    pressed?: boolean;
    defaultPressed?: boolean;
    onPressedChange?: (pressed: boolean) => void;
    checked?: boolean;
    defaultChecked?: boolean;
    onCheckedChange?: (checked: boolean) => void;
  };

const Toggle = React.forwardRef<React.ElementRef<typeof SwitchPrimitives.Root>, ToggleProps>(
  (
    {
      className,
      variant,
      size,
      pressed,
      defaultPressed,
      onPressedChange,
      checked,
      defaultChecked,
      onCheckedChange,
      ...props
    },
    ref,
  ) => {
    const resolvedChecked = pressed !== undefined ? pressed : checked;
    const resolvedDefault = defaultPressed ?? defaultChecked;

    const handleCheckedChange = React.useCallback(
      (next: boolean) => {
        onPressedChange?.(next);
        onCheckedChange?.(next);
      },
      [onPressedChange, onCheckedChange],
    );

    return (
      <SwitchPrimitives.Root
        ref={ref}
        data-slot="toggle"
        role="switch"
        className={cn(toggleTrackVariants({ variant, size }), className)}
        checked={resolvedChecked}
        defaultChecked={resolvedDefault}
        onCheckedChange={handleCheckedChange}
        {...props}
      >
        <SwitchPrimitives.Thumb
          data-slot="toggle-thumb"
          className={cn(toggleThumbVariants({ size }))}
        />
      </SwitchPrimitives.Root>
    );
  },
);
Toggle.displayName = "Toggle";

/** @deprecated Prefer estilizar via `className` no `Toggle`; mantido para compatível com shadcn. */
const toggleVariants = toggleTrackVariants;

export { Toggle, toggleVariants };
