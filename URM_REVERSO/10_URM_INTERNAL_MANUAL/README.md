# Manual Interno do URM

## Finalidade

Esta pasta é o **manual técnico interno do Universal Ren'Py Mod (URM)** reconstruído a partir da engenharia reversa.

Ela responde principalmente à pergunta:

> **Como as próprias peças do URM se organizam, quais responsabilidades possuem e como conversam entre si?**

Não é uma cópia do código-fonte original e não substitui as evidências. É uma camada de documentação consolidada derivada delas.

## Separação de responsabilidades

O projeto mantém três níveis distintos:

- `07_EVIDENCE/` — o que foi observado no material, código convertido, `.rpyc/.x52` e screenshots.
- `06_RENPY_COMPATIBILITY/` — o que o motor Ren'Py fornece e quais comportamentos do runtime são utilizados pelo URM.
- `10_URM_INTERNAL_MANUAL/` — como o URM usa suas próprias peças para formar o framework.

`08_CROSS_REFERENCE/` funciona como ponte entre esses níveis.

## Regra de leitura

Quando uma página deste manual mencionar uma API ou comportamento do Ren'Py, isso não significa que aquela peça pertença ao URM. A dependência deve ser indicada como dependência externa.

Exemplo:

```text
URMChoice.Action
    |
    +-- [URM] limpa fixed rollback
    |
    +-- [URM] chama ChoiceReturn
    |
    `-- [Ren'Py] ChoiceReturn continua a seleção pelo mecanismo nativo
```

## Núcleo atualmente documentado

### Choices

`ChoicesClass` detecta o `renpy.ast.Menu` atual e produz objetos `URMChoice` a partir de `Menu.items`.

`URMChoice` representa uma alternativa e expõe, entre outras coisas, texto, condição, visibilidade, reconstrução de código, destino de replay e ação de seleção.

### CodeView

`CodeView` transforma nós AST em uma representação legível para a interface do URM. Ele não deve ser confundido com o `.rpy` original.

### StoreMonitor

`StoreMonitor` observa alterações do store e integra callbacks/checkpoints e determinados mecanismos de interceptação. Ele não é o interpretador Python do Ren'Py.

### VarsStore

`VarsStore` mantém informações e controles do próprio URM sobre variáveis: watched, ignored, frozen e dados persistidos pelo URM.

### PathDetection

`PathDetection` constrói caminhos a partir de análise de nós e condições futuras. É relacionado ao fluxo de execução, mas é separado do sistema de `Choices`.

### Notifications

`Notifications` administra as notificações do URM. A notificação `Choices detected` é distinta das notificações de alteração de variável produzidas pelo monitoramento.

### Loader

O loader/bootstrap cria a infraestrutura modular do URM e carrega módulos externos sem fazer parte da lógica específica de Choices.

## Princípio de preservação

Durante a fase de arqueologia, componentes não devem ser removidos apenas porque parecem antigos, redundantes ou pouco utilizados. Primeiro documentamos a função e as dependências; a poda somente acontece depois que a árvore estiver suficientemente fechada.

## Classificação

- 🟢 **CONFIRMADO — URM**: diretamente sustentado pelo código/material do URM.
- 🔵 **CONFIRMADO — Ren'Py 7.4.11**: comportamento confirmado no SDK de referência.
- 🟡 **OBSERVAÇÃO SUA**: comportamento observado em execução pelo usuário.
- 🟠 **HIPÓTESE**: interpretação ainda não fechada.
- 🔴 **DESCARTADO/INCORRETO**: interpretação demonstrada como errada.

## Estado

O manual está sendo construído progressivamente. A investigação continua; portanto páginas podem registrar perguntas abertas em vez de preencher lacunas com suposições.
