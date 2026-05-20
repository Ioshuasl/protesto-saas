"use client";

import { type FormEvent, useEffect, useState } from "react";
import { format, parseISO } from "date-fns";
import { ptBR } from "date-fns/locale";
import { CalendarIcon } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Calendar } from "@/components/ui/calendar";
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "@/components/ui/select";
import { Textarea } from "@/components/ui/textarea";
import { CircleQuestionMark, Loader2, Search } from "lucide-react";
import PPessoaTableFormDialog from "@/packages/administrativo/components/PPessoa/PPessoaTableFormDialog";
import type { PPessoaInterface } from "@/packages/administrativo/interfaces/PPessoa/PPessoaInterface";
import { useGUsuarioReadHook } from "@/packages/administrativo/hooks/GUsuario/useGUsuarioReadHook";
import { usePCertidaoSaveHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoSaveHook";
import { usePCertidaoShowHook } from "@/packages/certidao/hooks/PCertidao/usePCertidaoShowHook";
import type { PCertidaoInterface } from "@/packages/certidao/interface/PCertidao/PCertidaoInterface";
import { isPCertidaoSaveResult } from "@/packages/certidao/interface/PCertidao/PCertidaoSaveInterface";
import InfoDialog from "@/shared/components/InfoDialog/InfoDialog";
import type { PCertidaoFormValues } from "@/packages/certidao/components/PCertidao/PCertidaoFormValues";
import { cn } from "@/lib/utils";

export type { PCertidaoFormValues };

/** Texto explicativo reutilizado no diálogo de ajuda (edição e emissão na página). */
export const PCERTIDAO_TIPO_INFO_MARKDOWN = `De acordo com o **Livro IV** do Código de Normas (Tabelionato de Protesto de Títulos), a diferença entre as certidões é a seguinte:

* **Certidão Negativa:** É o documento que comprova que **não existem** protestos registrados contra uma pessoa ou empresa no período pesquisado (geralmente nos últimos 5 anos). Ela também é emitida quando existe dúvida sobre a identidade de pessoas com o mesmo nome (homonímia) e o cartório consegue confirmar que o protesto não pertence ao solicitante.
* **Certidão Positiva:** É o documento emitido quando **existem** protestos em nome do pesquisado. Nesse caso, a certidão deve obrigatoriamente listar os detalhes de cada dívida protestada.`;

interface PCertidaoFormProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  /** Certidão existente a editar (fluxo exclusivo deste componente). */
  certidao: PCertidaoInterface;
  onSaved?: (certidao: PCertidaoInterface) => void;
}

interface PCertidaoFormState {
  apresentante: string;
  cpfcnpj: string;
  tipo_certidao: "P" | "N";
  status: "A" | "C";
  data_certidao: string;
  hora_certidao: string;
  usuario_id: string;
  observacao: string;
}

function getNowDateAndTime() {
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");

  return {
    date: `${year}-${month}-${day}`,
    time: `${hours}:${minutes}`,
  };
}

function formatDateInput(date?: Date | string): string {
  if (!date) return "";
  const parsed = new Date(date);
  if (Number.isNaN(parsed.getTime())) return "";
  const year = parsed.getFullYear();
  const month = String(parsed.getMonth() + 1).padStart(2, "0");
  const day = String(parsed.getDate()).padStart(2, "0");
  return `${year}-${month}-${day}`;
}

function mapCertidaoToFormState(certidao: PCertidaoInterface): PCertidaoFormState {
  const nowDefaults = getNowDateAndTime();

  return {
    apresentante: certidao.apresentante ?? "",
    cpfcnpj: certidao.cpfcnpj ?? "",
    tipo_certidao: certidao.tipo_certidao ?? "P",
    status: certidao.status ?? "A",
    data_certidao: formatDateInput(certidao.data_certidao) || nowDefaults.date,
    hora_certidao: certidao.hora_certidao ?? nowDefaults.time,
    usuario_id: certidao.usuario_id ? String(certidao.usuario_id) : "",
    observacao: certidao.observacao ?? "",
  };
}

