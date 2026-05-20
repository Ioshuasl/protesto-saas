# Endpoints dos `DataConfig.ts` com detalhamento individual

Este documento descreve cada endpoint encontrado nos arquivos `*DataConfig.ts` com foco em:

- papel no fluxo (principalmente edital/intimacao/protesto);
- responsabilidade exata da API backend;
- regras de validacao, efeitos e erros esperados.

## Contrato base recomendado (todos os endpoints)

- **Autenticacao/autorizacao** por perfil.
- **Resposta padrao** no formato `{ status, message, data }`.
- **Auditoria**: registrar usuario, data/hora, acao e estado anterior/novo.
- **Validacao de negocio** antes de persistir.
- **Erros previsiveis** com mensagens claras (400/404/409/422).

### Regra obrigatoria para todos os endpoints `index`

Todos os endpoints `index` (camada `data`) devem oferecer **suporte a filtro de busca** alinhado com as tipagens de cada modulo.

- O backend deve aceitar parametros de filtro coerentes com a interface/tipo do modulo (ex.: ids, descricao, codigo, datas, status, situacao).
- O backend nao deve aceitar filtros genericos sem validacao de tipo.
- O backend deve validar tipos de entrada e retornar erro claro para filtro invalido.
- O backend deve manter consistencia entre nomes de filtros e nomes de campos utilizados nos tipos do frontend.
- O backend deve permitir composicao de filtros (quando aplicavel), mantendo paginacao e ordenacao.

---

## 1) Modulo `GFeriado` (`administrativo/g_feriado/`)

### Endpoint: `index` (`GET administrativo/g_feriado/`)
- **Objetivo**: listar feriados para composicao de calendario util no calculo de prazos do fluxo.
- **Backend deve fazer**:
  - retornar feriados ativos e/ou historicos conforme filtro;
  - ordenar por data ascendente;
  - suportar filtro por ano e abrangencia.
- **Erros esperados**: 401/403 quando sem permissao.

### Endpoint: `show` (`GET administrativo/g_feriado/:id/`)
- **Objetivo**: detalhar um feriado especifico para consulta/edicao.
- **Backend deve fazer**:
  - retornar registro completo;
  - retornar 404 se id inexistente.

### Endpoint: `create` (`POST administrativo/g_feriado/`)
- **Objetivo**: cadastrar feriado.
- **Backend deve fazer**:
  - validar data obrigatoria;
  - impedir duplicidade da mesma data no mesmo escopo;
  - persistir autor e timestamp.
- **Erros esperados**: 409 para duplicidade; 422 para payload invalido.

### Endpoint: `update` (`PUT/PATCH administrativo/g_feriado/:id/`)
- **Objetivo**: atualizar feriado existente.
- **Backend deve fazer**:
  - validar conflito de data;
  - manter trilha de auditoria;
  - preservar integridade de calculos ja consolidados.

### Endpoint: `delete` (`DELETE administrativo/g_feriado/:id/`)
- **Objetivo**: remover/inativar feriado.
- **Backend deve fazer**:
  - preferir soft delete se o feriado ja foi usado em prazo;
  - impedir exclusao fisica quando houver dependencia legal.

---

## 2) Modulo `PBanco` (`administrativo/p_banco/`)

### `index` (`GET administrativo/p_banco/`)
- Lista bancos para selecao no titulo.
- Backend: paginar, filtrar por descricao/codigo e retornar somente registros validos para uso.

### `show` (`GET administrativo/p_banco/:id/`)
- Consulta banco especifico.
- Backend: retornar 404 para id inexistente.

### `create` (`POST administrativo/p_banco/`)
- Cadastra banco.
- Backend: validar unicidade de codigo bancario e campos obrigatorios.

### `update` (`PUT/PATCH administrativo/p_banco/:id/`)
- Atualiza banco.
- Backend: bloquear alteracao que quebre titulos existentes (ou versionar regras).

### `delete` (`DELETE administrativo/p_banco/:id/`)
- Remove/inativa banco.
- Backend: impedir exclusao se houver titulo vinculado.

---

## 3) Modulo `PEspecie` (`administrativo/p_especie/`)

### `index` (`GET administrativo/p_especie/`)
- Lista especies para classificacao de titulos.

### `show` (`GET administrativo/p_especie/:id/`)
- Detalha especie.

### `create` (`POST administrativo/p_especie/`)
- Cria especie com regras de negocio associadas.
- Backend: validar codigo/sigla unicos.

