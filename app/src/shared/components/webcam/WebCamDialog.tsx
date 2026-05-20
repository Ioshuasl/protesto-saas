'use client';

import { DialogClose } from '@radix-ui/react-dialog';
import { CameraIcon, RotateCcwIcon } from 'lucide-react';
import { useEffect, useMemo, useState } from 'react';

import { Button } from '@/components/ui/button';
import {
  Dialog,
  DialogContent,
  DialogFooter,
  DialogHeader,
  DialogTitle,
} from '@/components/ui/dialog';
import LoadingButton from '@/shared/components/loadingButton/LoadingButton';
import WebcamCapture from '@/shared/components/webcam/webcam';
import WebCamDialogInterface from '@/shared/interfaces/WebCamDialogInterface';

export default function WebCamDialog({
  isOpen,
  isLoading,
  onClose,
  onSave,
}: WebCamDialogInterface) {
  const [base64, setBase64] = useState('');

  const previewSrc = useMemo(() => {
    if (!base64?.trim()) return '';
    return base64.startsWith('data:') ? base64 : `data:image/jpeg;base64,${base64}`;
  }, [base64]);

  const hasPhoto = !!previewSrc;

  useEffect(() => {
    if (!isOpen) setBase64('');
  }, [isOpen]);

  return (
    <Dialog
      open={isOpen}
      onOpenChange={(open) => {
        if (!open) onClose(null, false);
      }}
    >
      <DialogContent className="w-full max-w-full p-6 sm:max-w-md">
        <DialogHeader className="space-y-2">
          <DialogTitle className="flex items-center gap-2 text-lg sm:text-xl">
            <CameraIcon className="h-5 w-5" />
            Foto
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-4">
          {/* Se tem foto: renderiza quadrado com preview.
              Se não tem: renderiza WebcamCapture livre (sem ser cortado). */}
          {hasPhoto ? (
            <div className="bg-muted/10 relative aspect-square w-full overflow-hidden rounded-lg border">
              <img
                src={previewSrc}
                alt="Pré-visualização da foto"
                className="h-full w-full object-cover"
              />
            </div>
          ) : (
            <WebcamCapture onCapture={setBase64} />
          )}

          <div className="flex items-center justify-end gap-2">
            <Button
              type="button"
              variant="outline"
              disabled={!hasPhoto}
              onClick={() => setBase64('')}
              className="h-9"
            >
              <RotateCcwIcon className="me-2 h-4 w-4" />
              Refazer
            </Button>

            <LoadingButton
              text="Salvar"
              textLoading="Salvando..."
              type="button"
              disabled={!hasPhoto}
              loading={isLoading}
              onClick={() => onSave(base64)}
            />
          </div>
        </div>

        <DialogFooter className="mt-4">
          <DialogClose asChild>
            <Button variant="outline" type="button" className="w-full sm:w-auto">
              Cancelar
            </Button>
          </DialogClose>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
}
