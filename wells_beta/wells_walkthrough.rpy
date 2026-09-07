################################################################################
## WELLS FRAMEWORK — WALKTHROUGH
## ANALISADOR DE CONSEQUÊNCIAS — V4
################################################################################

default persistent.wells_walkthrough_enabled = False

init -1000 python:
    import ast as wells_py_ast

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
                if isinstance(node, wells_py_ast.Constant):
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
                elif isinstance(node, wells_py_ast.AnnAssign):
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

    # Ren'Py advances the context to the node after the Menu before calling
    # renpy.exports.menu(). Capture the real Menu at that exact runtime point.
    wells_walkthrough_runtime_menu = None
    wells_walkthrough_runtime_choices = None
    wells_walkthrough_original_menu = getattr(renpy.exports, "menu", None)

    if wells_walkthrough_original_menu is not None and not getattr(wells_walkthrough_original_menu, "_wells_walkthrough_wrapped", False):
        def wells_walkthrough_menu_wrapper(items, set_expr=None, *args, **kwargs):
            global wells_walkthrough_runtime_menu
            global wells_walkthrough_runtime_choices
            try:
                current = renpy.game.context().current
                menu_node = None
                try:
                    menu_node = renpy.game.script.lookup_or_none(current)
                except:
                    pass
                if isinstance(menu_node, renpy.ast.Menu):
                    wells_walkthrough_runtime_menu = menu_node
                    wells_walkthrough_runtime_choices = list(items)
                else:
                    wells_walkthrough_runtime_menu = None
                    wells_walkthrough_runtime_choices = None
            except:
                wells_walkthrough_runtime_menu = None
                wells_walkthrough_runtime_choices = None
            return wells_walkthrough_original_menu(items, set_expr, *args, **kwargs)

        wells_walkthrough_menu_wrapper._wells_walkthrough_wrapped = True
        renpy.exports.menu = wells_walkthrough_menu_wrapper

    def wells_walkthrough_current_menu(items):
        try:
            if isinstance(wells_walkthrough_runtime_menu, renpy.ast.Menu):
                return wells_walkthrough_runtime_menu
        except:
            pass
        try:
            current = renpy.game.context().current
            node = renpy.game.script.lookup_or_none(current)
            if isinstance(node, renpy.ast.Menu):
                return node
        except:
            pass
        return None

    def wells_walkthrough_get_info(items, item):
        if not persistent.wells_walkthrough_enabled:
            return ""
        try:
            menu = wells_walkthrough_current_menu(items)
            if menu is None:
                return ""

            action = getattr(item, "action", None)
            menu_index = getattr(action, "value", None)
            block = None

            if isinstance(menu_index, int):
                if menu_index >= 0 and menu_index < len(menu.items):
                    block = menu.items[menu_index][2]

            if block is None:
                caption = item.caption if hasattr(item, "caption") else item[0]
                for menu_item in menu.items:
                    if str(menu_item[0]) == str(caption):
                        block = menu_item[2]
                        break

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
        return ""

    def wells_walkthrough_text_size(base_size):
        size = int(base_size)
        if size < 12:
            size = 12
        return size