### `update` (`PUT/PATCH administrativo/p_especie/:id/`)
- Atualiza especie.
- Backend: preservar compatibilidade com titulos ja cadastrados.

### `delete` (`DELETE administrativo/p_especie/:id/`)
- Remove/inativa especie.
- Backend: bloquear exclusao com dependencia.

---

## 4) Modulo `POcorrencias` (`administrativo/p_ocorrencias/`)

### `index` (`GET administrativo/p_ocorrencias/`)
- Lista ocorrencias/status disponiveis para andamento.

### `show` (`GET administrativo/p_ocorrencias/:id/`)
- Exibe detalhes de ocorrencia.

### `create` (`POST administrativo/p_ocorrencias/`)
- Cadastra ocorrencia.
- Backend: validar codigo unico e classificacao.

### `update` (`PUT/PATCH administrativo/p_ocorrencias/:id/`)
- Atualiza ocorrencia.
- Backend: nao permitir alteracao que invalide historico.

### `delete` (`DELETE administrativo/p_ocorrencias/:id/`)
- Remove/inativa ocorrencia.
- Backend: impedir exclusao de ocorrencia ja usada.

---

## 5) Modulo `PMotivos` (`administrativo/p_motivos/`)

### `index` (`GET administrativo/p_motivos/`)
- Lista motivos de apontamento.

### `show` (`GET administrativo/p_motivos/:id/`)
- Detalha motivo.

### `create` (`POST administrativo/p_motivos/`)
- Cria motivo.
- Backend: validar descricao/codigo.

### `update` (`PUT/PATCH administrativo/p_motivos/:id/`)
- Atualiza motivo.
- Backend: manter historico de alteracao.

### `delete` (`DELETE administrativo/p_motivos/:id/`)
- Remove/inativa motivo.
- Backend: bloquear exclusao em uso.

---

## 6) Modulo `PMotivosCancelamento` (`administrativo/p_motivos_cancelamento/`)

### `index` (`GET administrativo/p_motivos_cancelamento/`)
- Lista motivos aceitos para cancelamento/desistencia.

### `show` (`GET administrativo/p_motivos_cancelamento/:id/`)
- Detalha motivo de cancelamento.

### `create` (`POST administrativo/p_motivos_cancelamento/`)
- Cria motivo de cancelamento.
- Backend: padronizar classificacao e obrigatoriedades.

### `update` (`PUT/PATCH administrativo/p_motivos_cancelamento/:id/`)
- Atualiza motivo.

### `delete` (`DELETE administrativo/p_motivos_cancelamento/:id/`)
- Remove/inativa motivo.
- Backend: impedir exclusao com uso historico.

---

## 7) Modulo `PPessoa` (`administrativo/p_pessoa/`)

### `index` (`GET administrativo/p_pessoa/`)
- Lista pessoas para vinculos no titulo (devedor, apresentante etc.).

### `show` (`GET administrativo/p_pessoa/:id/`)
- Detalha pessoa.

### `create` (`POST administrativo/p_pessoa/`)
- Cadastra pessoa.
- Backend: validar CPF/CNPJ, tipo de pessoa e campos obrigatorios.

### `update` (`PUT/PATCH administrativo/p_pessoa/:id/`)
- Atualiza pessoa.
- Backend: tratar conflito de documento duplicado.

### `delete` (`DELETE administrativo/p_pessoa/:id/`)
- Remove/inativa pessoa.
- Backend: bloquear quando houver vinculo com titulo.

---

## 8) Modulo `PLivroAndamento` (`administrativo/p_livro_andamento/`)

### `index` (`GET administrativo/p_livro_andamento/`)
- Lista livros/andamentos disponiveis.

### `show` (`GET administrativo/p_livro_andamento/:id/`)
- Detalha livro.

### `create` (`POST administrativo/p_livro_andamento/`)
- Cria livro.
- Backend: validar numeracao e disponibilidade.

### `update` (`PUT/PATCH administrativo/p_livro_andamento/:id/`)
- Atualiza livro.

### `delete` (`DELETE administrativo/p_livro_andamento/:id/`)
- Remove/inativa livro.
- Backend: impedir exclusao em uso.

---

## 9) Modulo `PLivroNatureza` (`administrativo/p_livro_natureza/`)

### `index` (`GET administrativo/p_livro_natureza/`)
- Lista naturezas de livro.

### `show` (`GET administrativo/p_livro_natureza/:id/`)
- Detalha natureza.

