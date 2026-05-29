"use client";

import { useEffect, useRef, useState } from "react";
import { FileText, Trash2, Upload } from "lucide-react";
import { toast } from "sonner";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";
import { PBancoForm } from "@/packages/administrativo/components/PBanco/PBancoForm";
import type { PBancoInterface } from "@/packages/administrativo/interfaces/PBanco/PBancoInterface";
import type { BancoFormValues } from "@/packages/administrativo/schemas/PBanco/PBancoFormSchema";
import { PBancoSaveCreateService } from "@/packages/administrativo/services/PBanco/PBancoSaveCreateService";
import { PBancoShowByCodigoService } from "@/packages/administrativo/services/PBanco/PBancoShowByCodigoService";
import { parsePBancoRecord } from "@/packages/administrativo/utils/parsePBancoRecord";
import { importCraRemessaFile } from "@/packages/cra/functions/CraImportacao";
import type { CraRemessaImportResult, CraRemessaTransacao } from "@/packages/cra/functions/CraImportacao";
import { useCraImportacaoSaveHook } from "@/packages/cra/hooks/CraImportacao/useCraImportacaoSaveHook";
import { isCraImportacaoSaveResult } from "@/packages/cra/interface/CraImportacao/CraImportacaoSaveInterface";
import ConfirmDialog from "@/shared/components/confirmDialog/ConfirmDialog";
import { LoadingDialog } from "@/shared/components/loading/LoadingDialog";
import { CraImportacaoDetailsModal } from "./CraImportacaoDetailsModal";
import { CraImportacaoSubView } from "./CraImportacaoSubView";

function extractBancoCodeFromFileName(fileName: string): string | null {
  const match = fileName.trim().toUpperCase().match(/^B([A-Z0-9]{3})/);
  return match?.[1] ?? null;
}

type ResolveBancoResult =
  | { status: "found"; banco: PBancoInterface }
  | { status: "not_found" }
  | { status: "error" };

