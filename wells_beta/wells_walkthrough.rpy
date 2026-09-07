################################################################################
## WELLS FRAMEWORK — WALKTHROUGH
## ANALISADOR DE CONSEQUÊNCIAS — V7
##
## Arquitetura:
## - usa a mesma ideia estrutural do URW: interceptar renpy.exports.menu
## - localiza o Menu AST real usando captions + contexto/proximidade
## - analisa o bloco AST da escolha
## - injeta a informação no caption ANTES da tela Choice ser criada
## - NÃO substitui a screen choice do Wells
## - NÃO cria uma segunda tela de choices
## - NÃO altera action/value das escolhas
################################################################################

default persistent.wells_walkthrough_enabled = False

init -1000 python:
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
                return "valor"
            except:
                return "valor"

        def _call_text(self, node):
            try:
                if isinstance(node.func, wells_py_ast.Name):
                    name = node.func.id
                else:
                    name = self._target_name(node.func)
                return str(name)
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
            try:
                source = code_obj.source
                if isinstance(source, str):
                    return source
                return str(source)
            except:
                pass
            try:
                source = code_obj.py
                if isinstance(source, str):
                    return source
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

            for node in wells_py_ast.walk(tree):
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

        def _analyze_direct_node(self, node, result):
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
                            self._analyze_direct_node(child, result)
                    except:
                        self._analyze_direct_node(node, result)
                        try:
                            children = getattr(node, "children", None)
                            if children:
                                for child in children:
                                    self._analyze_direct_node(child, result)
                        except:
                            pass
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
    ## URW-STYLE MENU FINDER
    ########################################################################

    wells_walkthrough_original_menu = getattr(renpy.exports, "menu", None)
    wells_walkthrough_runtime_menu = None
    wells_walkthrough_runtime_items = None
    wells_walkthrough_runtime_match = None
    wells_walkthrough_runtime_injected = False

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
            return wells_walkthrough_clean_caption(item)
        except:
            return ""

    def wells_walkthrough_execution_context():
        context = {
            "filename": None,
            "linenumber": 0,
            "label": None,
        }
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

            if not context["filename"]:
                for attr in ("call_location_stack", "return_stack"):
                    try:
                        stack = getattr(ctx, attr, None)
                        if isinstance(stack, (list, tuple)):
                            for node_name in reversed(list(stack)):
                                try:
                                    node = script.lookup(node_name)
                                    if node is not None and getattr(node, "filename", None):
                                        context["filename"] = node.filename
                                        context["linenumber"] = getattr(node, "linenumber", 0) or 0
                                        break
                                except:
                                    pass
                        if context["filename"]:
                            break
                    except:
                        pass

            if context["filename"]:
                context["filename"] = str(context["filename"]).replace(".rpyc", ".rpy")

            if context["filename"]:
                best_label = None
                best_line = -1
                try:
                    for node_name, node in script.namemap.items():
                        if isinstance(node, renpy.ast.Label):
                            filename = getattr(node, "filename", None)
                            line = getattr(node, "linenumber", 0) or 0
                            if filename == context["filename"] and line <= context["linenumber"] and line > best_line:
                                best_label = node.name
                                best_line = line
                    context["label"] = best_label
                except:
                    pass
        except:
            pass
        return context

    def wells_walkthrough_score_menu(menu_node, runtime_items, context):
        score = 0
        try:
            ast_items = getattr(menu_node, "items", None)
            if not ast_items:
                return -1

            runtime_captions = [wells_walkthrough_item_caption(x) for x in runtime_items]
            ast_captions = []
            for entry in ast_items:
                try:
                    ast_captions.append(wells_walkthrough_clean_caption(entry[0]))
                except:
                    ast_captions.append("")

            if not runtime_captions:
                return -1

            matches = 0
            for caption in runtime_captions:
                if caption in ast_captions:
                    matches += 1

            ratio = float(matches) / float(len(runtime_captions))
            if ratio < 0.8:
                return -1

            score += int(ratio * 1000)

            menu_file = str(getattr(menu_node, "filename", "") or "").replace(".rpyc", ".rpy")
            context_file = str(context.get("filename") or "")
            if menu_file and context_file:
                if menu_file == context_file:
                    score += 500
                elif menu_file.endswith(context_file.split("/")[-1]):
                    score += 250

            menu_line = getattr(menu_node, "linenumber", 0) or 0
            context_line = context.get("linenumber", 0) or 0
            if menu_line and context_line:
                distance = abs(menu_line - context_line)
                if distance < 25:
                    score += 200
                elif distance < 100:
                    score += 100
                elif distance < 500:
                    score += 25
        except:
            return -1
        return score

    def wells_walkthrough_find_menu_node(items):
        global wells_walkthrough_runtime_match

        best = None
        best_score = -1
        context = wells_walkthrough_execution_context()

        try:
            script = renpy.game.script
            for node_name, node in script.namemap.items():
                try:
                    if not isinstance(node, renpy.ast.Menu):
                        continue
                    score = wells_walkthrough_score_menu(node, items, context)
                    if score > best_score:
                        best_score = score
                        best = node
                except:
                    pass
        except:
            pass

        if best is not None and best_score >= 800:
            wells_walkthrough_runtime_match = {
                "score": best_score,
                "strategy": "urw_style_caption_context",
            }
            return best

        wells_walkthrough_runtime_match = None
        return None

    def wells_walkthrough_block_for_item(menu_node, runtime_item):
        try:
            if menu_node is None:
                return None

            value = None
            if isinstance(runtime_item, (list, tuple)) and len(runtime_item) >= 3:
                value = runtime_item[2]

            if isinstance(value, int):
                if 0 <= value < len(menu_node.items):
                    return menu_node.items[value][2]

            caption = wells_walkthrough_item_caption(runtime_item)
            for menu_item in menu_node.items:
                try:
                    if wells_walkthrough_clean_caption(menu_item[0]) == caption:
                        return menu_item[2]
                except:
                    pass
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
        global wells_walkthrough_runtime_items
        global wells_walkthrough_runtime_match
        global wells_walkthrough_runtime_injected

        wells_walkthrough_runtime_menu = None
        wells_walkthrough_runtime_items = None
        wells_walkthrough_runtime_match = None
        wells_walkthrough_runtime_injected = False

        try:
            runtime_items = list(items) if items is not None else []
        except:
            runtime_items = items

        wells_walkthrough_runtime_items = runtime_items

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
                    wells_walkthrough_runtime_items = runtime_items
                    wells_walkthrough_runtime_injected = injected_any
            except:
                wells_walkthrough_runtime_menu = None
                wells_walkthrough_runtime_injected = False

        return wells_walkthrough_original_menu(runtime_items, set_expr, args, kwargs, item_arguments)

    if wells_walkthrough_original_menu is not None and not getattr(wells_walkthrough_original_menu, "_wells_walkthrough_wrapped", False):
        wells_walkthrough_menu_wrapper._wells_walkthrough_wrapped = True
        renpy.exports.menu = wells_walkthrough_menu_wrapper

    def wells_walkthrough_get_info(items, item):
        if not persistent.wells_walkthrough_enabled:
            return ""

        # V7 já injeta o resultado no caption antes de a screen choice
        # receber os itens. Isso evita duplicação na screen Wells.
        if wells_walkthrough_runtime_injected:
            return ""

        return ""

    def wells_walkthrough_text_size(base_size):
        size = int(base_size)
        if size < 12:
            size = 12
        return size
