import type { SearchComboboxOption } from "@/packages/administrativo/components/shared/SearchComboboxSelect";
import type { PTituloSelectOption } from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormSchema";
import {
  ensureTituloSelectOption,
  mergeTituloSelectOptionLists,
} from "@/packages/administrativo/schemas/PTitulo/PTituloDetailsFormUtils";

export type ComboboxOptionSource = {
  value: string;
  label: string;
  searchValue?: string;
};

export function buildSearchComboboxOptions(params: {
  fromFetch: ComboboxOptionSource[];
  optionsOverride?: PTituloSelectOption[];
  value?: string;
  selectedLabel?: string;
}): SearchComboboxOption[] {
  const searchByValue = new Map(
    params.fromFetch.map((item) => [
      item.value,
      item.searchValue ?? `${item.label} ${item.value}`,
    ]),
  );
  const merged = mergeTituloSelectOptionLists(
    params.fromFetch.map(({ value, label }) => ({ value, label })),
    params.optionsOverride,
  );
  const ensured = ensureTituloSelectOption(merged, params.value, params.selectedLabel);
  return ensured.map((option) => ({
    value: option.value,
    label: option.label,
    searchValue: searchByValue.get(option.value) ?? `${option.label} ${option.value}`,
  }));
}
