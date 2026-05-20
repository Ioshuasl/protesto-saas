import MultiplicarValorPorQuantidadeInterface from './MultiplicarValorPorQuantidadeInterface';

export default function MultiplicarValorPorQuantidade(
  data: MultiplicarValorPorQuantidadeInterface,
): number {
  if (!data.valor || !data.quantidade) return 0;
  return Number((data.valor * data.quantidade).toFixed(2));
}
