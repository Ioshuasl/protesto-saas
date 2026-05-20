'use client';

import {
  Download,
  Eye,
  File as FileIcon,
  FileArchive,
  FileImage,
  FileSpreadsheet,
  FileText,
  MoreVertical,
  Plus,
  PresentationIcon,
  Share2,
  Trash2,
} from 'lucide-react';
import Image from 'next/image';
import { type ElementType } from 'react';

import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import {
  DropdownMenu,
  DropdownMenuContent,
  DropdownMenuItem,
  DropdownMenuSeparator,
  DropdownMenuTrigger,
} from '@/components/ui/dropdown-menu';
import { Skeleton } from '@/components/ui/skeleton';

import FileInterface from './interfaces/FileInterface';
import FilesIndexInterface from './interfaces/FilesIndexInterface';

const FILE_KIND_META: Record<string, { label: string; icon: ElementType }> = {
  image: { label: 'IMG', icon: FileImage },
  pdf: { label: 'PDF', icon: FileText },
  sheet: { label: 'XLS', icon: FileSpreadsheet },
  slides: { label: 'PPT', icon: PresentationIcon },
  archive: { label: 'ZIP', icon: FileArchive },
  other: { label: 'ARQ', icon: FileText },
};

function kindMeta(kind?: string) {
  return FILE_KIND_META[kind ?? 'other'] ?? FILE_KIND_META.other;
}

function isExternalUrl(src?: string) {
  return !!src && (src.startsWith('http://') || src.startsWith('https://'));
}

function FileActionsMenu({
  file,
  onView,
  onDownload,
  onDelete,
  onShare,
}: {
  file: FileInterface;
  onView?: (file: FileInterface) => void;
  onDownload?: (file: FileInterface) => void;
  onDelete?: (file: FileInterface) => void;
  onShare?: (file: FileInterface) => void;
}) {
  return (
    <DropdownMenu>
      <DropdownMenuTrigger asChild>
        <Button
          variant="ghost"
          size="icon"
          className="h-8 w-8 rounded-full"
          aria-label={`Ações de ${file.name}`}
        >
          <MoreVertical className="h-4 w-4" />
        </Button>
      </DropdownMenuTrigger>

      <DropdownMenuContent align="end" className="w-48">
        {onView && (
          <DropdownMenuItem onClick={() => onView(file)}>
            <Eye className="mr-2 h-4 w-4" />
            Visualizar
          </DropdownMenuItem>
        )}
        {onShare && (
          <DropdownMenuItem onClick={() => onShare(file)}>
            <Share2 className="mr-2 h-4 w-4" />
            Compartilhar
          </DropdownMenuItem>
        )}
        {onDownload && (
          <>
            <DropdownMenuSeparator />
            <DropdownMenuItem onClick={() => onDownload(file)}>
              <Download className="mr-2 h-4 w-4" />
              Baixar
            </DropdownMenuItem>
          </>
        )}
        {onDelete && (
          <>
            <DropdownMenuSeparator />
            <DropdownMenuItem
              className="text-destructive"
              onClick={() => onDelete(file)}
            >
              <Trash2 className="mr-2 h-4 w-4" />
              Remover
            </DropdownMenuItem>
          </>
        )}
      </DropdownMenuContent>
    </DropdownMenu>
  );
}

function FileThumbnail({ file }: { file: FileInterface }) {
  const { icon: Icon, label } = kindMeta(file.kind);

  if (!file.thumbUrl) {
    return (
      <div className="bg-muted relative flex aspect-square w-full items-center justify-center rounded-t-xl">
        <div className="absolute top-3 left-3">
          <Badge variant="secondary" className="gap-1">
            <Icon className="h-3.5 w-3.5" />
            {label}
          </Badge>
        </div>
        <Icon className="text-muted-foreground h-10 w-10" />
      </div>
    );
  }

  return (
    <div className="bg-muted relative aspect-square w-full overflow-hidden rounded-t-xl">
      <div className="absolute top-3 left-3 z-10">
        <Badge variant="secondary" className="gap-1 backdrop-blur">
          <Icon className="h-3.5 w-3.5" />
          {label}
        </Badge>
      </div>
      {isExternalUrl(file.thumbUrl) ? (
        <img
          src={file.thumbUrl}
          alt={file.name}
          className="h-full w-full object-cover"
          loading="lazy"
        />
      ) : (
        <Image src={file.thumbUrl} alt={file.name} fill className="object-cover" />
      )}
    </div>
  );
}

