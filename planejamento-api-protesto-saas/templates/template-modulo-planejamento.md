# Template — planejamento de módulo `<entidade>`

> Copiar para `modulos/<dominio>/<entidade>.md` e preencher.

## Metadados

| Campo | Valor |
|-------|-------|
| Entidade | `<entidade>` |
| Pacote | `packages/v1/<modulo>/` |
| Prefix HTTP | `/<prefixo>/` |
| DataConfig | `app/src/packages/.../<entidade>DataConfig.ts` |
| Fase | [04-ordem-implementacao.md](../04-ordem-implementacao.md) — Fase N |
| Status | planejado \| em andamento \| concluído |

## Rotas

| Operação | Método | Path (relativo ao prefix) | Auth |
|----------|--------|---------------------------|------|
| index | GET | `/` | sim |
| show | GET | `/{id}/` | sim |
| create | POST | `/` | sim |
| update | PUT | `/{id}/` | sim |
| delete | DELETE | `/{id}/` | sim |

## Regras de negócio (backend)

- 
- 

## Filtros `index` (IndexSchema)

| Campo filtro | Tipo | Origem TS |
|--------------|------|-----------|
| | | |

## Erros esperados

| Código | Condição |
|--------|----------|
| 404 | id inexistente |
| 409 | duplicidade / conflito |
| 422 | payload inválido |

## Tabela Firebird (a confirmar)

| Tabela | PK | Observação |
|--------|-----|------------|
| | | |

## Arquivos a criar

Ver [template-matriz-arquivos-por-entidade.md](./template-matriz-arquivos-por-entidade.md).

## Testes planejados

- [ ] unit: index com filtros válidos/inválidos
- [ ] unit: save/update regras de unicidade
- [ ] unit: delete com dependência → bloqueio

## Dependências

- 

## Notas

- 
