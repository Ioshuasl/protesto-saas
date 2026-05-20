"use client";

import { Button } from "@/components/ui/button";
import { isPTituloMockDataEnabled } from "@/packages/administrativo/data/PTitulo/ptituloDataConfig";
import { usePTituloCancelamentoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloCancelamentoHook";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import { useState } from "react";

export function PTituloCancelamentoButton({ id, onSuccess }: { id: number; onSuccess: (titulo: TituloListItem) => void }) {
  const { cancelarTitulo } = usePTituloCancelamentoHook();
  const [isLoading, setIsLoading] = useState(false);

  return (
    <Button
      variant="destructive"
      type="button"
      disabled={isLoading}
      className="h-9 rounded-md border px-3 text-sm font-medium shadow-none transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] md:h-10 md:px-4"
      onClick={async () => {
        setIsLoading(true);
        try {
          if (isPTituloMockDataEnabled()) {
            window.alert('Protótipo: confirmar "Cancelar Título"');
          }
          const response = await cancelarTitulo(id);
          if (response && typeof response === "object" && "titulo_id" in response) {
            onSuccess(response as TituloListItem);
          }
        } finally {
          setIsLoading(false);
        }
      }}
    >
      Cancelar Título
    </Button>
  );
}
