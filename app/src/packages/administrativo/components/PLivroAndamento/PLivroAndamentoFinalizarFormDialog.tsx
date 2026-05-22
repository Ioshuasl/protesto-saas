"use client";

import { useEffect, useMemo, useState } from "react";
import { format, startOfDay } from "date-fns";
import { ptBR } from "date-fns/locale";

import { Button } from "@/components/ui/button";
import { DatePicker } from "@/components/ui/date-picker";
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Label } from "@/components/ui/label";
import type { PLivroAndamentoInterface } from "@/packages/administrativo/interfaces/PLivroAndamento/PLivroAndamentoInterface";

export type PLivroAndamentoFinalizarFormValues = {
  data_fechamento: Date;
};

interface PLivroAndamentoFinalizarFormDialogProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  livroAndamento: PLivroAndamentoInterface;
  onSubmit: (data: PLivroAndamentoFinalizarFormValues) => void;
  isLoading?: boolean;
}

function getDefaultDataFechamento(): Date {
  return startOfDay(new Date());
}

export function PLivroAndamentoFinalizarFormDialog({
  open,
  onOpenChange,
  livroAndamento,
  onSubmit,
  isLoading,
}: PLivroAndamentoFinalizarFormDialogProps) {
  const [dataFechamento, setDataFechamento] = useState<Date>(getDefaultDataFechamento);

  const dataAberturaMin = useMemo(() => {
    if (!livroAndamento.data_abertura) {
      return new Date("1900-01-01");
    }
    return startOfDay(new Date(livroAndamento.data_abertura));
  }, [livroAndamento.data_abertura]);

  const hoje = useMemo(() => startOfDay(new Date()), []);

  useEffect(() => {
    if (open) {
      setDataFechamento(getDefaultDataFechamento());
    }
  }, [open]);

  const handleSubmit = (event: React.FormEvent) => {
    event.preventDefault();
    onSubmit({ data_fechamento: dataFechamento });
  };

  const livroLabel =
    livroAndamento.numero_livro != null
      ? `Livro nº ${livroAndamento.numero_livro}`
      : "Livro em andamento";

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="top-[8dvh] left-[50%] flex max-h-[min(calc(100dvh-10dvh),640px)] translate-x-[-50%] translate-y-0 flex-col gap-4 overflow-hidden sm:max-w-[425px]">
        <DialogHeader className="shrink-0">
          <DialogTitle>Finalizar livro</DialogTitle>
        </DialogHeader>

        <form
          onSubmit={handleSubmit}
          className="flex min-h-0 flex-1 flex-col gap-4 overflow-y-auto [scrollbar-width:none] [-ms-overflow-style:none] [&::-webkit-scrollbar]:hidden"
        >
          <p className="shrink-0 text-sm text-muted-foreground">
            {livroLabel}
            {livroAndamento.data_abertura ? (
              <>
                {" "}
                · aberto em{" "}
                {format(new Date(livroAndamento.data_abertura), "dd/MM/yyyy", {
                  locale: ptBR,
                })}
              </>
            ) : null}
          </p>

          <div className="shrink-0 space-y-2">
            <Label htmlFor="data-fechamento">Data de fechamento</Label>
            <DatePicker
              id="data-fechamento"
              variant="hybrid"
              calendarSize="compact"
              showOutsideDays={false}
              showTodayButton={false}
              value={dataFechamento}
              onChange={(date) => {
                setDataFechamento(date ? startOfDay(date) : getDefaultDataFechamento());
              }}
              calendarDisabled={(date) => {
                const day = startOfDay(date);
                return day > hoje || day < dataAberturaMin;
              }}
              placeholder="dd/mm/aaaa"
            />
          </div>

          <DialogFooter className="shrink-0 gap-2 pt-2 sm:gap-0">
            <Button
              type="button"
              variant="outline"
              onClick={() => onOpenChange(false)}
              disabled={isLoading}
            >
              Cancelar
            </Button>
            <Button
              type="submit"
              disabled={isLoading}
              className="bg-[#FF6B00] hover:bg-[#E56000] text-white"
            >
              {isLoading ? "Finalizando..." : "Finalizar"}
            </Button>
          </DialogFooter>
        </form>
      </DialogContent>
    </Dialog>
  );
}
