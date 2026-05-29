"use client";

import { useEffect, useMemo, useState } from "react";

import { PTemplateFilter } from "@/packages/administrativo/components/PTemplate/PTemplateFilter";
import { PTemplateOnlyOfficeDialog } from "@/packages/administrativo/components/PTemplate/PTemplateOnlyOfficeDialog";
import { PTemplateTable } from "@/packages/administrativo/components/PTemplate/PTemplateTable";
import { usePTemplateOnlyOfficeHook } from "@/packages/administrativo/hooks/PTemplate/usePTemplateOnlyOfficeHook";
import { usePTemplateReadHook } from "@/packages/administrativo/hooks/PTemplate/usePTemplateReadHook";
import type { PTemplateInterface } from "@/packages/administrativo/interfaces/PTemplate/PTemplateInterface";
import { DEFAULT_PAGINATION_META, Pagination } from "@/shared/components/pagination";

const PTEMPLATE_PER_PAGE = DEFAULT_PAGINATION_META.per_page;

export default function PTemplateIndex() {
  const { templates, pagination, isLoading, fetchTemplates } = usePTemplateReadHook();
  const {
    isEditorOpen,
    isLoading: isEditorLoading,
    selectedTemplate: editorTemplate,
    config: editorConfig,
    markerLegend,
    openEditor,
    closeEditor,
  } = usePTemplateOnlyOfficeHook();

  const [search, setSearch] = useState("");
  const [selected, setSelected] = useState<PTemplateInterface | null>(null);
  const [page, setPage] = useState(1);
  const [debouncedSearch, setDebouncedSearch] = useState(search);

  useEffect(() => {
    const timer = window.setTimeout(() => setDebouncedSearch(search), 400);
    return () => window.clearTimeout(timer);
  }, [search]);

  useEffect(() => {
    setPage(1);
  }, [debouncedSearch]);

  const query = useMemo(
    () => ({
      descricao: debouncedSearch || undefined,
      page,
      per_page: PTEMPLATE_PER_PAGE,
      sort: "template_id.desc",
    }),
    [debouncedSearch, page],
  );

  useEffect(() => {
    void fetchTemplates(query);
  }, [fetchTemplates, query]);

  return (
    <div className="flex w-full flex-col gap-6">
      <div className="flex flex-col gap-2">
        <h1 className="text-3xl font-bold tracking-tight">Minutas</h1>
        <p className="text-muted-foreground">
          Lista inicial de minutas (P_TEMPLATE). Edição detalhada será adicionada na próxima etapa.
        </p>
      </div>

      <div className="flex flex-col gap-4">
        <PTemplateFilter value={search} onChange={setSearch} />
        <PTemplateTable
          data={templates}
          isLoading={isLoading}
          onEdit={setSelected}
          onOpenDocument={(template) => void openEditor(template, "edit")}
        />
        <Pagination pagination={pagination} onPageChange={setPage} disabled={isLoading} />
      </div>

      {selected ? (
        <p className="text-sm text-muted-foreground">
          Minuta selecionada: #{selected.template_id} - {selected.descricao}
        </p>
      ) : null}

      <PTemplateOnlyOfficeDialog
        open={isEditorOpen}
        onOpenChange={(open) => {
          if (!open) closeEditor();
        }}
        template={editorTemplate}
        config={editorConfig}
        markerLegend={markerLegend}
        isLoading={isEditorLoading}
      />
    </div>
  );
}
