"use client";

import { useEffect, useRef, useState } from "react";
import { FileText, Trash2, Upload } from "lucide-react";
import { useRouter } from "next/navigation";
import { toast } from "sonner";
import {
  AlertDialog,
  AlertDialogAction,
  AlertDialogCancel,
  AlertDialogContent,
  AlertDialogDescription,
  AlertDialogFooter,
  AlertDialogHeader,
  AlertDialogTitle,
} from "@/components/ui/alert-dialog";
import { Button } from "@/components/ui/button";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import type { PBancoInterface } from "@/packages/administrativo/interfaces/PBanco/PBancoInterface";
import { importCraRemessaFile } from "@/packages/cra/functions/CraImportacao";
import type { CraRemessaImportResult, CraRemessaTransacao } from "@/packages/cra/functions/CraImportacao";
import { useCraImportacaoSaveHook } from "@/packages/cra/hooks/CraImportacao/useCraImportacaoSaveHook";
import { isCraImportacaoSaveResult } from "@/packages/cra/interface/CraImportacao/CraImportacaoSaveInterface";
import { CraImportacaoDetailsModal } from "./CraImportacaoDetailsModal";
import { CraImportacaoSubView } from "./CraImportacaoSubView";

function extractBancoCodeFromFileName(fileName: string): string | null {
  const match = fileName.trim().toUpperCase().match(/^B([A-Z0-9]{3})/);
  return match?.[1] ?? null;
}