### `create` (`POST administrativo/p_livro_natureza/`)
- Cadastra natureza.

### `update` (`PUT/PATCH administrativo/p_livro_natureza/:id/`)
- Atualiza natureza.

### `delete` (`DELETE administrativo/p_livro_natureza/:id/`)
- Remove/inativa natureza.
- Backend: nao quebrar compatibilidade com atos ja lavrados.

---

## 10) Modulo `GUsuario` (`administrativo/g_usuario/`)

### `index` (`GET administrativo/g_usuario/`)
- Lista usuarios administrativos.

### `show` (`GET administrativo/g_usuario/:id/`)
- Detalha usuario.

### `create` (`POST administrativo/g_usuario/`)
- Cria usuario.
- Backend: validar login/email unicos e perfil.

### `update` (`PUT/PATCH administrativo/g_usuario/:id/`)
- Atualiza usuario.
- Backend: auditar alteracoes de perfil e status.

### `delete` (`DELETE administrativo/g_usuario/:id/`)
- Remove/inativa usuario.
- Backend: preferir inativacao para historico.

---

## 11) Modulo central `PTitulo` (`administrativo/p_titulo/`)

## Fluxo de edital e endpoints individuais

### Regra obrigatoria de retorno (todos os endpoints de acoes de botao)
- Todos os endpoints acionados pelos botoes de acao do fluxo de `PTitulo` devem retornar o **titulo completo atualizado** no campo `data` da resposta.
- Esse retorno completo e obrigatorio para permitir re-render imediato da tela e, em seguida, revalidacao da leitura (`show`) para garantir consistencia visual e de negocio.
- Nao retornar payload parcial (ex.: apenas status/mensagem) para endpoints de acao; o frontend depende do objeto completo do titulo.

### `index` (`GET administrativo/p_titulo/`)
- **Etapa no fluxo**: entrada/consulta da carteira.
- **Objetivo**: listar titulos com campos de triagem (ocorrencia, datas, partes, valores).
- **Backend deve fazer**:
  - suportar filtros por fase (`apontado`, `intimacao`, `protestado`, etc.);
  - permitir ordenacao e paginacao;
  - retornar payload suficiente para listagem sem chamadas extras.

### `show` (`GET administrativo/p_titulo/:id/`)
- **Etapa no fluxo**: analise detalhada antes de decidir acao.
- **Objetivo**: abrir detalhe completo do titulo.
- **Backend deve fazer**:
  - retornar dados integrais do titulo, inclusive campos de prazo e andamento;
  - incluir referencias relacionadas necessarias para UI;
  - retornar 404 para id inexistente.

### `selos` (`GET administrativo/p_titulo/:id/selos`)
- **Etapa no fluxo**: composicao de custas/atos.
- **Objetivo**: listar selos vinculados ao titulo.
- **Backend deve fazer**:
  - retornar selos com status, valor e metadados;
  - garantir rastreabilidade (origem, data e usuario).

### `updateStatus` (`PUT administrativo/p_titulo/:id/status/`)
- **Etapa no fluxo**: manutencao de estado geral.
- **Objetivo**: atualizar status consolidado quando aplicavel.
- **Backend deve fazer**:
  - validar transicao permitida pela maquina de estados;
  - registrar historico de transicao;
  - recusar transicoes invalidas (409/422).

### `apontarTitulo` (`PUT administrativo/p_titulo/apontar_titulo/:id`)
- **Etapa no fluxo**: abertura do fluxo operacional do titulo.
- **Objetivo**: apontar titulo que ainda nao iniciou andamento (sem apontamento/intimacao/protesto/cancelamento).
- **Backend deve fazer**:
  - validar pre-condicao de "sem andamento" para evitar apontamento duplicado;
  - gerar/preencher dados de apontamento (ex.: `numero_apontamento`, `data_apontamento`) conforme regra interna;
  - atualizar situacao/ocorrencia para estado de apontamento de forma atomica e auditavel.

### `proximoNumeroApontamento` (`GET administrativo/p_titulo/proximo_numero_apontamento/`)
- **Etapa no fluxo**: preparacao do apontamento (preenchimento de dialog/form).
- **Objetivo**: retornar o proximo numero de apontamento disponivel na sequencia oficial do cartorio.
- **Backend deve fazer**:
  - consultar a sequencia corrente em fonte transacional confiavel (nao derivar apenas de cache do cliente);
  - devolver payload claro com o campo `proximo_numero_apontamento`;
  - garantir que o numero retornado respeite regras de sequencia (saltos permitidos, reservas e concorrencia);
  - auditar requisicoes em ambiente operacional quando a sequencia for sensivel.

