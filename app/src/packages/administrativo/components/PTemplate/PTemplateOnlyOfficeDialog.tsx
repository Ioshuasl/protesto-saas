"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import OnlyOfficeEditor from "@/shared/components/editor/onlyoffice/OnlyOfficeEditor";
import type { PTemplateInterface } from "@/packages/administrativo/interfaces/PTemplate/PTemplateInterface";
import type { PTemplateMarkerLegend } from "@/packages/administrativo/interfaces/PTemplate/PTemplateMarkerLegend";
import type { PTemplateOnlyOfficeConfig } from "@/packages/administrativo/interfaces/PTemplate/PTemplateOnlyOfficeConfig";
import { toast } from "sonner";

const LEGEND_SWATCH: Record<string, string> = {
  amarelo: "bg-yellow-200",
  verde: "bg-green-200",
  turquesa: "bg-cyan-200",
};

interface PTemplateOnlyOfficeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  template: PTemplateInterface | null;
  config: PTemplateOnlyOfficeConfig | null;
  markerLegend?: PTemplateMarkerLegend | null;
  isLoading?: boolean;
}

export function PTemplateOnlyOfficeDialog({
  open,
  onOpenChange,
  template,
  config,
  markerLegend,
  isLoading,
}: PTemplateOnlyOfficeDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="h-[92vh] w-[calc(100%-2rem)] max-w-6xl gap-0 p-0 sm:max-w-6xl">
        <DialogHeader className="space-y-3 border-b px-6 py-4">
          <DialogTitle>
            Editor de Minuta
            {template?.descricao?.trim()
              ? ` - ${template.descricao.trim()}`
              : template
                ? ` - #${template.template_id}`
                : ""}
          </DialogTitle>
          {markerLegend ? (
            <div className="flex flex-wrap gap-3 text-xs text-muted-foreground">
              {[markerLegend.manual, markerLegend.automatic, markerLegend.variable].map(
                (item) => (
                  <span
                    key={item.tag}
                    className="inline-flex items-center gap-1.5 rounded-md border px-2 py-1"
                  >
                    <span
                      className={`h-3 w-6 rounded ${LEGEND_SWATCH[item.color] ?? "bg-muted"}`}
                      aria-hidden
                    />
                    <span className="font-mono">{item.tag}</span>
                    <span>{item.label}</span>
                  </span>
                ),
              )}
            </div>
          ) : null}
        </DialogHeader>

        <div className="h-[calc(92vh-120px)] w-full">
          {isLoading ? (
            <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
              Carregando editor...
            </div>
          ) : config ? (
            <OnlyOfficeEditor
              id={`p-template-${template?.template_id ?? "novo"}`}
              config={config}
              onDocumentError={() => {
                toast("Falha ao salvar minuta", {
                  description:
                    "O OnlyOffice não conseguiu persistir a alteração. Verifique a conexão e tente salvar novamente.",
                });
              }}
            />
          ) : (
            <div className="flex h-full items-center justify-center text-sm text-muted-foreground">
              Não foi possível carregar o editor para esta minuta.
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  );
}

