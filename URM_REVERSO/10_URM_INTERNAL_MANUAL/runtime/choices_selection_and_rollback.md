# Choices — seleção, fixed rollback e fronteira com o Ren'Py

## Objetivo

Registrar o comportamento do URM na seleção de uma Choice sem confundir responsabilidades do mod com responsabilidades do motor.

## Fluxo interno do URM

```text
ChoicesClass
    ↓
URMChoice
    ↓
Action
    ↓
rollback_is_fixed = False
    ↓
renpy.ui.ChoiceReturn(original_text, index)()
```

Até aqui, a sequência é código do URM.

## O que acontece depois

A partir de `ChoiceReturn`, a continuação pertence ao Ren'Py:

```text
URMChoice.Action
    ↓
Ren'Py ChoiceReturn
    ↓
interação/menu
    ↓
valor da Choice
    ↓
Menu.execute()
    ↓
primeiro nó do bloco selecionado
```

O URM não precisa reproduzir a execução do bloco para fazer a seleção.

## Relação com rollback

No Ren'Py 7.4.11, a interação informa ao `RollbackLog` que ocorreu uma interação; checkpoints são usados para registrar pontos de rollback/roll-forward. `ChoiceReturn` também possui consultas relacionadas a fixed rollback e roll-forward.

No URM, a linha:

```python
renpy.game.log.rollback_is_fixed = False
```

é executada imediatamente antes de `ChoiceReturn`.

### Classificação atual

- 🟢 **CONFIRMADO — URM:** o URM força `rollback_is_fixed` para `False` antes da seleção programática.
- 🔵 **CONFIRMADO — Ren'Py 7.4.11:** `ChoiceReturn.get_sensitive()` e `get_selected()` consultam `in_fixed_rollback()`/`roll_forward_info()`.
- 🟠 **HIPÓTESE FORTE:** a linha do URM permite que sua seleção programática passe pela mesma infraestrutura de Choice sem ficar limitada pelo estado de fixed rollback.
- 🔴 **NÃO CONFIRMADO:** a intenção original do autor além desse efeito mecânico.

## `did_interaction` não é o checkpoint

O SDK 7.4.11 mostra uma distinção importante:

```text
interação termina
    ↓
did_interaction = True
    ↓
próxima execução de nó
    ↓
RollbackLog.begin()
    ↓
novo período de rollback
```

O `did_interaction` é um sinal de que uma interação ocorreu. O checkpoint é uma operação separada.

Isso evita a interpretação incorreta:

```text
Choice → did_interaction → checkpoint
```

como se `did_interaction` fosse o próprio checkpoint.

## Fixed rollback

`fix_rollback()` e `rollback_is_fixed` também não são a mesma operação.

No SDK 7.4.11, `fix_rollback()` estabelece uma fronteira; durante a operação de rollback, quando o contexto restaurado alcança a fronteira apropriada, o estado `rollback_is_fixed` pode ser ativado.

Consequentemente:

```text
fix_rollback()
    ≠
rollback_is_fixed = True
```

A primeira cria/define a condição de fronteira; a segunda representa o estado efetivo consultado pelo runtime.

## Por que isso importa para o URM

A linha do URM não deve ser traduzida para:

> "URM controla o rollback do Ren'Py."

A formulação mais precisa é:

> **O URM intervém em um estado de fixed rollback do Ren'Py imediatamente antes de devolver uma seleção ao mecanismo nativo de Choice.**

Isso preserva a fronteira arquitetural:

```text
Ren'Py = dono do rollback
URM    = consumidor/interventor pontual
```

## Regra para Wells

Na primeira reconstrução fiel:

1. preservar a chamada a `ChoiceReturn`;
2. preservar a alteração de `rollback_is_fixed` enquanto sua função mecânica não estiver totalmente fechada;
3. não criar um segundo sistema de rollback;
4. não substituir `did_interaction` por um suposto checkpoint;
5. não remover configurações do Ren'Py apenas por parecerem antigas ou indiretas.

A poda ou alteração dessas peças fica para uma etapa experimental posterior, depois que a árvore completa estiver documentada.