export default function CraImportacaoIndex() {
  const { isSaving, saveCraImportacao } = useCraImportacaoSaveHook();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [detectedBancoCode, setDetectedBancoCode] = useState<string | null>(null);
  const [detectedBanco, setDetectedBanco] = useState<PBancoInterface | null>(null);
  const [isBancoCadastroDialogOpen, setIsBancoCadastroDialogOpen] = useState(false);
  const [isSavingBanco, setIsSavingBanco] = useState(false);
  const [isResolvingBanco, setIsResolvingBanco] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [importResult, setImportResult] = useState<CraRemessaImportResult | null>(null);
  const [isConfirmed, setIsConfirmed] = useState(false);
  const [selectedTransacao, setSelectedTransacao] = useState<CraRemessaTransacao | null>(null);
  const [selectedTransacaoIndex, setSelectedTransacaoIndex] = useState<number | undefined>(undefined);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const [isConfirmImportDialogOpen, setIsConfirmImportDialogOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);
  const dragCounterRef = useRef(0);

  useEffect(() => {
    const preventBrowserDrop = (event: DragEvent) => {
      event.preventDefault();
    };
    window.addEventListener("dragover", preventBrowserDrop);
    window.addEventListener("drop", preventBrowserDrop);
    return () => {
      window.removeEventListener("dragover", preventBrowserDrop);
      window.removeEventListener("drop", preventBrowserDrop);
    };
  }, []);

  const processRemessaFile = async (file: File) => {
    setIsImporting(true);
    setImportResult(null);
    setIsConfirmed(false);

    try {
      const result = await importCraRemessaFile(file);
      setImportResult(result);

      if (!result.ok) {
        toast.error("Arquivo CRA inválido", {
          description: result.errors[0]?.message || "Falha na validação da remessa.",
        });
        return;
      }

      toast.success("Arquivo CRA processado", {
        description: `${result.parsed?.transacoes.length ?? 0} título(s) encontrado(s).`,
      });
    } catch {
      toast.error("Falha ao processar arquivo de remessa");
    } finally {
      setIsImporting(false);
    }
  };

  const resolveBancoByCodigo = async (codigoBanco: string): Promise<ResolveBancoResult> => {
    setIsResolvingBanco(true);
    setDetectedBanco(null);

    try {
      const response = await PBancoShowByCodigoService(codigoBanco);
      const banco = parsePBancoRecord(response);
      if (banco) {
        setDetectedBanco(banco);
        return { status: "found", banco };
      }

      if (
        response &&
        typeof response === "object" &&
        "status" in response &&
        typeof (response as { status?: unknown }).status === "number" &&
        (response as { status: number }).status >= 600
      ) {
        toast.error("Não foi possível consultar o banco", {
          description: "Falha de comunicação com a API ao validar o código do arquivo.",
        });
        return { status: "error" };
      }

      return { status: "not_found" };
    } finally {
      setIsResolvingBanco(false);
    }
  };

  const runPostUploadFlow = async (file: File, codigoBanco: string) => {
    const bancoResult = await resolveBancoByCodigo(codigoBanco);

    if (bancoResult.status === "error") return;

    if (bancoResult.status === "not_found") {
      setIsBancoCadastroDialogOpen(true);
      return;
    }

    await processRemessaFile(file);
  };

  const handleFileSelect = async (file?: File) => {
    if (!file) return;

    const codigoBanco = extractBancoCodeFromFileName(file.name);
    if (!codigoBanco) {
      toast.error("Nome de arquivo inválido", {
        description: 'Esperado formato iniciado por "B" + 3 caracteres alfanuméricos (ex.: B033, B50F).',
      });
      return;
    }

    setSelectedFile(file);
    setDetectedBancoCode(codigoBanco);
    setImportResult(null);
    setIsConfirmed(false);
    setIsBancoCadastroDialogOpen(false);

    await runPostUploadFlow(file, codigoBanco);
  };

  const handleSaveNovoBanco = async (formData: BancoFormValues) => {
    setIsSavingBanco(true);
    try {
      const response = await PBancoSaveCreateService(formData);
      const banco = parsePBancoRecord(response);

      if (!banco) {
        toast.error("Falha ao cadastrar banco", {
          description: (response as { message?: string })?.message || "Não foi possível salvar o banco.",
        });
        return;
      }

      setDetectedBanco(banco);
      setIsBancoCadastroDialogOpen(false);
      toast.success("Banco cadastrado com sucesso");

      if (selectedFile) {
        await processRemessaFile(selectedFile);
      }
    } catch {
      toast.error("Falha ao cadastrar banco");
    } finally {
      setIsSavingBanco(false);
    }
  };

  const handleResetFile = () => {
    setSelectedFile(null);
    setDetectedBancoCode(null);
    setDetectedBanco(null);
    setImportResult(null);
    setIsConfirmed(false);
    setIsBancoCadastroDialogOpen(false);
    setSelectedTransacao(null);
    setSelectedTransacaoIndex(undefined);
    setIsDetailsModalOpen(false);
    setIsConfirmImportDialogOpen(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const formatFileSize = (size: number) => {
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
  };

  const titulosEncontradosCount = importResult?.parsed?.transacoes.length ?? 0;

  const handleConfirmImport = async () => {
    if (!importResult?.ok || !importResult.parsed || !detectedBanco) return;

    setIsConfirmImportDialogOpen(false);

    const response = await saveCraImportacao({
      banco_id: detectedBanco.banco_id,
      remessa: importResult.parsed,
    });

    if (isCraImportacaoSaveResult(response)) {
      setIsConfirmed(true);
      toast.success("Importação confirmada com sucesso", {
        description: `${response.imported_count} título(s) importado(s).`,
      });
      return;
    }

    toast.error("Falha ao confirmar importação", {
      description: (response as { message?: string })?.message || "Erro inesperado ao salvar a remessa.",
    });
  };

  const handleOpenTransacaoDetails = (transacao: CraRemessaTransacao, index: number) => {
    setSelectedTransacao(transacao);
    setSelectedTransacaoIndex(index);
    setIsDetailsModalOpen(true);
  };

  const handleDragEnter = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    dragCounterRef.current += 1;
    setIsDragOver(true);
  };

  const handleDragLeave = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    dragCounterRef.current -= 1;
    if (dragCounterRef.current <= 0) {
      dragCounterRef.current = 0;
      setIsDragOver(false);
    }
  };

  const handleDragOver = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    event.dataTransfer.dropEffect = "copy";
  };

  const handleDrop = (event: React.DragEvent<HTMLDivElement>) => {
    event.preventDefault();
    event.stopPropagation();
    dragCounterRef.current = 0;
    setIsDragOver(false);
    const file = event.dataTransfer.files?.[0];
    if (file) {
      void handleFileSelect(file);
    }
  };

  const isProcessing = isResolvingBanco || isImporting;
  const loadingDialogDescription = isResolvingBanco
    ? "Consultando banco pelo código do arquivo..."
    : "Processando arquivo de remessa e validando títulos...";
  const fileDropZoneClassName = `rounded-lg border-2 border-dashed transition-colors ${
    isDragOver ? "border-[#FF6B00] bg-[#FF6B00]/5" : "border-border"
  }`;

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Importação de Título via CRA</h1>
        <p className="text-sm text-muted-foreground">
          Anexe o arquivo de remessa. O banco será detectado e os títulos processados automaticamente.
        </p>
      </div>

      <div className="space-y-4 rounded-xl border bg-card p-4 shadow-xs md:p-5">
        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Banco detectado</label>
          <div className="rounded-lg border bg-muted/20 p-3">
            {detectedBanco ? (
              <p className="text-sm text-foreground">
                <span className="font-semibold">{detectedBanco.descricao || "Banco"}</span>{" "}
                <span className="text-muted-foreground">
                  ({(detectedBanco.codigo_banco ?? "").trim().toUpperCase()})
                </span>
              </p>
            ) : (
              <p className="text-sm text-muted-foreground">
                {detectedBancoCode
                  ? `Código ${detectedBancoCode} detectado no arquivo. Cadastre o banco para continuar.`
                  : "Selecione um arquivo para detectar o banco automaticamente."}
              </p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <label id="cra-importacao-arquivo-label" className="text-sm font-medium text-foreground">
            Arquivo
          </label>
          <input
            ref={fileInputRef}
            id="cra-importacao-arquivo-input"
            type="file"
            className="sr-only"
            accept=".txt,.csv,.xml,text/plain,text/csv,application/xml,text/xml"
            aria-labelledby="cra-importacao-arquivo-label"
            disabled={isProcessing || isSavingBanco}
            onChange={(event) => {
              void handleFileSelect(event.target.files?.[0]);
              event.target.value = "";
            }}
          />
          <div
            role="button"
            tabIndex={isProcessing || isSavingBanco ? -1 : 0}
            aria-labelledby="cra-importacao-arquivo-label"
            aria-describedby="cra-importacao-arquivo-hint"
            aria-disabled={isProcessing || isSavingBanco}
            className={`${fileDropZoneClassName} ${isProcessing || isSavingBanco ? "pointer-events-none opacity-60" : ""}`}
            onClick={() => {
              if (!isProcessing && !isSavingBanco) fileInputRef.current?.click();
            }}
            onKeyDown={(event) => {
              if (isProcessing || isSavingBanco) return;
              if (event.key === "Enter" || event.key === " ") {
                event.preventDefault();
                fileInputRef.current?.click();
              }
            }}
            onDragEnter={handleDragEnter}
            onDragLeave={handleDragLeave}
            onDragOver={handleDragOver}
            onDrop={handleDrop}
          >
            {!selectedFile ? (
              <div className="flex flex-col items-center gap-3 p-6 text-center">
                <Upload className="h-6 w-6 text-muted-foreground" strokeWidth={1.5} />
                <div className="space-y-1">
                  <p className="text-sm font-medium text-foreground">
                    Arraste e solte o arquivo aqui ou clique para selecionar
                  </p>
                  <p id="cra-importacao-arquivo-hint" className="text-xs text-muted-foreground">
                    Formatos esperados: `.txt`, `.csv`, `.xml`
                  </p>
                </div>
              </div>
            ) : (
              <div className="p-4">
                <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                  <div className="flex min-w-0 items-center gap-3">
                    <div className="rounded-md border bg-background p-2">
                      <FileText className="h-5 w-5 text-muted-foreground" />
                    </div>
                    <div className="min-w-0">
                      <p className="truncate text-sm font-medium text-foreground">{selectedFile.name}</p>
                      <p className="text-xs text-muted-foreground">{formatFileSize(selectedFile.size)}</p>
                      <p id="cra-importacao-arquivo-hint" className="mt-1 text-xs text-muted-foreground">
                        {isProcessing
                          ? "Aguarde o processamento do arquivo..."
                          : "Arraste outro arquivo aqui para substituir"}
                      </p>
                    </div>
                  </div>
                  <div className="flex items-center gap-2">
                    <Button
                      type="button"
                      variant="outline"
                      size="sm"
                      disabled={isProcessing || isSavingBanco}
                      onClick={(event) => {
                        event.stopPropagation();
                        fileInputRef.current?.click();
                      }}
                    >
                      Trocar arquivo
                    </Button>
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      disabled={isProcessing || isSavingBanco}
                      onClick={(event) => {
                        event.stopPropagation();
                        handleResetFile();
                      }}
                      aria-label="Remover arquivo"
                    >
                      <Trash2 className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {importResult?.ok ? (
          <div className="flex justify-end pt-1">
            <Button
              type="button"
              className="bg-[#FF6B00] text-white hover:bg-[#E56000]"
              disabled={isSaving || isConfirmed || isProcessing}
              onClick={() => setIsConfirmImportDialogOpen(true)}
            >
              {isSaving ? "Confirmando..." : isConfirmed ? "Importação confirmada" : "Confirmar importação"}
            </Button>
          </div>
        ) : null}

        {importResult ? (
          <div className="rounded-lg border bg-muted/20 p-3">
            {importResult.ok ? (
              <div className="space-y-3 text-sm">
                <div className="space-y-1">
                  <p className="font-medium text-foreground">Arquivo validado com sucesso.</p>
                  <p className="text-muted-foreground">
                    Títulos encontrados:{" "}
                    <span className="font-medium text-foreground">{importResult.parsed?.transacoes.length ?? 0}</span>
                  </p>
                  {isConfirmed ? <p className="font-medium text-emerald-600">Importação confirmada.</p> : null}
                </div>
                <div className="space-y-2">
                  {importResult.parsed?.transacoes.map((transacao, index) => (
                    <CraImportacaoSubView
                      key={`${transacao.nossoNumero || "titulo"}-${index}`}
                      transacao={transacao}
                      index={index}
                      onClick={() => handleOpenTransacaoDetails(transacao, index)}
                    />
                  ))}
                </div>
              </div>
            ) : (
              <div className="space-y-2 text-sm">
                <p className="font-medium text-destructive">Foram encontrados erros na remessa.</p>
                <ul className="space-y-1 text-muted-foreground">
                  {importResult.errors.slice(0, 5).map((error) => (
                    <li key={`${error.code}-${error.line ?? 0}-${error.message}`}>- {error.message}</li>
                  ))}
                </ul>
              </div>
            )}
          </div>
        ) : null}
      </div>

      <LoadingDialog
        open={isProcessing}
        title="Processando importação"
        description={loadingDialogDescription}
      />

      <Dialog open={isBancoCadastroDialogOpen} onOpenChange={setIsBancoCadastroDialogOpen}>
        <DialogContent className="sm:max-w-4xl">
          <DialogHeader>
            <DialogTitle>Cadastrar banco</DialogTitle>
            <DialogDescription>
              O código {detectedBancoCode ? `"${detectedBancoCode}"` : "do arquivo"} não está cadastrado. Preencha os
              dados abaixo para continuar a importação.
            </DialogDescription>
          </DialogHeader>
          <PBancoForm
            defaultValues={{
              codigo_banco: detectedBancoCode ?? "",
            }}
            onSubmit={handleSaveNovoBanco}
            isLoading={isSavingBanco}
          />
        </DialogContent>
      </Dialog>

      <CraImportacaoDetailsModal
        open={isDetailsModalOpen}
        onOpenChange={setIsDetailsModalOpen}
        transacao={selectedTransacao}
        index={selectedTransacaoIndex}
      />

      <ConfirmDialog
        isOpen={isConfirmImportDialogOpen}
        title={selectedFile?.name ?? "Remessa CRA"}
        description="Confirmar importação"
        message={
          titulosEncontradosCount === 1
            ? "Você deseja realmente importar esse 1 título?"
            : `Você deseja realmente importar esses ${titulosEncontradosCount} títulos?`
        }
        confirmText="Importar"
        onConfirm={() => void handleConfirmImport()}
        onCancel={() => setIsConfirmImportDialogOpen(false)}
      />
    </div>
  );
}
