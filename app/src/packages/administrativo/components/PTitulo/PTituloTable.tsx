"use client";

import { Button } from "@/components/ui/button";
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuTrigger,
} from "@/components/ui/dropdown-menu";
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table";
import { usePOcorrenciasReadHook } from "@/packages/administrativo/hooks/POcorrencias/usePOcorrenciasReadHook";
import { TituloListItem } from "@/packages/administrativo/services/PTitulo/PTituloService";
import { Cog, EllipsisVertical, Eye } from "lucide-react";
import { useEffect, useMemo } from "react";
import { getTriduoMessage, moneyFormatter } from "./titulo-list-utils";

type PTituloTableWorkflowItem = TituloListItem & {
  hasApontamentoBase?: boolean;
  hasIntimacao?: boolean;
  hasProtestoCompleto?: boolean;
};

interface PTituloTableProps {
  data: PTituloTableWorkflowItem[];
  isLoading?: boolean;
  onViewDetails: (titulo: TituloListItem) => void;
  onUpdateStatus: (tituloId: number, status: "Em Tríduo" | "Pago" | "Protestado") => void;
}

export function PTituloTable({ data, isLoading, onViewDetails, onUpdateStatus }: PTituloTableProps) {
  const { ocorrencias, fetchOcorrencias } = usePOcorrenciasReadHook();

  useEffect(() => {
    void fetchOcorrencias();
  }, [fetchOcorrencias]);

  const ocorrenciaLabelById = useMemo(
    () =>
      new Map(
        ocorrencias.map((ocorrencia) => [
          ocorrencia.ocorrencias_id,
          ocorrencia.descricao || ocorrencia.tipo || ocorrencia.codigo || "Sem ocorrência",
        ]),
      ),
    [ocorrencias],
  );

  if (isLoading) {
    return <div className="w-full flex items-center justify-center p-8 text-muted-foreground">Carregando títulos...</div>;
  }

  if (data.length === 0) {
    return (
      <div className="w-full flex items-center justify-center rounded-md border p-8 text-muted-foreground">
        Nenhum título encontrado.
      </div>
    );
  }

  return (
    <div className="rounded-md border overflow-x-auto">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead className="w-[60px]">ID</TableHead>
            <TableHead>Número/Nosso Número</TableHead>
            <TableHead>Protocolo</TableHead>
            <TableHead>Apresentante (Nome/CPF-CNPJ)</TableHead>
            <TableHead className="hidden lg:table-cell">Espécie</TableHead>
            <TableHead>Valor Total</TableHead>
            <TableHead>Ocorrência</TableHead>
            <TableHead className="text-right">Ações</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {data.map((titulo) => {
            const triduo = getTriduoMessage(titulo);
            const valorTotal = titulo.valor_total ?? titulo.valor_total_custas ?? titulo.valor_titulo ?? 0;
            const ocorrenciaLabel = titulo.ocorrencia_id
              ? ocorrenciaLabelById.get(titulo.ocorrencia_id) || "Sem ocorrência"
              : "Sem ocorrência";
            const hasValue = (value: unknown) => value !== null && value !== undefined && value !== "";
            const hasApontamentoBase =
              titulo.hasApontamentoBase ??
              (hasValue(titulo.numero_apontamento) && hasValue(titulo.data_apontamento));
            const hasIntimacao = titulo.hasIntimacao ?? (hasApontamentoBase && hasValue(titulo.data_intimacao));
            const hasProtestoCompleto =
              titulo.hasProtestoCompleto ??
              (hasIntimacao &&
                hasValue(titulo.data_protesto) &&
                hasValue(titulo.livro_id_protesto) &&
                hasValue(titulo.folha_protesto));

            return (
              <TableRow
                key={titulo.titulo_id}
                className="cursor-pointer"
                onClick={() => onViewDetails(titulo)}
              >
                <TableCell className="font-medium">{titulo.titulo_id}</TableCell>
                <TableCell>
                  <div className="flex max-w-[140px] flex-col">
                    <span className="truncate">{titulo.numero_titulo ?? "-"}</span>
                    <span className="truncate text-xs text-muted-foreground">
                      Nosso n. {titulo.nosso_numero ?? "-"}
                    </span>
                  </div>
                </TableCell>
                <TableCell className="whitespace-nowrap">{titulo.numero_apontamento ?? "-"}</TableCell>
                <TableCell>
                  <div className="flex max-w-[220px] flex-col">
                    <span className="truncate">{titulo.apresentante_nome ?? "-"}</span>
                    <span className="truncate text-xs text-muted-foreground">{titulo.apresentante_cpfcnpj ?? "-"}</span>
                  </div>
                </TableCell>
                <TableCell className="hidden lg:table-cell">{titulo.especie_sigla ?? "-"}</TableCell>
                <TableCell className="whitespace-nowrap">{moneyFormatter.format(valorTotal)}</TableCell>
                <TableCell>
                  <div className="flex min-w-[120px] flex-col gap-1">
                    <span>{ocorrenciaLabel}</span>
                    {triduo && <span className="text-xs text-muted-foreground">{triduo}</span>}
                  </div>
                </TableCell>
                <TableCell className="text-right">
                  <DropdownMenu>
                    <DropdownMenuTrigger asChild>
                      <Button
                        variant="ghost"
                        size="icon"
                        className="text-foreground hover:text-[#FF6B00]"
                        onClick={(event) => event.stopPropagation()}
                      >
                        <Cog className="h-4 w-4" strokeWidth={1.5} />
                        <span className="sr-only">Ações</span>
                      </Button>
                    </DropdownMenuTrigger>
                    <DropdownMenuContent align="end">
                      <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onViewDetails(titulo); }}>
                        <Eye className="mr-2 h-4 w-4" strokeWidth={1.5} />
                        Ver Detalhes
                      </DropdownMenuItem>
                      {hasProtestoCompleto ? (
                        <>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Voltar para Intimação" ainda não implementada'); }}>
                            <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Voltar para Intimação
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Cancelar Título" ainda não implementada'); }}>
                            <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Cancelar Título
                          </DropdownMenuItem>
                        </>
                      ) : hasIntimacao ? (
                        <>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Voltar para Apontamento" ainda não implementada'); }}>
                            <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Voltar para Apontamento
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); console.info('Ação "Aceite/Edital" ainda não implementada'); }}>
                            <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Aceite/Edital
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onUpdateStatus(titulo.titulo_id, "Pago"); }}>
                            <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Desistir/Liquidar Título
                          </DropdownMenuItem>
                          <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onUpdateStatus(titulo.titulo_id, "Protestado"); }}>
                            <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                            Protestar Título
                          </DropdownMenuItem>
                        </>
                      ) : hasApontamentoBase ? (
                        <DropdownMenuItem onClick={(event) => { event.stopPropagation(); onUpdateStatus(titulo.titulo_id, "Em Tríduo"); }}>
                          <EllipsisVertical className="mr-2 h-4 w-4" strokeWidth={1.5} />
                          Intimar Título
                        </DropdownMenuItem>
                      ) : null}
                    </DropdownMenuContent>
                  </DropdownMenu>
                </TableCell>
              </TableRow>
            );
          })}
        </TableBody>
      </Table>
    </div>
  );
}
