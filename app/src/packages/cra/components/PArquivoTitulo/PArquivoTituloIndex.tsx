"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { toast } from "sonner";
import { usePBancoReadHook } from "@/packages/administrativo/hooks/PBanco/usePBancoReadHook";
import { PArquivoTituloFilter } from "@/packages/cra/components/PArquivoTitulo/PArquivoTituloFilter";
import {
  buildPArquivoTituloIndexQuery,
  defaultPArquivoTituloFilterState,
  type PArquivoTituloFilterState,
} from "@/packages/cra/components/PArquivoTitulo/pArquivoTituloFilterUtils";
import { usePTituloArquivoReadHook } from "@/packages/cra/hooks/PTituloArquivo/usePTituloArquivoReadHook";
import type { PArquivoTituloInterface } from "@/packages/cra/interface/PArquivoTitulo/PArquivoTituloInterface";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";
import { PArquivoTituloTable } from "./PArquivoTituloTable";
import { PArquivoTituloTitulosTableDialog } from "./PArquivoTituloTitulosTableDialog";

const PARQUIVO_TITULO_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

export default function PArquivoTituloIndex() {
  const { bancos, fetchBancos } = usePBancoReadHook();
  const { arquivosTitulo, pagination, isLoading, fetchArquivosTitulo } = usePTituloArquivoReadHook();
  const [filters, setFilters] = useState<PArquivoTituloFilterState>(defaultPArquivoTituloFilterState);
  const [page, setPage] = useState(1);
  const [titulosModalOpen, setTitulosModalOpen] = useState(false);
  const [arquivoSelecionado, setArquivoSelecionado] = useState<PArquivoTituloInterface | null>(null);

  useEffect(() => {
    void fetchBancos({ page: 1, per_page: 500, sort: "banco_id.desc" });
  }, [fetchBancos]);

  const bancoCodigoById = useMemo(
    () =>
      new Map(
        bancos.map((banco) => [
          String(banco.banco_id),
          (banco.codigo_banco ?? "").trim(),
        ]),
      ),
    [bancos],
  );

  const apiFilters = useMemo(
    () => buildPArquivoTituloIndexQuery(filters, bancoCodigoById),
    [filters, bancoCodigoById],
  );

  const indexQuery = useMemo(
    () => ({
      ...(apiFilters ?? {}),
      page,
      per_page: PARQUIVO_TITULO_PER_PAGE,
      sort: "arquivo_titulo_id.desc",
      include: "titulos",
    }),
    [apiFilters, page],
  );

  useEffect(() => {
    void fetchArquivosTitulo(indexQuery);
  }, [fetchArquivosTitulo, indexQuery]);

  const handleFiltersChange = useCallback((next: PArquivoTituloFilterState) => {
    setFilters(next);
    setPage(1);
  }, []);

  const handleSearch = () => {
    void fetchArquivosTitulo(indexQuery);
  };

  const handleGerarArquivoConfirmacao = (arquivo: PArquivoTituloInterface) => {
    toast.info("Funcionalidade em construção", {
      description: `Geração de confirmação para "${arquivo.nome_arquivo ?? "arquivo"}" ainda não implementada.`,
    });
  };

  const handleVerTitulos = (arquivo: PArquivoTituloInterface) => {
    setArquivoSelecionado(arquivo);
    setTitulosModalOpen(true);
  };

  const handleEstornarRemessa = (arquivo: PArquivoTituloInterface) => {
    toast.info("Funcionalidade em construção", {
      description: `Estorno da remessa "${arquivo.nome_arquivo ?? "arquivo"}" ainda não implementado.`,
    });
  };

  return (
    <div className="flex w-full flex-col gap-4">
      <div className="space-y-1">
        <h1 className="text-3xl font-bold tracking-tight">CRA - Confirmação</h1>
        <p className="text-sm text-muted-foreground">
          Acompanhe os arquivos importados e execute as ações de confirmação da remessa.
        </p>
      </div>

      <PArquivoTituloFilter
        value={filters}
        onChange={handleFiltersChange}
        onSearch={handleSearch}
        disabled={isLoading}
      />

      <PArquivoTituloTable
        data={arquivosTitulo}
        isLoading={isLoading}
        onGerarArquivoConfirmacao={handleGerarArquivoConfirmacao}
        onEstornarRemessa={handleEstornarRemessa}
        onVerTitulos={handleVerTitulos}
      />

      <PArquivoTituloTitulosTableDialog
        key={arquivoSelecionado?.arquivo_titulo_id ?? "closed"}
        open={titulosModalOpen}
        onOpenChange={(open) => {
          setTitulosModalOpen(open);
          if (!open) setArquivoSelecionado(null);
        }}
        arquivo={arquivoSelecionado}
      />

      <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
    </div>
  );
}
