"use client";

import { Badge } from "@/components/ui/badge";

interface PTituloStatusBadgeProps {
  status?: string;
}

export function PTituloStatusBadge({ status }: PTituloStatusBadgeProps) {
  const normalizedStatus = (status ?? "").toLowerCase();

  const className =
    normalizedStatus.includes("tríduo") ||
    normalizedStatus.includes("triduo") ||
    normalizedStatus.includes("apont")
      ? "bg-[#FF6B00] text-white"
      : normalizedStatus.includes("liquid") || normalizedStatus.includes("pago")
        ? "bg-green-600 text-white"
        : normalizedStatus.includes("protest")
          ? "bg-red-600 text-white"
          : normalizedStatus.includes("desist") || normalizedStatus.includes("cancel")
            ? "bg-gray-500 text-white"
            : "bg-muted text-muted-foreground";

  return <Badge className={className}>{status ?? "Sem status"}</Badge>;
}
