import { PCERTIDAO_ENDPOINTS } from "@/packages/certidao/data/PCertidao/pCertidaoDataConfig";
import {
  type PCertidaoConsultaApresentantePayload,
  type PCertidaoConsultaApresentanteResult,
} from "@/packages/certidao/interface/PCertidao/PCertidaoConsultaApresentanteInterface";
import API from "@/shared/services/api/Api";
import { Methods } from "@/shared/services/api/enums/ApiMethodEnum";

export async function PCertidaoConsultaApresentanteData(
  payload: PCertidaoConsultaApresentantePayload,
): Promise<PCertidaoConsultaApresentanteResult> {
  const params = new URLSearchParams();
  params.set("apresentante", payload.apresentante.trim());
  params.set("cpfcnpj", payload.cpfcnpj.trim());
  if (payload.data_inicio) params.set("data_inicio", payload.data_inicio);
  if (payload.data_fim) params.set("data_fim", payload.data_fim);

  const api = new API();
  const response = await api.send({
    method: Methods.GET,
    endpoint: `${PCERTIDAO_ENDPOINTS.consultaApresentante}?${params.toString()}`,
  });

  if (Number(response?.status) >= 200 && Number(response?.status) < 300 && response?.data) {
    return response.data as PCertidaoConsultaApresentanteResult;
  }

  throw new Error(response?.message || "Não foi possível consultar o apresentante");
}
