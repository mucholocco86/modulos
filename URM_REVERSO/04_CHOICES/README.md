# Choices — sistema completo identificado até agora

## Estado da investigação

A análise do sistema de Choices avançou de uma simples identificação de `ChoicesClass` para um modelo arquitetural mais completo: **AST/Choice estrutural**, **estado dinâmico**, **seleção real**, **checkpoint** e **rollback** são canais relacionados, mas não são a mesma coisa.

Documento detalhado desta etapa:

- `01_FLUXO_CHOICE_ROLLBACK.md` — fluxo da Choice desde a detecção no `renpy.ast.Menu`, passando pela seleção via `ChoiceReturn`, execução pelo Ren'Py, observação de alterações pelo `StoreMonitor` e retorno por rollback.

## Núcleo

`classes/choices.rpy` contém `ChoicesClass`.

`isDisplayingChoice` consulta o nó atual pelo contexto/script e verifica `renpy.ast.Menu`.

`currentChoices` percorre `script.items` e cria `URMChoice` para itens válidos.

`hiddenCount` conta escolhas não visíveis.

## URMChoice

O item é tratado como tupla com:

```text
item[0] → texto
item[1] → condição
item[2] → lista de nós AST da alternativa
```

Propriedades importantes:

- `isVisible` avalia a condição em `renpy.store.__dict__`;
- `text` usa `renpy.exports.substitute`;
- `condition` preserva a condição da alternativa;
- `code` usa `CodeView.nodesToCode`;
- `jumpTo` procura o primeiro `renpy.ast.Jump`.

## Código da Choice ≠ mudança de variável

Esta distinção está agora formalmente registrada.

O código mostrado na tela de Choices vem dos **nós AST pertencentes à alternativa**. Em particular, para `renpy.ast.Python`, `CodeView.nodesToCode()` utiliza `node.code.source`.

Exemplo:

```renpy
"A":
    RPjosy += 5
```

pode ser apresentado como código da alternativa. Isso não significa que `RPjosy` já tenha mudado.

A mudança efetiva de estado pertence ao caminho separado:

```text
execução Ren'Py
    ↓
StoreMonitor
    ↓
oldVal / newVal
```

Essa separação é uma das conclusões centrais da análise.

## Seleção

A ação de `URMChoice` faz:

```python
renpy.game.log.rollback_is_fixed = False
return renpy.ui.ChoiceReturn(choice_text, index)()
```

O URM não executa manualmente o código da alternativa. A decisão é devolvida ao mecanismo de interação do Ren'Py, que continua a execução real dos nós associados à escolha.

A semântica exata de `rollback_is_fixed` e o caminho interno completo de `ChoiceReturn` até o RollbackLog ainda estão em investigação direta no SDK 7.4.11.

## Estado dinâmico

`StoreMonitor` é um componente separado do sistema de Choices. Ele observa/intercepta determinadas alterações do store e usa `get_changes()` no callback Python para obter deltas de estado.

Quando uma variável está sendo monitorada, `handleVarChange()` pode criar a notificação `Variable changed`, com valor anterior e valor novo.

Isso não deve ser confundido com a notificação dedicada `Choices detected`.

## Notificação de Choice

A tela `URM_notifications` possui uma seção específica para Choices baseada em `Choices.isDisplayingChoice` e nas configurações correspondentes.

A mensagem observada nos screenshots `0018`/`0019` é:

```text
Choices detected
```

Ela indica presença de Choice/Menu no fluxo atual; não é uma notificação de mudança de variável.

## Rollback

A investigação atual sustenta o seguinte modelo:

```text
Choice
  ↓
ChoiceReturn
  ↓
Ren'Py executa a alternativa
  ↓
Store pode mudar
  ↓
StoreMonitor observa
  ↓
Ren'Py mantém seu estado de rollback
  ↓
usuário faz rollback
  ↓
Ren'Py restaura estado/contexto
  ↓
Choice pode reaparecer
  ↓
URM observa novamente
```

O URM não deve ser modelado como dono de um segundo estado ou de um segundo mecanismo de rollback.

## Evidências principais

- `screenshots 0018/0019`: Choices e código AST exibido (`tree_thank = True/False`);
- `screenshot 0017`: Path Detection separado e variáveis observadas;
- `screenshot 0012`: changelog do URM 2.6.2, incluindo referências a rollback/Choices e à prevenção de dados estáticos no save;
- código de `classes/choices.rpy`, `classes/codeview.rpy`, `classes/vars.rpy` e `screens/choices.rpy`.

## Perguntas abertas

1. Semântica exata de `ChoiceReturn()` no SDK 7.4.11.
2. Semântica exata de `rollback_is_fixed` e por que o URM o libera antes da seleção.
3. Relação precisa entre `force_checkpoint` e `RollbackLog.complete()`.
4. Momento exato em que o checkpoint passa a integrar o rollback.
5. Sequência interna de restauração de contexto/store durante rollback.
6. Comportamento com estruturas AST de Choice mais complexas.
7. Compatibilidade exata entre versões do Ren'Py.
8. Limites entre fonte Python associada à AST e fonte textual original do script.

**Regra de preservação:** ainda não implementar nem simplificar o sistema. Primeiro completar a árvore inteira; somente depois decidir o que será transplantado para o Wells Framework.
