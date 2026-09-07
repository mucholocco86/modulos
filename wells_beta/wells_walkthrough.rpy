################################################################################
## WELLS FRAMEWORK — WALKTHROUGH
## ANALISADOR DE CONSEQUÊNCIAS — V8
##
## Arquitetura:
## - usa a mesma ideia estrutural do URW: interceptar renpy.exports.menu
## - captura o Menu AST REAL no momento em que Menu.execute() está rodando
## - usa o índice real da escolha para localizar o bloco AST
## - mantém fallback por captions/contexto quando necessário
## - injeta a informação no caption ANTES da screen Choice ser criada
## - NÃO substitui a screen choice do Wells
## - NÃO cria uma segunda tela de choices
## - NÃO altera action/value das escolhas
################################################################################

default persistent.wells_walkthrough_enabled = False

init -1100 python:
    import ast as wells_py_ast
    import re as wells_re

    class WellsWalkthroughConsequence(object):
        def __init__(self, kind, text):
            self.kind = kind
            self.text = text

    class WellsWalkthroughAnalyzer(object):

        def _format_value(self, value):
            if isinstance(value, bool):
                return "True" if value else "False"
            if value is None:
                return "None"
            try:
                return str(value)
            except:
                return "?"

        def _target_name(self, target):
            try:
                if isinstance(target, wells_py_ast.Name):
                    return target.id
                if isinstance(target, wells_py_ast.Attribute):
                    parts = []
                    cur = target
                    while isinstance(cur, wells_py_ast.Attribute):
                        parts.insert(0, cur.attr)
                        cur = cur.value
                    if isinstance(cur, wells_py_ast.Name):
                        parts.insert(0, cur.id)
                    return ".".join(parts)
            except:
                pass
            return None

        def _value_text(self, node):
            try:
                if hasattr(wells_py_ast, "Constant") and isinstance(node, wells_py_ast.Constant):
                    return self._format_value(node.value)
                if isinstance(node, wells_py_ast.Name):
                    return node.id
                if isinstance(node, wells_py_ast.Attribute):
                    return self._target_name(node)
                if isinstance(node, wells_py_ast.UnaryOp):
                    if isinstance(node.op, wells_py_ast.USub):
                        return "-" + self._value_text(node.operand)
                    if isinstance(node.op, wells_py_ast.UAdd):
                        return "+" + self._value_text(node.operand)
                if isinstance(node, wells_py_ast.BinOp):
                    left = self._value_text(node.left)
                    right = self._value_text(node.right)
                    if isinstance(node.op, wells_py_ast.Add):
                        return left + " + " + right
                    if isinstance(node.op, wells_py_ast.Sub):
                        return left + " - " + right
                if isinstance(node, wells_py_ast.Call):
                    return self._call_text(node)
            except:
                pass
            return "valor"

        def _call_text(self, node):
            try:
                if isinstance(node.func, wells_py_ast.Name):
                    return str(node.func.id)
                return str(self._target_name(node.func))
            except:
                return "function"

        def _append(self, result, kind, text):
            result.append(WellsWalkthroughConsequence(kind, text))

        def _python_source(self, code_obj):
            try:
                if isinstance(code_obj, str):
                    return code_obj
            except:
                pass
            for attr in ("source", "py"):
                try:
                    source = getattr(code_obj, attr)
                    if isinstance(source, str):
                        return source
                    if source is not None:
                        return str(source)
                except:
                    pass
            return None

        def _analyze_python(self, source, result):
            if not source:
                return
            try:
                tree = wells_py_ast.parse(source)
            except:
                return

            try:
                nodes = wells_py_ast.walk(tree)
            except:
                return

            for node in nodes:
                try:
                    if isinstance(node, wells_py_ast.AugAssign):
                        name = self._target_name(node.target)
                        if not name:
                            continue
                        value = self._value_text(node.value)
                        if isinstance(node.op, wells_py_ast.Add):
                            self._append(result, "increase", name + " += " + value)
                        elif isinstance(node.op, wells_py_ast.Sub):
                            self._append(result, "decrease", name + " -= " + value)
                    elif isinstance(node, wells_py_ast.Assign):
                        value = self._value_text(node.value)
                        for target in node.targets:
                            name = self._target_name(target)
                            if name:
                                self._append(result, "assign", name + " = " + value)
                    elif hasattr(wells_py_ast, "AnnAssign") and isinstance(node, wells_py_ast.AnnAssign):
                        name = self._target_name(node.target)
                        if name and node.value:
                            self._append(result, "assign", name + " = " + self._value_text(node.value))
                    elif isinstance(node, wells_py_ast.Call):
                        self._append(result, "call", self._call_text(node))
                except:
                    pass

        def _analyze_node(self, node, result):
            if node is None:
                return
            try:
                if isinstance(node, renpy.ast.PyCode):
                    self._analyze_python(self._python_source(node), result)
                    return
            except:
                pass
            try:
                if isinstance(node, renpy.ast.Python):
                    self._analyze_python(self._python_source(node.code), result)
                    return
            except:
                pass
            try:
                if isinstance(node, renpy.ast.Jump):
                    self._append(result, "jump", str(node.target))
                    return
            except:
                pass
            try:
                if isinstance(node, renpy.ast.Call):
                    self._append(result, "call", str(node.label))
                    return
            except:
                pass
            try:
                if isinstance(node, renpy.ast.If):
                    self._append(result, "condition", "condition")
                    return
            except:
                pass

        def analyze(self, block):
            result = []
            try:
                nodes = block if isinstance(block, (list, tuple)) else [block]
                for node in nodes:
                    try:
                        collected = []
                        node.get_children(collected.append)
                        for child in collected:
                            self._analyze_node(child, result)
                    except:
                        self._analyze_node(node, result)
            except:
                pass

            clean = []
            seen = set()
            for item in result:
                key = (item.kind, item.text)
                if key not in seen:
                    seen.add(key)
                    clean.append(item)
            return clean

    wells_walkthrough_analyzer = WellsWalkthroughAnalyzer()

    ########################################################################
    ## RUNTIME MENU CAPTURE
    ########################################################################

    wells_walkthrough_original_menu = getattr(renpy.exports, "menu", None)
    wells_walkthrough_original_menu_execute = getattr(renpy.ast.Menu, "execute", None)
    wells_walkthrough_active_menu = None
    wells_walkthrough_runtime_menu = None
    wells_walkthrough_runtime_injected = False

    def wells_walkthrough_menu_execute(self):
        global wells_walkthrough_active_menu
        previous = wells_walkthrough_active_menu
        wells_walkthrough_active_menu = self
        try:
            return wells_walkthrough_original_menu_execute(self)
        finally:
            wells_walkthrough_active_menu = previous

    try:
        if wells_walkthrough_original_menu_execute is not None:
            renpy.ast.Menu.execute = wells_walkthrough_menu_execute
    except:
        pass

    ########################################################################
    ## FALLBACK MENU FINDER
    ########################################################################

    def wells_walkthrough_clean_caption(value):
        try:
            text = str(value)
        except:
            text = ""
        try:
            text = wells_re.sub(r"\{[^}]*\}", "", text)
        except:
            pass
        return text.strip()

    def wells_walkthrough_item_caption(item):
        try:
            if hasattr(item, "caption"):
                return wells_walkthrough_clean_caption(item.caption)
            if isinstance(item, (list, tuple)) and len(item) > 0:
                return wells_walkthrough_clean_caption(item[0])
        except:
            pass
        return ""

    def wells_walkthrough_execution_context():
        context = {"filename": None, "linenumber": 0}
        try:
            ctx = renpy.game.context()
            script = renpy.game.script
            current = getattr(ctx, "current", None)
            if current:
                try:
                    node = script.lookup(current)
                    if node is not None:
                        context["filename"] = getattr(node, "filename", None)
                        context["linenumber"] = getattr(node, "linenumber", 0) or 0
                except:
                    pass
        except:
            pass
        return context

    def wells_walkthrough_find_menu_node(items):
        if wells_walkthrough_active_menu is not None:
            return wells_walkthrough_active_menu

        best = None
        best_score = -1
        context = wells_walkthrough_execution_context()

        try:
            for node_name, node in renpy.game.script.namemap.items():
                if not isinstance(node, renpy.ast.Menu):
                    continue

                ast_items = getattr(node, "items", None)
                if not ast_items:
                    continue

                runtime_captions = [wells_walkthrough_item_caption(x) for x in items]
                ast_captions = [wells_walkthrough_clean_caption(x[0]) for x in ast_items]

                matches = 0
                for caption in runtime_captions:
                    if caption in ast_captions:
                        matches += 1

                if not runtime_captions:
                    continue

                ratio = float(matches) / float(len(runtime_captions))
                if ratio < 0.8:
                    continue

                score = int(ratio * 1000)
                menu_file = str(getattr(node, "filename", "") or "").replace(".rpyc", ".rpy")
                context_file = str(context.get("filename") or "")
                if menu_file and context_file and menu_file == context_file:
                    score += 500

                if score > best_score:
                    best_score = score
                    best = node
        except:
            pass

        return best

    def wells_walkthrough_block_for_item(menu_node, runtime_item):
        if menu_node is None:
            return None

        try:
            # Ren'Py 7.4.11 Menu.execute() sends:
            # (label, condition, real_menu_item_index)
            if isinstance(runtime_item, (list, tuple)) and len(runtime_item) >= 3:
                index = runtime_item[2]
                if isinstance(index, int) and 0 <= index < len(menu_node.items):
                    return menu_node.items[index][2]
        except:
            pass

        # Fallback for engines/mods that don't expose the index.
        caption = wells_walkthrough_item_caption(runtime_item)
        try:
            for menu_item in menu_node.items:
                if wells_walkthrough_clean_caption(menu_item[0]) == caption:
                    return menu_item[2]
        except:
            pass

        return None

    def wells_walkthrough_format_consequences(consequences):
        lines = []
        for consequence in consequences:
            if consequence.kind == "increase":
                lines.append("{color=#39ff14}" + consequence.text + "{/color}")
            elif consequence.kind == "decrease":
                lines.append("{color=#ff4040}" + consequence.text + "{/color}")
            elif consequence.kind == "assign":
                lines.append("{color=#00f3ff}" + consequence.text + "{/color}")
            elif consequence.kind == "jump":
                lines.append("{color=#ff9d00}⇒ " + consequence.text + "{/color}")
            elif consequence.kind == "call":
                lines.append("{color=#39ff14}⇒ " + consequence.text + "{/color}")
            elif consequence.kind == "condition":
                lines.append("{color=#ffe600}? condition{/color}")
        return "\n".join(lines)

    def wells_walkthrough_menu_wrapper(items, set_expr, args=None, kwargs=None, item_arguments=None):
        global wells_walkthrough_runtime_menu
        global wells_walkthrough_runtime_injected

        wells_walkthrough_runtime_menu = None
        wells_walkthrough_runtime_injected = False

        try:
            runtime_items = list(items) if items is not None else []
        except:
            runtime_items = items

        if persistent.wells_walkthrough_enabled:
            try:
                menu_node = wells_walkthrough_find_menu_node(runtime_items)
                wells_walkthrough_runtime_menu = menu_node

                if menu_node is not None:
                    enhanced_items = []
                    injected_any = False

                    for runtime_item in runtime_items:
                        try:
                            if not isinstance(runtime_item, (list, tuple)) or len(runtime_item) < 3:
                                enhanced_items.append(runtime_item)
                                continue

                            caption = runtime_item[0]
                            condition = runtime_item[1]
                            value = runtime_item[2]
                            block = wells_walkthrough_block_for_item(menu_node, runtime_item)
                            consequences = wells_walkthrough_analyzer.analyze(block)
                            info = wells_walkthrough_format_consequences(consequences)

                            if info and value is not None:
                                caption = str(caption) + "\n" + info
                                injected_any = True

                            enhanced_items.append((caption, condition, value))
                        except:
                            enhanced_items.append(runtime_item)

                    runtime_items = enhanced_items
                    wells_walkthrough_runtime_injected = injected_any
            except:
                wells_walkthrough_runtime_menu = None
                wells_walkthrough_runtime_injected = False

        return wells_walkthrough_original_menu(runtime_items, set_expr, args, kwargs, item_arguments)

    if wells_walkthrough_original_menu is not None and not getattr(wells_walkthrough_original_menu, "_wells_walkthrough_wrapped", False):
        wells_walkthrough_menu_wrapper._wells_walkthrough_wrapped = True
        renpy.exports.menu = wells_walkthrough_menu_wrapper

    def wells_walkthrough_get_info(items, item):
        # A tela Wells não precisa mais chamar o analisador.
        # O caption já chega pronto pela camada de runtime.
        return ""

    def wells_walkthrough_text_size(base_size):
        size = int(base_size)
        if size < 12:
            size = 12
        return size