### `intimarTitulo` (`PUT administrativo/p_titulo/intimar_titulo/:id`)
- **Etapa no fluxo**: inicio formal da intimacao.
- **Objetivo**: mover titulo de apontado para intimacao/triduo.
- **Backend deve fazer**:
  - validar pre-condicoes: apontamento completo, dados minimos obrigatorios;
  - calcular data-base de intimacao e prazos;
  - atualizar ocorrencia/situacao de forma atomica.

### `aceiteEdital` (`PUT administrativo/p_titulo/aceite_edital/:id`)
- **Etapa no fluxo**: marco de aceite/publicacao de edital.
- **Objetivo**: registrar aceite/edital durante a intimacao.
- **Backend deve fazer**:
  - validar se titulo esta em etapa elegivel;
  - persistir data/hora, usuario e origem da acao;
  - impedir aceite duplicado sem regra de retrabalho.

### `voltarApontamento` (`PUT administrativo/p_titulo/voltar_apontamento/:id`)
- **Etapa no fluxo**: rollback da intimacao para apontamento.
- **Objetivo**: reabrir fase de apontamento.
- **Backend deve fazer**:
  - permitir apenas quando titulo estiver em estado reversivel;
  - limpar campos dependentes de intimacao/protesto conforme regra;
  - gravar justificativa de retorno.

### `voltarIntimacao` (`PUT administrativo/p_titulo/voltar_intimacao/:id`)
- **Etapa no fluxo**: rollback de protesto para intimacao.
- **Objetivo**: desfazer protesto e retornar para etapa anterior.
- **Backend deve fazer**:
  - validar permissao e elegibilidade de reversao;
  - desfazer campos de protesto (livro/folha/data/numero) quando aplicavel;
  - recalcular ocorrencia para estado de intimacao.

### `liquidarTitulo` (`PUT administrativo/p_titulo/liquidar_titulo/:id`)
- **Etapa no fluxo**: desfecho por liquidacao/pagamento.
- **Objetivo**: encerrar titulo como liquidado.
- **Backend deve fazer**:
  - validar dados financeiros;
  - definir data de liquidacao/pagamento;
  - encerrar fluxo para impedir novas acoes incompatíveis.

### `desistirTitulo` (`PUT administrativo/p_titulo/desistir_titulo/:id`)
- **Etapa no fluxo**: desfecho por desistencia.
- **Objetivo**: encerrar fluxo por desistencia formal.
- **Backend deve fazer**:
  - exigir motivo de desistencia (quando regra exigir);
  - registrar data e operador;
  - atualizar ocorrencia final de forma auditavel.

### `cancelarTitulo` (`PUT administrativo/p_titulo/cancelar_titulo/:id`)
- **Etapa no fluxo**: desfecho por cancelamento.
- **Objetivo**: cancelar titulo por regra legal/operacional.
- **Backend deve fazer**:
  - exigir motivo de cancelamento;
  - validar elegibilidade (ex.: nao permitir em status final imutavel);
  - bloquear quaisquer evolucoes futuras sem reabertura.

### `voltarProtesto` (`PUT administrativo/p_titulo/voltar_protesto/:id`)
- **Etapa no fluxo**: rollback de cancelamento para protesto.
- **Objetivo**: desfazer cancelamento completo (com protesto registrado) e retornar o titulo ao estado protestado.
- **Backend deve fazer**:
  - validar elegibilidade de retorno (cancelamento com `data_cancelamento` + `motivo_cancelamento` e protesto completo previamente registrado);
  - desfazer campos de cancelamento (`data_cancelamento`, `motivo_cancelamento`, `numero_cancelamento`) mantendo rastreabilidade;
  - restaurar situacao/ocorrencia coerente com "protestado" sem perda de historico.

### `protestarTitulo` (`PUT administrativo/p_titulo/protestar_titulo/:id`)
- **Etapa no fluxo**: conclusao do protesto.
- **Objetivo**: finalizar processo com registro de protesto.
- **Backend deve fazer**:
  - validar cumprimento de intimacao/edital e prazo legal;
  - gerar/persistir dados de protesto (livro, folha, numero, data);
  - publicar ocorrencia final e eventos de integracao.

