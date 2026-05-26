"use client";

import { CircleQuestionMark, Loader2 } from "lucide-react";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";

import { Button } from "@/components/ui/button";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";
import { PCERTIDAO_TIPO_INFO_MARKDOWN } from "@/packages/certidao/components/PCertidao/PCertidaoForm";
import type { PCertidaoFormValues } from "@/packages/certidao/components/PCertidao/PCertidaoFormValues";
import { PCertidaoEmissaoForm } from "@/packages/certidao/components/PCertidao/PCertidaoEmissaoForm";
import { usePCertidaoSaveHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoSaveHook";
import { isPCertidaoSaveResult } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";

export default function PCertidaoEmissaoPage() {
  const router = useRouter();
  const { isLoading: isLoadingUsuarios, fetchUsuarios } = useGUsuarioReadHook();
  const { isSaving, saveCertidao } = usePCertidaoSaveHook();
  const [tipoInfoOpen, setTipoInfoOpen] = useState(false);

  useEffect(() => {
    void fetchUsuarios();
  }, [fetchUsuarios]);

  const handleEmit = async (payload: PCertidaoFormValues) => {
    const response = await saveCertidao(payload);
    if (isPCertidaoSaveResult(response)) {
      router.push("/certidao");
    }
  };

  return (
    <div className="flex w-full min-w-0 flex-col gap-4">
      <section className="rounded-xl border bg-card p-4 shadow-xs">
        <div className="flex min-w-0 flex-col gap-3 md:flex-row md:items-start md:justify-between">
          <div className="min-w-0 space-y-1">
            <div className="flex items-center gap-2">
              <h1 className="text-2xl font-bold tracking-tight md:text-3xl">Emitir Nova Certidão</h1>
              <Button
                type="button"
                variant="ghost"
                size="icon-sm"
                onClick={() => setTipoInfoOpen(true)}
                aria-label="Informações sobre tipos de certidão"
              >
                <CircleQuestionMark className="h-4 w-4" />
              </Button>
            </div>
            <p className="max-w-3xl text-sm text-muted-foreground">
              Consulte registros ativos no período, revise o tipo derivado e a homonímia quando aplicável.
            </p>
          </div>
          <Button
            type="button"
            variant="outline"
            size="sm"
            className="w-fit"
            onClick={() => router.push("/certidao")}
            disabled={isSaving}
          >
            Voltar
          </Button>
        </div>
      </section>

      <section className="rounded-xl border bg-card p-4 shadow-xs">
        {isLoadingUsuarios ? (
          <div className="flex min-h-[220px] flex-col items-center justify-center gap-3 text-muted-foreground">
            <Loader2 className="h-5 w-5 animate-spin" />
            <p className="text-sm">Carregando usuarios...</p>
          </div>
        ) : (
          <PCertidaoEmissaoForm
            open
            isLoadingUsuarios={isLoadingUsuarios}
            onEmit={handleEmit}
            onCancel={() => router.push("/certidao")}
            isSaving={isSaving}
          />
        )}
      </section>

      <InfoDialog
        isOpen={tipoInfoOpen}
        onOpenChange={setTipoInfoOpen}
        title="Tipos de certidão"
        description="Diferença entre certidão negativa e positiva"
        content={PCERTIDAO_TIPO_INFO_MARKDOWN}
      />
    </div>
  );
}
