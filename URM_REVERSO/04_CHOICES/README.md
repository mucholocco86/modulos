# Choices — sistema completo identificado até agora

## Núcleo

`classes/choices.rpy` contém `ChoicesClass`. `isDisplayingChoice` consulta o nó atual pelo contexto/script e verifica `renpy.ast.Menu`. `currentChoices` percorre `script.items` e cria `URMChoice` para itens válidos. `hiddenCount` conta escolhas não visíveis.

## URMChoice

O item é tratado como tupla com texto, condição e lista de nós AST executados pela escolha. `isVisible` avalia a condição em `renpy.store.__dict__`; `text` usa `renpy.exports.substitute`; `code` usa `CodeView.nodesToCode`; `jumpTo` procura o primeiro `renpy.ast.Jump`.

## Seleção

A ação faz:

```python
renpy.game.log.rollback_is_fixed = False
return renpy.ui.ChoiceReturn(choice_text, index)()
```

A semântica exata de `rollback_is_fixed` e `ChoiceReturn` ainda precisa ser validada diretamente no SDK 7.4.11.

## UI

`screens/choices.rpy` mostra número, texto, visibilidade, código, próximo label e seleção, além de CodeView, condição, replay/jump e atalhos.

## Perguntas abertas

1. Semântica exata de `ChoiceReturn()`.
2. Relação entre seleção e rollback log.
3. Momento exato do checkpoint.
4. Avaliação do Menu pelo Ren'Py versus avaliação adicional do URM.
5. Compatibilidade entre versões.
