# Arquitetura atual — mapa consolidado

Ren'Py é o executor/interpreter do fluxo. O URM observa, apresenta, registra e manipula partes do runtime.

```text
Ren'Py AST / Context / Store / Interaction / Rollback
                     |
        +------------+-------------+
        |            |             |
     Choices    StoreMonitor     TextBox
        |            |             |
        |         VarsStore     TextRepl
        |            |             |
        +------------+-------------+
                     |
                  URM UI
```

## Fluxo típico

```text
Say -> TextBox/URM_say (se habilitado) -> avanço
    -> Python (se houver) -> StoreMonitor callback
    -> If (se houver) -> Menu -> Choices.currentChoices
    -> URMChoice -> seleção -> ChoiceReturn -> continuação
```

Este é um fluxo típico, não uma regra universal: Menu pode aparecer sem Say imediatamente antes.

## Papéis

- Choices: observa o `renpy.ast.Menu` atual e fornece representação/ações/UI.
- CodeView: reconstrói AST em código exibível; não é o interpretador.
- PathDetection: analisa caminhos e condições; distinto da seleção normal de Menu.
- VarsStore: memória/configuração de variáveis observadas, congeladas, monitoradas e ignoradas.
- StoreMonitor: observa/intercepta mudanças e integra callbacks/checkpoints.
- TextBox: apresentação/interceptação do pipeline de Say.
- TextRepl: substituição/filtro de texto.

O bloqueio real de interação vem do nó Ren'Py que exige interação (`node.interact`), não do TextBox.
