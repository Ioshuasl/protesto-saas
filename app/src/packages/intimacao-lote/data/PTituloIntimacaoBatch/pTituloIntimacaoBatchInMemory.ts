import db from "@/db.json";
import type { PTituloInterface } from "@/packages/administrativo/interfaces/PTitulo/PTituloInterface";
import type { PTituloIntimacaoBatchInterface } from "@/packages/intimacao-lote/interface/PTituloIntimacaoBatch/PTituloIntimacaoBatchInterface";

interface PessoaVinculoRecord {
  titulo_id: number;
  tipo_vinculo?: string;
  nome?: string;
  cpfcnpj?: string;
}

function mapBatchTitulosFromDb(): PTituloIntimacaoBatchInterface[] {
  const titulos = (db.titulos as unknown as PTituloInterface[]) ?? [];
  const vinculos = (db.pessoas_vinculo as unknown as PessoaVinculoRecord[]) ?? [];

  return titulos.map((titulo) => {
    const apresentanteVinculo =
      vinculos.find((item) => item.titulo_id === titulo.titulo_id && item.tipo_vinculo === "A") ??
      vinculos.find((item) => item.titulo_id === titulo.titulo_id);

    return {
      titulo_id: titulo.titulo_id,
      numero_titulo: titulo.numero_titulo,
      nosso_numero: titulo.nosso_numero,
      numero_apontamento: titulo.numero_apontamento,
      data_apontamento: titulo.data_apontamento,
      data_intimacao: titulo.data_intimacao,
      data_cadastro: titulo.data_cadastro,
      valor_titulo: titulo.valor_titulo,
      banco_id: titulo.banco_id,
      apresentante: apresentanteVinculo?.nome,
      cpfcnpj: apresentanteVinculo?.cpfcnpj,
      situacao_aceite: titulo.situacao_aceite,
    };
  });
}

export const pTituloIntimacaoBatchListRef: { current: PTituloIntimacaoBatchInterface[] } = {
  current: mapBatchTitulosFromDb(),
};
