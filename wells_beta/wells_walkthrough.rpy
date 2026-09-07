################################################################################
## WELLS FRAMEWORK — WALKTHROUGH
## ANALISADOR DE CONSEQUÊNCIAS — V6
##
## Base estrutural:
## - usa o mesmo ponto de interceptação do URW: renpy.exports.menu
## - recebe os itens reais enviados pelo Menu.execute()
## - localiza o Menu AST correspondente no script
## - usa o índice original do Ren'Py para chegar ao bloco da escolha
## - NÃO substitui a tela Choice do Wells
## - NÃO altera a lista de escolhas do jogo
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
                    for entry in node.entries:
                        if len(entry) > 1:
                            self._analyze_node(entry[1], result)
                    return
            except:
                pass
            try:
                children = node.get_children()
                if children:
                    for child in children:
                        self._analyze_node(child, result)
                    return
            except:
                pass
            try:
                for child in node.children:
                    self._analyze_node(child, result)
            except:
                pass

        def analyze(self, block):
            result = []
            try:
                nodes = block if isinstance(block, (list, tuple)) else [block]
                for node in nodes:
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
    ## RUNTIME MENU FINDER
    ##
    ## Este é o ponto principal da V6. O wrapper recebe exatamente a lista
    ## entregue por renpy.ast.Menu.execute() a renpy.exports.menu().
    ########################################################################

    wells_walkthrough_original_menu = getattr(renpy.exports, "menu", None)
    wells_walkthrough_runtime_menu = None
    wells_walkthrough_runtime_items = None
    wells_walkthrough_runtime_match = None

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

    def wells_walkthrough_items_match(ast_items, runtime_items):
        try:
            runtime = [wells_walkthrough_item_caption(x) for x in runtime_items]
            ast_captions = []
            for entry in ast_items:
                try:
                    ast_captions.append(wells_walkthrough_clean_caption(entry[0]))
                except:
                    ast_captions.append("")

            if not runtime:
                return False

            matches = 0
            for caption in runtime:
                if caption in ast_captions:
                    matches += 1

            return matches >= len(runtime) * 0.8
        except:
            return False

    def wells_walkthrough_execution_context():
        context = {
            "filename": None,
            "linenumber": 0,
            "label": None,
            "menu_node": None,
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
                        if isinstance(node, renpy.ast.Menu):
                            context["menu_node"] = node
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

    def wells_walkthrough_find_menu_node(items):
        global wells_walkthrough_runtime_menu
        global wells_walkthrough_runtime_match

        try:
            context = wells_walkthrough_execution_context()
            if context.get("menu_node") is not None:
                return context["menu_node"], {"strategy": "context_node", "offset": 0}

            script = renpy.game.script

            # 1. Exact/strong caption matching. This is the primary method.
            candidates = []
            for node_name, node in script.namemap.items():
                try:
                    if not isinstance(node, renpy.ast.Menu):
                        continue
                    if not getattr(node, "items", None):
                        continue
                    if wells_walkthrough_items_match(node.items, items):
                        candidates.append(node)
                except:
                    pass

            if len(candidates) == 1:
                return candidates[0], {"strategy": "caption_single", "offset": 0}

            # 2. File/line proximity, when the runtime context gives us location.
            if candidates and context.get("filename"):
                filename = context.get("filename")
                line = context.get("linenumber", 0)
                same_file = []
                for node in candidates:
                    node_file = str(getattr(node, "filename", "") or "").replace(".rpyc", ".rpy")
                    if node_file == filename or node_file.endswith(filename.split("/")[-1]):
                        same_file.append(node)
                if same_file:
                    same_file.sort(key=lambda n: abs((getattr(n, "linenumber", 0) or 0) - line))
                    return same_file[0], {"strategy": "caption_proximity", "offset": 0}

            # 3. Deterministic fallback: first matching candidate.
            if candidates:
                candidates.sort(key=lambda n: (str(getattr(n, "filename", "") or ""), getattr(n, "linenumber", 0) or 0))
                return candidates[0], {"strategy": "caption_fallback", "offset": 0}
        except:
            pass

        return None, None

    def wells_walkthrough_menu_wrapper(items, set_expr, args=None, kwargs=None, item_arguments=None):
        global wells_walkthrough_runtime_menu
        global wells_walkthrough_runtime_items
        global wells_walkthrough_runtime_match

        try:
            wells_walkthrough_runtime_items = list(items) if items is not None else []
        except:
            wells_walkthrough_runtime_items = items

        wells_walkthrough_runtime_menu = None
        wells_walkthrough_runtime_match = None

        if persistent.wells_walkthrough_enabled:
            try:
                menu_node, match_info = wells_walkthrough_find_menu_node(wells_walkthrough_runtime_items)
                wells_walkthrough_runtime_menu = menu_node
                wells_walkthrough_runtime_match = match_info
            except:
                wells_walkthrough_runtime_menu = None
                wells_walkthrough_runtime_match = None

        return wells_walkthrough_original_menu(items, set_expr, args, kwargs, item_arguments)

    if wells_walkthrough_original_menu is not None and not getattr(wells_walkthrough_original_menu, "_wells_walkthrough_wrapped", False):
        wells_walkthrough_menu_wrapper._wells_walkthrough_wrapped = True
        renpy.exports.menu = wells_walkthrough_menu_wrapper

    def wells_walkthrough_get_info(items, item):
        if not persistent.wells_walkthrough_enabled:
            return ""

        try:
            menu = wells_walkthrough_runtime_menu
            if menu is None:
                return ""

            action = getattr(item, "action", None)
            menu_index = getattr(action, "value", None)
            block = None

            # The runtime ChoiceReturn.value is the original Menu.items index.
            if isinstance(menu_index, int):
                if 0 <= menu_index < len(menu.items):
                    block = menu.items[menu_index][2]

            # Safe caption fallback for unusual/custom menu screens.
            if block is None:
                caption = wells_walkthrough_item_caption(item)
                for menu_item in menu.items:
                    try:
                        if wells_walkthrough_clean_caption(menu_item[0]) == caption:
                            block = menu_item[2]
                            break
                    except:
                        pass

            if block is None:
                return ""

            consequences = wells_walkthrough_analyzer.analyze(block)
            if not consequences:
                return ""

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
        except:
            return ""

    def wells_walkthrough_text_size(base_size):
        size = int(base_size)
        if size < 12:
            size = 12
        return size
