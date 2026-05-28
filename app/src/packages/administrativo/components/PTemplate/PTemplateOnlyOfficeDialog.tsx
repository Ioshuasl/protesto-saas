"use client";

import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import OnlyOfficeEditor from "@/shared/components/editor/onlyoffice/OnlyOfficeEditor";
import type { PTemplateInterface } from "@/packages/administrativo/interfaces/PTemplate/PTemplateInterface";
import type { PTemplateOnlyOfficeConfig } from "@/packages/administrativo/interfaces/PTemplate/PTemplateOnlyOfficeConfig";
import { toast } from "sonner";

interface PTemplateOnlyOfficeDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  template: PTemplateInterface | null;
  config: PTemplateOnlyOfficeConfig | null;
  isLoading?: boolean;
}

export function PTemplateOnlyOfficeDialog({
  open,
  onOpenChange,
  template,
  config,
  isLoading,
}: PTemplateOnlyOfficeDialogProps) {
  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="h-[92vh] w-[99vw] max-w-[1800px] p-0 sm:max-w-[1800px]">
        <DialogHeader className="border-b px-6 py-4">
          <DialogTitle>
            Editor de Minuta
            {template ? ` - #${template.template_id}` : ""}
          </DialogTitle>
        </DialogHeader>

        <div className="h-[calc(92vh-72px)] w-full">
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

