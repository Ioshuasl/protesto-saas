// ConfirmacaoCheckBoxForm.tsx
'use client';

import { Checkbox } from '@/components/ui/checkbox';

import ConfirmacaoCheckBoxFormInterface from './interfaces/ConfirmacaoCheckBoxFormInterface';

export default function ConfirmacaoCheckBoxForm({
  field,
  label,
}: ConfirmacaoCheckBoxFormInterface) {
  const checked = field.value === 'S';
  return (
    <div className="flex items-center gap-2">
      <Checkbox
        className='cursor-pointer'
        checked={checked}
        onCheckedChange={(value) => {
          field.onChange(value ? 'S' : 'N');
        }}
      />
      <span className="text-sm font-medium">{label}</span>
    </div>
  );
}
