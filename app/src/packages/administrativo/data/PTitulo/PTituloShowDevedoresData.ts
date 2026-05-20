import db from "@/db.json";
import { pPessoaVinculoListRef } from '@/packages/administrativo/data/PTitulo/ptituloPessoasVinculoInMemory';
import {
  PTITULO_FAKE_ENDPOINTS,
  isPTituloMockDataEnabled,
} from '@/packages/administrativo/data/PTitulo/ptituloDataConfig';
import type { PPessoaVinculoInterface } from '@/packages/administrativo/interfaces/PPessoaVinculo/PPessoaVinculoInterface';
import type { PPessoaInterface } from '@/packages/administrativo/interfaces/PPessoa/PPessoaInterface';
import type { PTituloShowDevedoresItem } from '@/packages/administrativo/interfaces/PTitulo/PTituloShowDevedoresItem';
import { mockDbDelay } from '@/packages/administrativo/shared/mockDbDelay';
import { withClientErrorHandler } from '@/shared/actions/withClientErrorHandler/withClientErrorHandler';
import API from '@/shared/services/api/Api';
import { Methods } from '@/shared/services/api/enums/ApiMethodEnum';

const pessoasList: PPessoaInterface[] = [...(db.pessoas as unknown as PPessoaInterface[])];

function mapVinculoToDevedor(item: PPessoaVinculoInterface): PTituloShowDevedoresItem {
  const pessoa = pessoasList.find((p) => Number(p.pessoa_id) === Number(item.pessoa_id));
  return {
    titulo_id: Number(item.titulo_id ?? 0),
    pessoa_vinculo_id: item.pessoa_vinculo_id,
    devedor_nome: item.nome ?? pessoa?.nome,
    devedor_cpfcnpj: item.cpfcnpj ?? pessoa?.cpfcnpj,
    devedor_tipo_aceite: (item.devedor_tipo_aceite as "A" | "E" | undefined) ?? undefined,
    devedor_data_aceite: item.devedor_data_aceite,
  };
}

export async function PTituloShowDevedoresData(tituloId: number): Promise<PTituloShowDevedoresItem[]> {
  if (!isPTituloMockDataEnabled()) {
    const api = new API();
    const apiCall = withClientErrorHandler(async () =>
      api.send({
        method: Methods.GET,
        endpoint: PTITULO_FAKE_ENDPOINTS.showDevedores(tituloId),
      }),
    );
    const response = await apiCall();
    if (
      Number(response?.status) >= 200 &&
      Number(response?.status) < 300 &&
      Array.isArray(response?.data)
    ) {
      return (response.data as PPessoaVinculoInterface[]).map(mapVinculoToDevedor);
    }
  }

  await mockDbDelay(500);

  return pPessoaVinculoListRef.current
    .filter((vinculo) => Number(vinculo.titulo_id) === tituloId && (vinculo.tipo_vinculo ?? "").toUpperCase() === "D")
    .map(mapVinculoToDevedor)
    .filter((devedor) => Boolean(devedor.devedor_nome || devedor.devedor_cpfcnpj));
}

