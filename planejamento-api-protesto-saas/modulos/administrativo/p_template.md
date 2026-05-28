# PTemplate

| Campo | Valor |
|-------|-------|
| Pacote | `packages/v1/administrativo/` |
| Prefix | `/administrativo/p_template` |
| Tabela | `P_TEMPLATE` |
| Fase | 1 |
| Status | planejado para CRUD inicial |

## Rotas

| Operacao | Metodo | Path |
|----------|--------|------|
| index | GET | `/` |
| show | GET | `/{id}` |
| create | POST | `/` |
| update | PUT | `/{id}` |
| delete | DELETE | `/{id}` |

## Descoberta Firebird

`USE_ORM_FIREBIRD=true`; schema confirmado por `QueryInterface.describe_table`.

| Coluna | Tipo | Obrigatorio | Contrato inicial API |
|--------|------|-------------|----------------------|
| `TEMPLATE_ID` | `NUMERIC(10,2)` | sim | `template_id` |
| `DESCRICAO` | `VARCHAR(60)` | sim | `descricao` |
| `TEXTO` | `BLOB SUB_TYPE BINARY` | nao | fora do CRUD inicial |

FKs: nenhuma encontrada.

## Amostra

| `TEMPLATE_ID` | `DESCRICAO` | `TEXTO` |
|---------------|-------------|---------|
| `2` | `CERTIDAO POSITIVA` | BLOB RTF compactado (`rtf-zlib`) |
| `1` | `CERTIDAO NEGATIVA` | BLOB RTF compactado (`rtf-zlib`) |

## Siglas

Nao ha colunas `CHAR(1)` / `VARCHAR(1)` no escopo do CRUD inicial.

## Regras de negocio

- index: filtros `template_id`, `descricao`; formato3 com `p`, `per_page`, `sort`.
- sort permitido: `template_id`, `descricao`; fallback `template_id.desc`.
- create/update: manipula apenas `descricao`; `TEXTO` nao entra no body.
- index/show: retorna apenas `template_id` e `descricao`; `TEXTO` nao entra nas consultas.
- create: gera `TEMPLATE_ID` via `G_SEQUENCIA` para tabela `P_TEMPLATE` quando nao informado.
- delete: fisico (`DELETE` na tabela).

## Models necessarios

| Tabela Firebird | Arquivo model | Motivo no escopo |
|-----------------|---------------|------------------|
| `P_TEMPLATE` | `model/p_template.py` | Entidade alvo |

## Associacoes planejadas

Nenhuma associacao planejada nesta fase.

## Arquivos

| Camada | Arquivos |
|--------|----------|
| model | `model/p_template.py` |
| schema | `schemas/p_template_schema.py` |
| repositories | `p_template_index_repository.py`, `_show_`, `_save_`, `_update_`, `_delete_` |
| demais | actions, services, controller, endpoint (padrao CRUD) |

Sem arquivos auxiliares em `repositories/p_template/`.

## Postman

Pasta `Administrativo` -> `Template`: All, Create, Get, Update, Delete.

## Debug OnlyOffice (PTemplate)

- Sintoma observado: editor abre, mas exibe `Erro ao baixar arquivo`.
- Causa raiz: o frontend reconstruia `document.url` com base em `title` (`/temp/template_<id>.docx`), porem o backend salva arquivo fisico com nome unico (`p_template_<id>_<hash>.docx`).
- Efeito: o Document Server tentava baixar um arquivo inexistente e retornava erro de download.
- Correcao aplicada:
  - `app/src/packages/administrativo/data/PTemplate/PTemplateOpenEditorData.ts`: passa a preservar `document.url` retornada pela API.
  - `app/src/shared/components/editor/onlyoffice/OnlyOfficeEditor.tsx`: usa `config.document.url` quando disponivel, sem sobrescrever por `title`.
- Verificacao recomendada:
  - no log `Configuração Final do Editor`, confirmar `document.url` com nome fisico completo;
  - abrir esta URL diretamente no navegador e validar download;
  - confirmar callback em `POST /api/v1/administrativo/p_template/{id}/texto/callback` apos salvar no editor.

## Debug OnlyOffice (Docker/EasyPanel)

- Se `document.url` estiver correta e ainda ocorrer `Erro ao baixar arquivo`, validar o Document Server.
- Cenario comum: filtro de seguranca do OnlyOffice bloqueando download por IP privado (ex.: `192.168.x.x`).
- Sinais nos logs do container:
  - `downloadFile` com falha;
  - mensagens contendo `private ip address` ou bloqueio por `request-filtering-agent`.
- Correcao operacional no container:
  - habilitar `ALLOW_PRIVATE_IP_ADDRESS=true`;
  - habilitar `ALLOW_META_IP_ADDRESS=true` (quando necessario);
  - reiniciar o container.
- Alternativa equivalente: ajustar `/etc/onlyoffice/documentserver/local.json` com:
  - `services.CoAuthoring.request-filtering-agent.allowPrivateIPAddress = true`
  - `services.CoAuthoring.request-filtering-agent.allowMetaIPAddress = true`
