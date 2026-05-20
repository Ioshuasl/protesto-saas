"use client";

import { Button } from "@/components/ui/button";
import { isPTituloMockDataEnabled } from "@/packages/administrativo/data/PTitulo/ptituloDataConfig";
import { usePTituloVoltarProtestoHook } from "@/packages/administrativo/hooks/PTitulo/usePTituloVoltarProtestoHook";
import type { TituloListItem } from "@/packages/administrativo/interfaces/PTitulo/PTituloListItem";
import { useState } from "react";

export function PTituloVoltarProtestoButton({ id, onSuccess }: { id: number; onSuccess: (titulo: TituloListItem) => void }) {
  const { voltarParaProtesto } = usePTituloVoltarProtestoHook();
  const [isLoading, setIsLoading] = useState(false);

  return (
    <Button
      variant="outline"
      type="button"
      disabled={isLoading}
      className="h-9 rounded-md border bg-muted px-3 text-sm font-medium shadow-none transition-transform duration-200 hover:-translate-y-0.5 hover:scale-[1.01] hover:bg-muted/80 md:h-10 md:px-4"
      onClick={async () => {
        setIsLoading(true);
        try {
          if (isPTituloMockDataEnabled()) {
            window.alert('Protótipo: confirmar "Voltar para Protesto"');
          }
          const response = await voltarParaProtesto(id);
          if (response && typeof response === "object" && "titulo_id" in response) {
            onSuccess(response as TituloListItem);
          }
        } finally {
          setIsLoading(false);
        }
      }}
    >
      Voltar para Protesto
    </Button>
  );
}