---

## 12) Lotes de operacao por fase

### Modulo `PTituloApontamentoBatch` (`apontamento-batch/p_titulo_apontamento_batch/`)

#### `index` (`GET apontamento-batch/p_titulo_apontamento_batch/`)
- **Objetivo**: listar lotes de apontamento e seus itens.
- **Backend deve fazer**:
  - retornar status do lote (processando, concluido, erro parcial);
  - retornar detalhe por item com motivo de falha;
  - suportar filtros por periodo, protocolo e origem.

### Modulo `PTituloIntimacaoBatch` (`intimacao-batch/p_titulo_intimacao_batch/`)

#### `index` (`GET intimacao-batch/p_titulo_intimacao_batch/`)
- **Objetivo**: listar lotes de intimacao.
- **Backend deve fazer**:
  - trazer titulo, etapa, prazo e resultado por item;
  - marcar itens aptos/não aptos para proxima etapa;
  - manter idempotencia para reprocessamento.

### Modulo `PTituloProtestarBatch` (`protesto-batch/p_titulo_protestar_batch/`)

#### `index` (`GET protesto-batch/p_titulo_protestar_batch/`)
- **Objetivo**: listar lotes destinados ao protesto.
- **Backend deve fazer**:
  - validar elegibilidade de cada titulo;
  - retornar consolidado de sucesso/erro;
  - manter consistencia transacional por lote/arquivo.

---

## 13) Certidao

### Modulo `PCertidao` (`certidao/p_certidao/`)

#### `index` (`GET certidao/p_certidao/`)
- Lista certidoes emitidas.
- Backend: suportar filtros por periodo, tipo e status.

#### `show` (`GET certidao/p_certidao/:id/`)
- Detalha certidao.
- Backend: retornar conteudo completo e metadados de emissao.

#### `create` (`POST certidao/p_certidao/`)
- Emite/cadastra certidao.
- Backend: validar elegibilidade do titulo e gerar identificador unico.

#### `update` (`PUT/PATCH certidao/p_certidao/:id/`)
- Atualiza certidao.
- Backend: limitar campos editaveis por regra legal e auditar alteracao.

#### `consulta_apresentante` (`GET certidao/p_certidao/consulta_apresentante/`)
- Consulta titulos para emissão de certidao com base em **apresentante + cpfcnpj + periodo**.
- Backend deve:
  - receber e validar query params: `apresentante`, `cpfcnpj`, `data_inicio`, `data_fim`;
  - aplicar regra de periodo para busca (padrão operacional de 5 anos, quando não informado pelo cliente);
  - retornar estrutura de análise para emissão:
    - `titulosPorDocumento`: títulos cujo documento confere com o informado;
    - `candidatosHomonimia`: títulos por nome semelhante/igual com documento diferente;
  - considerar apenas títulos elegíveis para certidão conforme regra de protesto ativo;
  - manter resposta padronizada para uso direto por hooks/services.

---

## 14) Integracao CRA

### Modulo `CraImportacao` (`cra/importacao/`)

#### `save` (`POST cra/importacao/`)
- **Objetivo**: receber arquivo/payload para pipeline CRA.
- **Backend deve fazer**:
  - validar schema e formato de entrada;
  - enfileirar processamento quando volumoso;
  - devolver protocolo para rastreio.

### Modulo `PTituloArquivo` (`cra/p_arquivo_titulo/`)

#### `index` (`GET cra/p_arquivo_titulo/`)
- Lista arquivos de titulo integrados com CRA.
- Backend: retornar metadados de lote, origem e status.

#### `show` (`GET cra/p_arquivo_titulo/:id/`)
- Detalha arquivo especifico.
- Backend: incluir relacao de titulos e resultado de processamento.

### Modulo `PRetornoCra` (`cra/retorno/`)

#### `index` (`GET cra/retorno/`)
- **Objetivo**: consultar retornos da CRA.
- **Backend deve fazer**:
  - mapear retorno externo para status interno;
  - exibir erro tecnico e erro de negocio separadamente;
  - permitir filtros por protocolo/lote/titulo.

---

## 15) Flags de mock e requisito de compatibilidade

Cada `DataConfig.ts` possui flag `NEXT_PUBLIC_USE_MOCK_*`.  
Para troca transparente de mock para API real, o backend deve manter:

- rotas exatamente como declaradas;
- semantica de negocio equivalente;
- contrato de resposta consistente para hooks/services atuais.

