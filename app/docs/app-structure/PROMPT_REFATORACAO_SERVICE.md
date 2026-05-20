# SCRIPT DE REFATORAÇÃO - CAMADA SERVICE

Objetivo:
Refatorar os arquivos de service do módulo `<MODULO_NOME>` para seguir exatamente o padrão em:
- documentacao-markdown/PADRAO_CAMADA_SERVICE_GFeriado.md
- documentacao-markdown/PADRAO_REFATORACAO_GFeriado_RESUMO.md

Escopo:
- Pasta alvo: `<PROJECT_PATH>/src/packages/<PACOTE>/services/<MODULO_NOME>/`

Estrutura obrigatória por arquivo:
1. Primeira linha: `'use server';`
2. Import do Data correspondente.
3. Import de `withClientErrorHandler`.
4. Criar função interna `execute<Modulo><Acao>Service(...)`.
5. Dentro da função:
   - `const response = await <Modulo><Acao>Data(...)`
   - `return response`
6. Export:
   - `export const <Modulo><Acao>Service = withClientErrorHandler(execute<...>)`

Restrições:
- Não criar retorno manual com `status/message/data` na service (se o padrão do módulo for pass-through).
- Não mover regra de mock/API para service (isso fica no data).
- Assinatura da service deve espelhar a assinatura da data.

Entregáveis:
- Todos os services do módulo no padrão.
- Lint sem erro.

Checklist final:
- [ ] `'use server';` presente.
- [ ] Função `execute...Service` criada.
- [ ] Pass-through mantido.
- [ ] Export com `withClientErrorHandler`.
- [ ] Assinaturas alinhadas com data.
- [ ] ReadLints sem erros.
