# Arquitetura atual — mapa consolidado

Ren'Py é o executor/interpreter do fluxo. O URM observa, apresenta, registra e manipula partes do runtime.

A análise das Choices refinou esse modelo: **estrutura da Choice, estado dinâmico e rollback são fluxos relacionados, porém distintos**.

```text
                         REN'PY
                           │
        ┌──────────────────┼──────────────────┐
        │                  │                  │
       AST                STORE            ROLLBACK
        │                  │                  │
        ▼                  ▼                  ▼
     Choices          StoreMonitor         Ren'Py
        │                  │
     CodeView           VarsStore
        │                  │
        └──────────┬───────┘
                   ▼
                 URM UI
```

## Fluxo típico

```text
Say -> TextBox/URM_say (se habilitado) -> avanço
    -> Python (se houver) -> StoreMonitor callback
    -> If (se houver) -> Menu -> Choices.currentChoices
    -> URMChoice -> ChoiceReturn -> continuação pelo Ren'Py
```

Este é um fluxo típico, não uma regra universal: Menu pode aparecer sem Say imediatamente antes.

## Choices: modelo refinado

Quando o contexto atual aponta para um `renpy.ast.Menu`, o URM pode construir `URMChoice` diretamente a partir dos itens do Menu.

```text
Ren'Py Script/AST
      ↓
renpy.ast.Menu
      ↓
ChoicesClass.currentChoices
      ↓
URMChoice
      ├── text
      ├── condition
      ├── visibility
      ├── AST nodes
      └── jumpTo
```

O código apresentado para uma alternativa é produzido pelo `CodeView.nodesToCode()` a partir dos nós AST. Para nós `renpy.ast.Python`, o URM usa `node.code.source`.

Isso é **informação estrutural da Choice**, não uma notificação de mudança de estado.

## Seleção real

O `URMChoice.Action` não executa manualmente o Python da alternativa. Ele libera `rollback_is_fixed` e chama `renpy.ui.ChoiceReturn(...)`, devolvendo a seleção ao mecanismo de interação do Ren'Py.

```text
Usuário seleciona
      ↓
URMChoice.Action
      ↓
ChoiceReturn
      ↓
Ren'Py
      ↓
execução real da alternativa
```

## Estado dinâmico

O caminho de alteração de variável é separado:

```text
execução Ren'Py
      ↓
SetField / Python callback
      ↓
StoreMonitor
      ↓
oldVal / newVal
      ↓
VarsStore / Notifications
```

Uma notificação `Variable changed` só deve ser interpretada como observação de estado quando o caminho de monitoramento correspondente estiver ativo.

## Choice notification ≠ Variable changed

A tela `URM_notifications` contém uma seção dedicada à presença de Choices, baseada em `Choices.isDisplayingChoice`. A mensagem observada é `Choices detected`.

Essa notificação é distinta das notificações temporárias produzidas por `Notifications.add()` para mudanças monitoradas de variáveis.

## Rollback

O URM não é tratado como proprietário de um segundo mecanismo de rollback. O Ren'Py continua responsável pelo histórico, checkpoints e restauração de estado/contexto.

Modelo conceitual:

```text
Menu
 ↓
ChoiceReturn
 ↓
Ren'Py executa
 ↓
Store muda
 ↓
StoreMonitor observa
 ↓
Ren'Py registra estado/rollback
 ↓
Rollback
 ↓
Ren'Py restaura
 ↓
Menu pode reaparecer
 ↓
Choices observa novamente
```

A relação exata entre `rollback_is_fixed`, `ChoiceReturn`, `force_checkpoint` e `RollbackLog.complete()` continua sendo objeto de investigação no SDK 7.4.11.

## Papéis

- **Choices:** observa o `renpy.ast.Menu` atual e fornece representação/ações/UI.
- **CodeView:** reconstrói determinados nós AST em código exibível; não é o interpretador.
- **PathDetection:** analisa caminhos e condições; distinto da seleção normal de Menu.
- **VarsStore:** memória/configuração de variáveis observadas, congeladas, monitoradas e ignoradas.
- **StoreMonitor:** observa/intercepta mudanças e integra callbacks/checkpoints.
- **TextBox:** apresentação/interceptação do pipeline de Say.
- **TextRepl:** substituição/filtro de texto.

O bloqueio real de interação vem do nó Ren'Py que exige interação (`node.interact`), não do TextBox.

## Regra arquitetural para o Wells

A fonte de verdade deve continuar sendo o runtime do Ren'Py:

```text
Ren'Py = dono da execução + estado + rollback
Wells = observador + apresentador + interface de análise
```

O Wells não deve manter uma cópia independente do estado do jogo nem transformar-se em um segundo interpretador de Ren'Py.
