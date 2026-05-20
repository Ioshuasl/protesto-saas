'use client';

import * as React from 'react';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';

import FilesFormDialogInterface from './interfaces/FilesFormDialogInterface';
import { FilesForm } from './FilesForm';

export default function FilesFormDialog({
  isOpen,
  onClose,
  onSave,
  title = 'Arquivos',
  description = 'Selecione os arquivos para vincular',
  maxFiles = 10,
  maxSize = 5 * 1024 * 1024,
  buttonIsLoading = false,
}: FilesFormDialogInterface) {
  const [files, setFiles] = React.useState<File[]>([]);

  const handleSave = () => {
    if (files.length === 0) return;
    onSave(files);
    setFiles([]);
  };

  const handleOpenChange = (open: boolean) => {
    if (!open) setFiles([]);
    onClose(open);
  };

  return (
    <Dialog open={isOpen} onOpenChange={handleOpenChange}>
      <DialogContent className="max-h-[90vh] w-full max-w-xl overflow-auto p-6">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          <DialogDescription>{description}</DialogDescription>
        </DialogHeader>

        <div className="max-h-[50vh] overflow-y-auto py-2">
          <FilesForm
            value={files}
            onValueChange={setFiles}
            maxFiles={maxFiles}
            maxSize={maxSize}
          />
        </div>

        <DialogFooter className="gap-2 sm:gap-0">
          <Button
            variant="outline"
            type="button"
            onClick={() => handleOpenChange(false)}
          >
            Cancelar
          </Button>
          <Button
            type="button"
            onClick={handleSave}
            disabled={files.length === 0 || buttonIsLoading}
          >
            {buttonIsLoading ? 'Enviando...' : `Enviar ${files.length > 0 ? `(${files.length})` : ''}`}
          </Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
