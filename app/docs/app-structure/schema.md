# Schema

## Finalidade

O **`GCartorioSchema`** define o **contrato de validação e estrutura de dados** para a entidade `GCartorio`.
Ele garante que todas as informações manipuladas no frontend — seja em formulários, hooks ou serviços — estejam **tipadas, validadas e consistentes** com o domínio do sistema.

---

## Responsabilidades

* Validar os campos do objeto `GCartorio` conforme as regras definidas.
* Garantir a integridade dos dados manipulados na criação, edição ou exibição de registros.
* Servir como **fonte única de verdade (Single Source of Truth)** para a estrutura de dados da entidade.
* Fornecer o tipo derivado `GCartorioFormValues` para uso em formulários e integração com hooks ou APIs.

---

## Características Técnicas

* Construído com a biblioteca **Zod**, especializada em validação e tipagem em tempo de execução.
* Define um **objeto de schema** (`z.object`) com todos os campos opcionais, permitindo flexibilidade nas operações CRUD.
* É amplamente utilizado em:

  * **Formulários:** validação e tipagem de entrada de dados.
  * **Hooks:** garantia de consistência ao salvar ou atualizar registros.
  * **Serviços:** validação antes do envio ao backend.
* Exporta o tipo `GCartorioFormValues` através de `z.infer`, mantendo o alinhamento entre o schema e a tipagem TypeScript.

---

## Código

```typescript
import z from "zod";

export const GCartorioSchema = z.object({
  cartorio_id: z.number().optional(),
  seq: z.string().optional(),
  cns: z.string().optional(),
  cnpj: z.string().optional(),
  denominacao_serventia: z.string().optional(),
  status_serventia: z.number().optional(),
  atribuicao: z.string().optional(),
  uf: z.string().optional(),
  ...
});

export type GCartorioFormValues = z.infer<typeof GCartorioSchema>;
```

---

## Fluxo de Utilização

1. O schema é importado por formulários ou hooks (`GCartorioForm`, `useGCartorioSaveHook`).
2. Ao enviar dados, o schema valida o objeto conforme as regras definidas.
3. Caso algum campo esteja inválido, o Zod gera mensagens de erro para exibição no formulário.
4. Quando válido, o objeto é convertido automaticamente para o tipo `GCartorioFormValues`.
5. Esse tipo é então usado em requisições HTTP ou armazenamento local com segurança e consistência.

---

## Conclusão

O **`GCartorioSchema`** é o núcleo da **camada de validação e modelagem de domínio** do frontend.
Ele assegura que os dados trafeguem de forma consistente entre formulários, hooks e serviços,
garantindo **tipagem forte**, **segurança de execução** e **confiabilidade estrutural** — em total conformidade com os princípios de **Clean Architecture** e **Domain-Driven Design**.