function FileCard({
  file,
  onView,
  onDownload,
  onDelete,
  onShare,
}: {
  file: FileInterface;
  onView?: (file: FileInterface) => void;
  onDownload?: (file: FileInterface) => void;
  onDelete?: (file: FileInterface) => void;
  onShare?: (file: FileInterface) => void;
}) {
  return (
    <Card className="group overflow-hidden transition hover:shadow-md">
      <CardContent className="p-0">
        <FileThumbnail file={file} />

        <div className="flex items-start justify-between gap-2 p-3">
          <div className="min-w-0">
            <p className="truncate text-sm font-medium" title={file.name}>
              {file.name}
            </p>
            <div className="text-muted-foreground mt-1 flex items-center gap-2 text-xs">
              {file.size && <span>{file.size}</span>}
              {file.size && file.activity && <span>•</span>}
              {file.activity && <span className="truncate">{file.activity}</span>}
            </div>
          </div>

          {(onView || onDownload || onDelete || onShare) && (
            <FileActionsMenu
              file={file}
              onView={onView}
              onDownload={onDownload}
              onDelete={onDelete}
              onShare={onShare}
            />
          )}
        </div>
      </CardContent>
    </Card>
  );
}

function LoadingSkeleton() {
  return (
    <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
      {Array.from({ length: 10 }).map((_, i) => (
        <Card key={i} className="overflow-hidden">
          <CardContent className="p-0">
            <Skeleton className="aspect-square w-full" />
            <div className="space-y-2 p-3">
              <Skeleton className="h-4 w-3/4" />
              <Skeleton className="h-3 w-1/2" />
            </div>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

function EmptyState({ onAdd }: { onAdd?: () => void }) {
  return (
    <Card className="border-dashed">
      <CardContent className="flex flex-col items-center justify-center gap-3 py-16 text-center">
        <div className="bg-muted rounded-full p-3">
          <FileIcon className="text-muted-foreground h-8 w-8" />
        </div>
        <div className="space-y-1">
          <p className="font-medium">Nenhum arquivo encontrado</p>
          <p className="text-muted-foreground text-sm">
            Adicione arquivos para começar a organizar os documentos.
          </p>
        </div>
        {onAdd && (
          <Button type="button" className="mt-2" onClick={onAdd}>
            <Plus className="mr-2 h-4 w-4" />
            Adicionar arquivo
          </Button>
        )}
      </CardContent>
    </Card>
  );
}

export default function FilesIndex({
  title = 'Arquivos',
  description,
  files,
  isLoading = false,
  onAdd,
  onView,
  onDownload,
  onDelete,
  onShare,
}: FilesIndexInterface) {
  return (
    <div className="space-y-4">
      <div className="flex flex-col gap-3 sm:flex-row sm:items-center sm:justify-between">
        <div>
          <h2 className="text-lg font-semibold">{title}</h2>
          {description && (
            <p className="text-muted-foreground text-sm">{description}</p>
          )}
          {!description && (
            <p className="text-muted-foreground text-sm">
              {files.length} {files.length === 1 ? 'arquivo' : 'arquivos'}
            </p>
          )}
        </div>

        {onAdd && (
          <Button
            type="button"
            className="w-full sm:w-auto"
            onClick={onAdd}
            aria-label="Adicionar arquivo"
          >
            <Plus className="mr-2 h-4 w-4" />
            Adicionar
          </Button>
        )}
      </div>

      {isLoading ? (
        <LoadingSkeleton />
      ) : files.length === 0 ? (
        <EmptyState onAdd={onAdd} />
      ) : (
        <div className="grid grid-cols-2 gap-4 sm:grid-cols-3 md:grid-cols-4 lg:grid-cols-5">
          {files.map((file) => (
            <FileCard
              key={file.id}
              file={file}
              onView={onView}
              onDownload={onDownload}
              onDelete={onDelete}
              onShare={onShare}
            />
          ))}
        </div>
      )}
    </div>
  );
}
