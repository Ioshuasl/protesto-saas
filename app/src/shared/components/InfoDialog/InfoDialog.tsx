'use client';

import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog';
import { InfoDialogContent, renderInfoContent } from '@/shared/components/InfoDialog/utils/content';

interface InfoDialogProps {
  isOpen: boolean;
  title: string;
  description?: string;
  message?: string;
  content?: InfoDialogContent;
  onOpenChange?: (open: boolean) => void;
}

export default function InfoDialog({ isOpen, title, description, message, content, onOpenChange }: InfoDialogProps) {
  return (
    <Dialog open={isOpen} onOpenChange={onOpenChange}>
      <DialogContent className="sm:max-w-[640px]">
        <DialogHeader>
          <DialogTitle>{title}</DialogTitle>
          {description ? <DialogDescription>{description}</DialogDescription> : null}
        </DialogHeader>

        {message ? <p className="text-sm text-muted-foreground">{message}</p> : null}
        {renderInfoContent(content)}
      </DialogContent>
    </Dialog>
  );
}