export function PCertidaoForm({ open, onOpenChange, certidao, onSaved }: PCertidaoFormProps) {
  const { usuarios, isLoading: isLoadingUsuarios, fetchUsuarios } = useGUsuarioReadHook();
  const { certidao: certidaoLoaded, isLoading: isLoadingShow, fetchCertidao } = usePCertidaoShowHook();
  const { isSaving, saveCertidao } = usePCertidaoSaveHook();
  const [formState, setFormState] = useState<PCertidaoFormState>(() => mapCertidaoToFormState(certidao));
  const [isBootstrappingHooks, setIsBootstrappingHooks] = useState(false);
  const [isPPessoaDialogOpen, setIsPPessoaDialogOpen] = useState(false);
  const [isInfoDialogOpen, setIsInfoDialogOpen] = useState(false);
  const isHooksLoading = isBootstrappingHooks || isLoadingUsuarios || isLoadingShow;
  const isFormLoading = isHooksLoading || isSaving;

  useEffect(() => {
    if (!open) return;
    let active = true;

    const loadHooksData = async () => {
      setIsBootstrappingHooks(true);
      try {
        await fetchUsuarios();
        await fetchCertidao(certidao.certidao_id);
      } finally {
        if (active) setIsBootstrappingHooks(false);
      }
    };

    void loadHooksData();

    return () => {
      active = false;
    };
  }, [open, certidao.certidao_id]);

  useEffect(() => {
    if (!open) return;
    if (certidaoLoaded) {
      setFormState(mapCertidaoToFormState(certidaoLoaded));
      return;
    }
    setFormState(mapCertidaoToFormState(certidao));
  }, [open, certidaoLoaded, certidao]);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    const payload: PCertidaoFormValues = {
      certidao_id: certidao.certidao_id,
      apresentante: formState.apresentante.trim(),
      cpfcnpj: formState.cpfcnpj.trim(),
      tipo_certidao: formState.tipo_certidao,
      status: formState.status,
      data_certidao: formState.data_certidao ? new Date(`${formState.data_certidao}T00:00:00`) : undefined,
      hora_certidao: formState.hora_certidao,
      usuario_id: formState.usuario_id ? Number(formState.usuario_id) : undefined,
      observacao: formState.observacao.trim(),
    };

    const response = await saveCertidao(payload);
    if (isPCertidaoSaveResult(response)) {
      onSaved?.(response);
      onOpenChange(false);
    }
  };

  const handleSelectPessoa = (pessoa: PPessoaInterface) => {
    setFormState((prev) => ({
      ...prev,
      apresentante: pessoa.nome ?? "",
      cpfcnpj: pessoa.cpfcnpj ?? "",
    }));
    setIsPPessoaDialogOpen(false);
  };

  return (
    <>
      <Dialog open={open} onOpenChange={onOpenChange}>
        <DialogContent className="max-h-[88vh] gap-3 overflow-y-auto p-5 sm:max-w-[680px] sm:p-6">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-1.5 pr-10 text-left">
              <span>Editar Certidão</span>
              <Button
                type="button"
                variant="ghost"
                size="icon"
                className="h-8 w-8 shrink-0"
                onClick={() => setIsInfoDialogOpen(true)}
                aria-label="Informações sobre tipos de certidão"
              >
                <CircleQuestionMark className="h-4 w-4" />
              </Button>
            </DialogTitle>
            <DialogDescription>Ajuste os dados cadastrais, tipo e status da certidão.</DialogDescription>
          </DialogHeader>

          {isHooksLoading ? (
            <div className="flex min-h-[260px] flex-col items-center justify-center gap-3 text-muted-foreground">
              <Loader2 className="h-5 w-5 animate-spin" />
              <p className="text-sm">Carregando dados do formulário...</p>
            </div>
          ) : (
            <form className="space-y-4" onSubmit={handleSubmit}>
              <div className="grid gap-4 md:grid-cols-2">
                <div className="space-y-1.5">
                  <Label htmlFor="apresentante">Apresentante</Label>
                  <div className="relative">
                    <Input
                      id="apresentante"
                      value={formState.apresentante}
                      onChange={(event) => setFormState((prev) => ({ ...prev, apresentante: event.target.value }))}
                      placeholder="Nome do apresentante"
                      className="pr-10"
                      required
                    />
                    <Button
                      type="button"
                      variant="ghost"
                      size="icon"
                      className="absolute top-1/2 right-1 h-8 w-8 -translate-y-1/2"
                      onClick={() => setIsPPessoaDialogOpen(true)}
                      aria-label="Buscar pessoa"
                    >
                      <Search className="h-4 w-4" />
                    </Button>
                  </div>
                </div>
                <div className="space-y-1.5">
                  <Label htmlFor="cpfcnpj">CPF/CNPJ</Label>
                  <Input
                    id="cpfcnpj"
                    value={formState.cpfcnpj}
                    onChange={(event) => setFormState((prev) => ({ ...prev, cpfcnpj: event.target.value }))}
                    placeholder="000.000.000-00"
                    required
                  />
                </div>

                <div className="space-y-1.5">
                  <Label>Tipo da Certidão</Label>
                  <Select
                    value={formState.tipo_certidao}
                    onValueChange={(value) => setFormState((prev) => ({ ...prev, tipo_certidao: value === "N" ? "N" : "P" }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o tipo" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="P">Positiva</SelectItem>
                      <SelectItem value="N">Negativa</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-1.5">
                  <Label>Status</Label>
                  <Select
                    value={formState.status}
                    onValueChange={(value) => setFormState((prev) => ({ ...prev, status: value === "C" ? "C" : "A" }))}
                  >
                    <SelectTrigger>
                      <SelectValue placeholder="Selecione o status" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="A">Ativa/Emitida</SelectItem>
                      <SelectItem value="C">Cancelada</SelectItem>
                    </SelectContent>
                  </Select>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="data_certidao">Data da Certidão</Label>
                  <Popover>
                    <PopoverTrigger asChild>
                      <Button
                        id="data_certidao"
                        type="button"
                        variant="outline"
                        className={cn(
                          "w-full justify-between text-left font-normal",
                          !formState.data_certidao && "text-muted-foreground",
                        )}
                      >
                        {formState.data_certidao
                          ? format(parseISO(formState.data_certidao), "dd/MM/yyyy", { locale: ptBR })
                          : "Selecionar data"}
                        <CalendarIcon className="h-4 w-4 opacity-50" strokeWidth={1.5} />
                      </Button>
                    </PopoverTrigger>
                    <PopoverContent className="w-auto p-0" align="start">
                      <Calendar
                        mode="single"
                        selected={
                          formState.data_certidao ? parseISO(formState.data_certidao) : undefined
                        }
                        onSelect={(date) =>
                          setFormState((prev) => ({
                            ...prev,
                            data_certidao: date ? format(date, "yyyy-MM-dd") : "",
                          }))
                        }
                        initialFocus
                      />
                    </PopoverContent>
                  </Popover>
                </div>

                <div className="space-y-1.5">
                  <Label htmlFor="hora_certidao">Hora da Certidão</Label>
                  <Input
                    id="hora_certidao"
                    type="time"
                    value={formState.hora_certidao}
                    onChange={(event) => setFormState((prev) => ({ ...prev, hora_certidao: event.target.value }))}
                  />
                </div>

                <div className="space-y-1.5 md:col-span-2">
                  <div className="pb-1">
                    <Button type="button" className="w-full bg-[#FF6B00] text-white hover:bg-[#E56000]">
                      Abrir Editor
                    </Button>
                  </div>
                  <Label htmlFor="usuario_id">Usuário responsável</Label>
                  <Select
                    value={formState.usuario_id || "none"}
                    onValueChange={(value) => setFormState((prev) => ({ ...prev, usuario_id: value === "none" ? "" : value }))}
                  >
                    <SelectTrigger id="usuario_id">
                      <SelectValue placeholder="Selecione o usuário" />
                    </SelectTrigger>
                    <SelectContent>
                      <SelectItem value="none">Sem usuário</SelectItem>
                      {usuarios.map((usuario) => (
                        <SelectItem key={usuario.usuario_id} value={String(usuario.usuario_id)}>
                          {usuario.nome_completo || usuario.login || `Usuário ${usuario.usuario_id}`}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>
              </div>

              <div className="space-y-1.5">
                <Label htmlFor="observacao">Observação</Label>
                <Textarea
                  id="observacao"
                  rows={3}
                  value={formState.observacao}
                  onChange={(event) => setFormState((prev) => ({ ...prev, observacao: event.target.value }))}
                  placeholder="Detalhes complementares da certidão"
                />
              </div>

              <div className="flex justify-end gap-2 pt-2">
                <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
                  Cancelar
                </Button>
                <Button type="submit" disabled={isFormLoading} className="bg-[#FF6B00] text-white hover:bg-[#E56000]">
                  {isSaving ? "Salvando..." : "Salvar alterações"}
                </Button>
              </div>
            </form>
          )}
        </DialogContent>
      </Dialog>

      <PPessoaTableFormDialog
        isOpen={isPPessoaDialogOpen}
        tipoPessoa="P"
        onClose={setIsPPessoaDialogOpen}
        onSave={handleSelectPessoa}
        buttonIsLoading={false}
      />
      <InfoDialog
        isOpen={isInfoDialogOpen}
        onOpenChange={setIsInfoDialogOpen}
        title="Tipos de certidão"
        description="Diferença entre certidão negativa e positiva"
        content={PCERTIDAO_TIPO_INFO_MARKDOWN}
      />
    </>
  );
}
