'use client';

import { Upload, X } from 'lucide-react';
import * as React from 'react';
import { toast } from 'sonner';

import { Button } from '@/components/ui/button';
import {
  FileUpload,
  FileUploadDropzone,
  FileUploadItem,
  FileUploadItemDelete,
  FileUploadItemMetadata,
  FileUploadItemPreview,
  FileUploadList,
  FileUploadTrigger,
} from '@/components/ui/file-upload';

export type FilesFormItemStatus = 'pending' | 'uploading' | 'uploaded' | 'error';

interface FilesFormProps {
  value?: File[];
  onValueChange?: (files: File[]) => void;
  maxFiles?: number;
  maxSize?: number;
  accept?: string | string[];
  renderFileControl?: (file: File) => React.ReactNode;
  fileStatus?: Record<string, FilesFormItemStatus>;
  fileErrorMessage?: Record<string, string>;
  getFileKey?: (file: File) => string;
  disableRemoveAfterSubmit?: boolean;
}

function defaultGetFileKey(file: File): string {
  return `${file.name}::${file.size}::${file.lastModified}`;
}

function getStatusLabel(status: FilesFormItemStatus): string {
  if (status === 'uploading') return 'Enviando...';
  if (status === 'uploaded') return 'Enviado';
  if (status === 'error') return 'Erro';
  return 'Aguardando envio';
}

function getStatusClassName(status: FilesFormItemStatus): string {
  if (status === 'uploading') return 'bg-blue-100 text-blue-700';
  if (status === 'uploaded') return 'bg-emerald-100 text-emerald-700';
  if (status === 'error') return 'bg-red-100 text-red-700';
  return 'bg-slate-100 text-slate-700';
}

export function FilesForm({
  value,
  onValueChange,
  maxFiles = 10,
  maxSize = 5 * 1024 * 1024,
  accept,
  renderFileControl,
  fileStatus,
  fileErrorMessage,
  getFileKey = defaultGetFileKey,
  disableRemoveAfterSubmit = true,
}: FilesFormProps) {
  const [internalFiles, setInternalFiles] = React.useState<File[]>([]);

  const files = value ?? internalFiles;
  const setFiles = onValueChange ?? setInternalFiles;

  const onFileReject = React.useCallback((file: File, message: string) => {
    toast(message, {
      description: `"${file.name.length > 20 ? `${file.name.slice(0, 20)}...` : file.name}" foi rejeitado`,
    });
  }, []);

  const formattedMaxSize = React.useMemo(() => {
    if (maxSize >= 1024 * 1024) return `${Math.round(maxSize / (1024 * 1024))}MB`;
    return `${Math.round(maxSize / 1024)}KB`;
  }, [maxSize]);
  const acceptedTypes = React.useMemo(() => {
    if (!accept) return undefined;
    return Array.isArray(accept) ? accept.join(',') : accept;
  }, [accept]);

  return (
    <FileUpload
      maxFiles={maxFiles}
      maxSize={maxSize}
      accept={acceptedTypes}
      className="w-full"
      value={files}
      onValueChange={setFiles}
      onFileReject={onFileReject}
      multiple
    >
      <FileUploadDropzone>
        <div className="flex flex-col items-center gap-1 text-center">
          <div className="flex items-center justify-center rounded-full border p-2.5">
            <Upload className="text-muted-foreground size-6" />
          </div>
          <p className="text-sm font-medium">Arraste e solte os arquivos aqui</p>
          <p className="text-muted-foreground text-xs">
            Ou clique para procurar (máx. {maxFiles} arquivos, até {formattedMaxSize} cada)
          </p>
        </div>

        <FileUploadTrigger asChild>
          <Button variant="outline" size="sm" className="mt-2 w-fit">
            Selecionar arquivos
          </Button>
        </FileUploadTrigger>
      </FileUploadDropzone>

      <FileUploadList>
        {files.map((file, index) => (
          <FileUploadItem key={index} value={file}>
            <FileUploadItemPreview />
            <FileUploadItemMetadata />
            {(() => {
              const fileKey = getFileKey(file);
              const status = fileStatus?.[fileKey] ?? 'pending';
              const removeDisabled =
                disableRemoveAfterSubmit && status !== 'pending';
              const errorMessage = status === 'error' ? fileErrorMessage?.[fileKey] : undefined;

              return (
                <>
                  <div className="flex min-w-[130px] flex-col items-start gap-1">
                    <span
                      className={`inline-flex rounded-full px-2 py-0.5 text-xs font-medium ${getStatusClassName(status)}`}
                    >
                      {getStatusLabel(status)}
                    </span>
                    {errorMessage && (
                      <span className="text-xs text-red-600" title={errorMessage}>
                        {errorMessage}
                      </span>
                    )}
                  </div>
                  {renderFileControl?.(file)}
                  <FileUploadItemDelete asChild>
                    <Button
                      variant="ghost"
                      size="icon"
                      className="size-7"
                      disabled={removeDisabled}
                    >
                      <X />
                    </Button>
                  </FileUploadItemDelete>
                </>
              );
            })()}
          </FileUploadItem>
        ))}
      </FileUploadList>
    </FileUpload>
  );
}
