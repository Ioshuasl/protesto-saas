'use client';

import { Download, File as FileIcon } from 'lucide-react';
import { useEffect, useState } from 'react';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

import { FileDownloadActions } from './actions/FileDownloadActions';
import { FilePathActions } from './actions/FilePathActions';
import { FileViewKindMeta } from './actions/FileViewKindMeta';
import FilesViewDialogSkeleton from './FilesViewDialogSkeleton';
import FilesViewDialogInterface from './interfaces/FilesViewDialogInterface';

export default function FilesViewDialog({
  isOpen,
  onClose,
  filePath,
  title: titleProp,
  onDownload,
  showDownloadButton = true,
}: FilesViewDialogInterface) {
  const [previewLoaded, setPreviewLoaded] = useState(false);

  const hasPath = !!filePath?.trim();
  const ext = hasPath ? FilePathActions.pathToExtension(filePath!) : '';
  const kind = FilePathActions.extensionToKind(ext);
  const fileName = hasPath ? FilePathActions.pathToFileName(filePath!) : '';
  const title = titleProp ?? (fileName || 'Visualizar arquivo');
  const { icon: Icon, label } = FileViewKindMeta.getMeta(kind);
  const canPreviewImage = kind === 'image' && hasPath;
  const canPreviewPdf = kind === 'pdf' && hasPath;

  useEffect(() => {
    setPreviewLoaded(false);
  }, [filePath]);

  useEffect(() => {
    if (!isOpen) setPreviewLoaded(false);
  }, [isOpen]);

  const handleOpenChange = (open: boolean) => {
    if (!open) onClose(false);
  };

  const handleDownload = () => {
    if (onDownload) {
      onDownload();
    } else if (filePath) {
      FileDownloadActions.forceDownload(filePath, fileName);
    }
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="flex h-dvh max-h-dvh w-full max-w-full flex-col overflow-hidden p-0 sm:h-auto sm:max-h-[90vh] sm:max-w-4xl">
        <DialogHeader className="shrink-0 border-b px-4 py-3 sm:px-6 sm:py-4">
          <DialogTitle>{title}</DialogTitle>
          {fileName && (
            <DialogDescription className="truncate">{fileName}</DialogDescription>
          )}
        </DialogHeader>
        <div className="flex min-h-0 flex-1 flex-col items-center justify-center overflow-auto p-4 sm:p-6">
          {!hasPath ? (
            <div className="text-muted-foreground flex flex-col items-center gap-2 text-sm">
              <FileIcon className="h-10 w-10 sm:h-12 sm:w-12" />
              <span>Nenhum arquivo selecionado</span>
            </div>
          ) : canPreviewImage ? (
            <div className="relative flex min-h-[60vh] w-full max-w-full flex-1 flex-col items-center justify-center sm:min-h-[70vh]">
              {!previewLoaded && <FilesViewDialogSkeleton />}
              {previewLoaded ? (
                <div className="relative max-h-[60vh] w-full max-w-full overflow-hidden rounded-lg border bg-background sm:max-h-[70vh]">
                  <img
                    src={filePath!}
                    alt={fileName}
                    className="h-full w-full object-contain"
                    style={{ maxHeight: '60vh' }}
                  />
                </div>
              ) : (
                <img
                  src={filePath!}
                  alt={fileName}
                  className="absolute inset-0 h-full w-full max-w-full opacity-0 object-contain"
                  onLoad={() => setPreviewLoaded(true)}
                />
              )}
            </div>
          ) : canPreviewPdf ? (
            <div className="relative flex h-[60vh] w-full max-w-full flex-col overflow-hidden rounded-lg border bg-background sm:h-[70vh]">
              {!previewLoaded && <FilesViewDialogSkeleton />}
              <iframe
                src={filePath!}
                title={fileName}
                className={`h-full w-full flex-1 ${previewLoaded ? 'block' : 'absolute inset-0 opacity-0'}`}
                onLoad={() => setPreviewLoaded(true)}
              />
            </div>
          ) : (
            <div className="flex flex-col items-center gap-4 rounded-lg border bg-background p-4 sm:p-8">
              <div className="bg-muted flex h-24 w-24 items-center justify-center rounded-full">
                <Icon className="text-muted-foreground h-12 w-12" />
              </div>
              <div className="text-center space-y-1">
                <p className="font-medium">{label}</p>
                <p className="text-muted-foreground max-w-xs truncate text-sm">{fileName}</p>
              </div>
              <p className="text-muted-foreground text-center text-sm">
                {showDownloadButton
                  ? 'Visualização não disponível para este tipo. Use o botão Baixar para abrir o arquivo.'
                  : 'Visualização não disponível para este tipo.'}
              </p>
            </div>
          )}
        </div>

        {hasPath && (
          <DialogFooter className="shrink-0 gap-2 border-t px-4 py-3 sm:px-6 sm:py-4">
            <Button variant="outline" type="button" onClick={() => handleOpenChange(false)}>
              Fechar
            </Button>
            {showDownloadButton && (
              <Button type="button" onClick={handleDownload}>
                <Download className="mr-2 h-4 w-4" />
                Baixar
              </Button>
            )}
          </DialogFooter>
        )}
      </DialogContent>
    </Dialog>
  );
}
