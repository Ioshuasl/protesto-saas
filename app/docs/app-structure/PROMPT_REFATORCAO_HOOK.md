# SCRIPT DE REFATORAÇÃO - CAMADA HOOKS

Objetivo:
Refatorar hooks do módulo `<MODULO_NOME>` com o padrão de:
- documentacao-markdown/PADRAO_CAMADA_HOOKS_GFeriado.md
- documentacao-markdown/PADRAO_REFATORACAO_GFeriado_RESUMO.md

Escopo:
- Pasta alvo: `<PROJECT_PATH>/src/packages/<PACOTE>/hooks/<MODULO_NOME>/`

Padrão obrigatório:
1. Usar `useState` para estado local.
2. Importar interface de domínio.
3. Importar `useResponse` e usar `setResponse`.
4. Em cada ação:
   - `const response = await ...`
   - atualizar estado local quando aplicável
   - `setResponse(response)`
   - retornar `response` quando aplicável
5. Manter naming consistente:
   - `use<Modulo>ReadHook`
   - `use<Modulo>SaveHook`
   - `use<Modulo>Delete/RemoveHook`

Regras de aderência:
- Seguir estrutura visual e ordem lógica do módulo de referência.
- Não adicionar complexidade extra sem necessidade (ex.: callbacks e estados extras fora do padrão definido).

Entregáveis:
- Hooks Read/Save/Delete (ou Remove) no padrão.
- Sem quebra de contrato para componentes consumidores.
- Lint sem erro.

Checklist final:
- [ ] `useResponse` presente em todos os hooks de ação.
- [ ] `setResponse(response)` após chamadas assíncronas.
- [ ] Estado local alinhado ao tipo do hook.
- [ ] Nomes e assinatura consistentes.
- [ ] ReadLints sem erros.
