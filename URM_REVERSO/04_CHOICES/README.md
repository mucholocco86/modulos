# Choices — sistema completo identificado até agora

## Estado da investigação

A análise do sistema de Choices avançou de uma simples identificação de `ChoicesClass` para um modelo arquitetural mais completo: **AST/Choice estrutural**, **estado dinâmico**, **seleção real**, **checkpoint** e **rollback** são canais relacionados, mas não são a mesma coisa.

Documentos detalhados desta etapa:

- `01_FLUXO_CHOICE_ROLLBACK.md` — fluxo da Choice desde a detecção no `renpy.ast.Menu`, passando pela seleção via `ChoiceReturn`, execução pelo Ren'Py, observação de alterações pelo `StoreMonitor` e retorno por rollback.
- `02_LIMITES_E_CASOS_ESPECIAIS.md` — limites, Choices ocultas, texto substituído versus valor real, `jumpTo`, CodeView, fixed rollback, Skip e regras de preservação para o Wells.

## Núcleo

`classes/choices.rpy` contém `ChoicesClass`.

`isDisplayingChoice` consulta o nó atual pelo contexto/script e verifica `renpy.ast.Menu`.

`currentChoices` percorre `script.items` e cria `URMChoice` para itens válidos.

`hiddenCount` conta escolhas não visíveis.

## URMChoice

O item é tratado como tupla com:

```text
item[0] → texto da Choice
item[1] → condição
item[2] → lista de nós AST da alternativa
```

Propriedades importantes:

- `isVisible` avalia a condição em `renpy.store.__dict__`;
- `text` usa `renpy.exports.substitute`;
- `condition` preserva a condição da alternativa;
- `code` usa `CodeView.nodesToCode`;
- `jumpTo` procura o primeiro `renpy.ast.Jump` direto no conteúdo da alternativa.

## Choices ocultas

O URM mantém Choices cuja condição atual é falsa e apresenta sua visibilidade separadamente.

Isso permite inspeção de alternativas que a interface normal do jogo pode não mostrar.

A própria ação de seleção não faz uma segunda checagem de `isVisible`, o que é coerente com a funcionalidade histórica do URM de permitir selecionar Choices ocultas.

Isso deve ser tratado como intervenção avançada, não como mera reprodução visual do Menu normal.

## Código da Choice ≠ mudança de variável

Esta distinção está formalmente registrada.

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

## CodeView e fidelidade

O CodeView é uma reconstrução de apresentação da AST. Para nós Python, `node.code.source` fornece uma ligação forte com a fonte associada ao nó. Para outros nós, o URM reconstrói uma representação legível.

O próprio URM avisa que o código mostrado é gerado por ele e provavelmente não é exatamente igual ao que o desenvolvedor escreveu.

Portanto, para o Wells, é necessário distinguir:

```text
fonte associada ao nó Python
≠
reconstrução CodeView
≠
arquivo .rpy original
```

## Texto exibido versus valor usado na seleção

`URMChoice.text` usa `renpy.exports.substitute()` para apresentação.

`URMChoice.Action`, porém, passa `self._m1_choices__choice[0]` para `ChoiceReturn`, e não `self.text`.

Assim existe uma separação importante:

```text
item original
 ├──→ substitute → texto apresentado
 └──→ ChoiceReturn → seleção real
```

Isso reforça a regra de que a camada visual não deve substituir a estrutura real usada pelo Ren'Py.

## Seleção

A ação de `URMChoice` faz:

```python
renpy.game.log.rollback_is_fixed = False
return renpy.ui.ChoiceReturn(choice_text, index)()
```

O URM não executa manualmente o código da alternativa. A decisão é devolvida ao mecanismo de interação do Ren'Py, que continua a execução real dos nós associados à escolha.

A semântica exata de `rollback_is_fixed` e o caminho interno completo de `ChoiceReturn` até o RollbackLog ainda estão em investigação direta no SDK 7.4.11.

## `jumpTo` não é um grafo completo

O URM procura o primeiro `renpy.ast.Jump` diretamente presente na lista de nós da Choice.

Portanto a coluna `Next label` é uma indicação baseada nessa heurística, e não uma garantia de que esse será o próximo destino em todo fluxo possível.

Estruturas com `If`, `Call`, `Jump` indireto ou lógica interna mais complexa exigem análise adicional.

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

## Path Detection

`PathDetection` é separado de `Choices`.

```text
Choice:
renpy.ast.Menu
    ↓
Choices.currentChoices

Path Detection:
nó atual
    ↓
look-ahead
    ↓
If futuro
    ↓
Paths
```

Não devemos fundir os dois sistemas na futura implementação do Wells.

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

## Fixed rollback e Skip

O changelog do URM registra:

- 2.1: Choices dialog capaz de bypass de fixed choices / fixed rollback;
- 2.2.1: Skip capaz de avançar rapidamente até a próxima Choice;
- 2.3: CodeView inteligente para Choices e paths;
- 2.6.1: prevenção de dados estáticos do URM no save.

A presença de:

```python
renpy.game.log.rollback_is_fixed = False
```

antes de `ChoiceReturn` reforça que o bypass de fixed rollback faz parte do mecanismo de seleção do URM.

A semântica exata ainda precisa ser fechada diretamente no SDK 7.4.11.

## Evidências principais

- `screenshots 0018/0019`: Choices e código AST exibido (`tree_thank = True/False`);
- `screenshot 0017`: Path Detection separado e variáveis observadas;
- `screenshot 0012`: changelog URM 2.6.2;
- código de `classes/choices.rpy`, `classes/codeview.rpy`, `classes/vars.rpy` e `screens/choices.rpy`;
- changelog embutido no próprio URM, incluindo evolução das Choices desde 0.8.

## Perguntas abertas

1. Semântica exata de `ChoiceReturn()` no SDK 7.4.11.
2. Semântica exata de `rollback_is_fixed` e por que o URM o libera antes da seleção.
3. Relação precisa entre `force_checkpoint` e `RollbackLog.complete()`.
4. Momento exato em que o checkpoint passa a integrar o rollback.
5. Sequência interna de restauração de contexto/store durante rollback.
6. Comportamento com estruturas AST de Choice mais complexas.
7. Compatibilidade exata entre versões do Ren'Py.
8. Limites entre fonte Python associada à AST e fonte textual original do script.
9. Como o mecanismo de Skip encontra/interrompe a próxima Choice.
10. Como o URM mantém segurança e consistência ao permitir Choices ocultas/fixed rollback.

**Regra de preservação:** ainda não implementar nem simplificar o sistema. Primeiro completar a árvore inteira; somente depois decidir o que será transplantado para o Wells Framework.
