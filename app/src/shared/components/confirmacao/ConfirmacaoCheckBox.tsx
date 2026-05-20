import { Checkbox } from '@/components/ui/checkbox';
import { FormControl, FormField, FormItem, FormLabel } from '@/components/ui/form';

interface ConfirmacaoCheckBoxProps {
  name: string;
  label: string;
  control: any;
}

export function ConfirmacaoCheckBox({ name, label, control }: ConfirmacaoCheckBoxProps) {
  return (
    <FormField
      control={control}
      name={name}
      render={({ field }) => (
        <FormItem className="flex flex-row items-center space-y-0 space-x-3">
          <FormControl>
            <Checkbox
              checked={field.value === 'S'}
              onCheckedChange={(checked) => field.onChange(checked ? 'S' : 'N')}
            />
          </FormControl>
          <FormLabel className="cursor-pointer font-normal">{label}</FormLabel>
        </FormItem>
      )}
    />
  );
}