export default function CraImportacaoIndex() {
  const router = useRouter();
  const { bancos, fetchBancos } = usePBancoReadHook();
  const { isSaving, saveCraImportacao } = useCraImportacaoSaveHook();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [detectedBancoCode, setDetectedBancoCode] = useState<string | null>(null);
  const [detectedBanco, setDetectedBanco] = useState<PBancoInterface | null>(null);
  const [isBancoNotFoundDialogOpen, setIsBancoNotFoundDialogOpen] = useState(false);
  const [isDragOver, setIsDragOver] = useState(false);
  const [isImporting, setIsImporting] = useState(false);
  const [importResult, setImportResult] = useState<CraRemessaImportResult | null>(null);
  const [isConfirmed, setIsConfirmed] = useState(false);
  const [selectedTransacao, setSelectedTransacao] = useState<CraRemessaTransacao | null>(null);
  const [selectedTransacaoIndex, setSelectedTransacaoIndex] = useState<number | undefined>(undefined);
  const [isDetailsModalOpen, setIsDetailsModalOpen] = useState(false);
  const fileInputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    void fetchBancos();
  }, [fetchBancos]);

  useEffect(() => {
    if (!detectedBancoCode) {
      setDetectedBanco(null);
      return;
    }

    const matchedBanco =
      bancos.find((banco) => (banco.codigo_banco ?? "").trim().padStart(3, "0") === detectedBancoCode) ?? null;
    setDetectedBanco(matchedBanco);

    if (!matchedBanco && bancos.length > 0) {
      setIsBancoNotFoundDialogOpen(true);
    }
  }, [bancos, detectedBancoCode]);

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

    // Verifica o banco imediatamente no momento da seleção do arquivo.
    let bancosParaValidacao = bancos;
    if (bancosParaValidacao.length === 0) {
      const response = await fetchBancos();
      if (Array.isArray(response)) {
        bancosParaValidacao = response;
      }
    }

    const matchedBanco =
      bancosParaValidacao.find((banco) => (banco.codigo_banco ?? "").trim().padStart(3, "0") === codigoBanco) ?? null;

    setDetectedBanco(matchedBanco);
    if (!matchedBanco) {
      setIsBancoNotFoundDialogOpen(true);
    }
  };

  const handleResetFile = () => {
    setSelectedFile(null);
    setDetectedBancoCode(null);
    setDetectedBanco(null);
    setImportResult(null);
    setIsConfirmed(false);
    setSelectedTransacao(null);
    setSelectedTransacaoIndex(undefined);
    setIsDetailsModalOpen(false);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  };

  const formatFileSize = (size: number) => {
    if (size < 1024) return `${size} B`;
    if (size < 1024 * 1024) return `${(size / 1024).toFixed(1)} KB`;
    return `${(size / (1024 * 1024)).toFixed(2)} MB`;
  };

  const handleImport = async () => {
    if (!selectedFile) return;
    if (!detectedBanco) {
      setIsBancoNotFoundDialogOpen(true);
      return;
    }

    setIsImporting(true);
    try {
      const result = await importCraRemessaFile(selectedFile);
      setImportResult(result);

      if (!result.ok) {
        toast.error("Arquivo CRA inválido", {
          description: result.errors[0]?.message || "Falha na validação da remessa.",
        });
        return;
      }

      setIsConfirmed(false);
      toast.success("Arquivo CRA validado com sucesso", {
        description: `${result.parsed?.transacoes.length ?? 0} título(s) pronto(s) para confirmação.`,
      });
    } catch {
      toast.error("Falha ao processar arquivo de remessa");
    } finally {
      setIsImporting(false);
    }
  };

  const handleConfirmImport = async () => {
    if (!importResult?.ok || !importResult.parsed || !detectedBanco) return;

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

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">Importação de Título via CRA</h1>
        <p className="text-sm text-muted-foreground">
          Anexe o arquivo de remessa e inicie a importação. O banco será detectado automaticamente.
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
                  ({(detectedBanco.codigo_banco ?? "").trim().padStart(3, "0")})
                </span>
              </p>
            ) : (
              <p className="text-sm text-muted-foreground">
                {detectedBancoCode
                  ? `Código ${detectedBancoCode} detectado no arquivo, mas não cadastrado.`
                  : "Selecione um arquivo para detectar o banco automaticamente."}
              </p>
            )}
          </div>
        </div>

        <div className="space-y-2">
          <label className="text-sm font-medium text-foreground">Arquivo</label>
          <input
            ref={fileInputRef}
            type="file"
            className="hidden"
            onChange={(event) => handleFileSelect(event.target.files?.[0])}
          />
          {!selectedFile ? (
            <div
              role="button"
              tabIndex={0}
              className={`rounded-lg border-2 border-dashed p-6 transition-colors ${
                isDragOver ? "border-[#FF6B00] bg-[#FF6B00]/5" : "border-border"
              }`}
              onClick={() => fileInputRef.current?.click()}
              onKeyDown={(event) => {
                if (event.key === "Enter" || event.key === " ") {
                  event.preventDefault();
                  fileInputRef.current?.click();
                }
              }}
              onDragOver={(event) => {
                event.preventDefault();
                setIsDragOver(true);
              }}
              onDragLeave={() => setIsDragOver(false)}
              onDrop={(event) => {
                event.preventDefault();
                setIsDragOver(false);
                handleFileSelect(event.dataTransfer.files?.[0]);
              }}
            >
              <div className="flex flex-col items-center gap-3 text-center">
                <Upload className="h-6 w-6 text-muted-foreground" strokeWidth={1.5} />
                <div className="space-y-1">
                  <p className="text-sm font-medium text-foreground">
                    Arraste e solte o arquivo aqui ou clique para selecionar
                  </p>
                  <p className="text-xs text-muted-foreground">Formatos esperados: `.txt`, `.csv`, `.xml`</p>
                </div>
              </div>
            </div>
          ) : null}
          {selectedFile ? (
            <div className="rounded-lg border bg-muted/20 p-4">
              <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
                <div className="flex min-w-0 items-center gap-3">
                  <div className="rounded-md border bg-background p-2">
                    <FileText className="h-5 w-5 text-muted-foreground" />
                  </div>
                  <div className="min-w-0">
                    <p className="truncate text-sm font-medium text-foreground">{selectedFile.name}</p>
                    <p className="text-xs text-muted-foreground">{formatFileSize(selectedFile.size)}</p>
                  </div>
                </div>
                <div className="flex items-center gap-2">
                  <Button type="button" variant="outline" size="sm" onClick={() => fileInputRef.current?.click()}>
                    Trocar arquivo
                  </Button>
                  <Button type="button" variant="ghost" size="icon" onClick={handleResetFile} aria-label="Remover arquivo">
                    <Trash2 className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        <div className="pt-1">
          <div className="flex flex-wrap items-center gap-2">
            <Button
              type="button"
              className="bg-[#FF6B00] text-white hover:bg-[#E56000]"
              disabled={!selectedFile || isImporting}
              onClick={handleImport}
            >
              {isImporting ? "Importando..." : "Importar"}
            </Button>
            <Button
              type="button"
              variant="outline"
              disabled={!importResult?.ok || isSaving || isConfirmed}
              onClick={handleConfirmImport}
            >
              {isSaving ? "Confirmando..." : isConfirmed ? "Importação confirmada" : "Confirmar importação"}
            </Button>
          </div>
        </div>

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

      <AlertDialog open={isBancoNotFoundDialogOpen} onOpenChange={setIsBancoNotFoundDialogOpen}>
        <AlertDialogContent>
          <AlertDialogHeader>
            <AlertDialogTitle>Banco não cadastrado</AlertDialogTitle>
            <AlertDialogDescription>
              O código {detectedBancoCode ? `"${detectedBancoCode}"` : "detectado no arquivo"} não foi encontrado na
              base de bancos. Para seguir, é necessário cadastrar o banco primeiro.
            </AlertDialogDescription>
          </AlertDialogHeader>
          <AlertDialogFooter>
            <AlertDialogCancel>Fechar</AlertDialogCancel>
            <AlertDialogAction
              onClick={() => {
                router.push("/cadastro/banco");
              }}
            >
              Continuar
            </AlertDialogAction>
          </AlertDialogFooter>
        </AlertDialogContent>
      </AlertDialog>

      <CraImportacaoDetailsModal
        open={isDetailsModalOpen}
        onOpenChange={setIsDetailsModalOpen}
        transacao={selectedTransacao}
        index={selectedTransacaoIndex}
      />
    </div>
  );
}
