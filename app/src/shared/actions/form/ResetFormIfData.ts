import { FieldValues, UseFormReturn } from 'react-hook-form';

import normalizeFormData from './normalizeFormData';

export function ResetFormIfData<T extends FieldValues>(form: UseFormReturn<T>, data?: T | null) {
  if (data == null) {
    form.reset();
    return;
  }
  const normalized = normalizeFormData(data);
  const currentValues = form.getValues();
  const isDifferent = JSON.stringify(currentValues) !== JSON.stringify(normalized);
  if (isDifferent) {
    form.reset(normalized as T);
  }
}
