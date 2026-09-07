################################################################################
## WELLS FRAMEWORK — WALKTHROUGH
## BETA — INTERCEPTAÇÃO NO PONTO DO MENU
##
## Esta versão NÃO cria uma nova tela de choices.
## Ela usa o menu normal do Ren'Py e injeta a informação diretamente
## no caption que chega à tela "choice".
##
## Objetivo:
##   renpy.exports.menu(...)
##       -> localizar o Menu AST real
##       -> analisar o bloco da opção
##       -> acrescentar a consequência ao caption
##       -> devolver os mesmos itens ao Ren'Py
##
## A apresentação continua sendo responsabilidade de wells_choices.rpy.
################################################################################

default persistent.wells_walkthrough_enabled = False

init -1000 python:
    import ast as wells_py_ast

    class WellsWalkthroughConsequence(object):
        def __init__(self, kind, text):
            self.kind = kind
            self.text = text


    class WellsWalkthroughAnalyzer(object):

        MAX_RESULTS = 4

        def _python_source(self, code_obj):
            try:
                source = code_obj.source
                if source:
                    return source
            except:
                pass

            try:
                source = code_obj.py
                if source:
                    return source
            except:
                pass

            try:
                source = code_obj.sourcecode
                if source:
                    return source
            except:
                pass

            return None

        def _target_name(self, target):
            try:
                if isinstance(target, wells_py_ast.Name):
                    return target.id

                if isinstance(target, wells_py_ast.Attribute):
                    base = self._target_name(target.value)
                    if base:
                        return base + "." + target.attr
                    return target.attr

                if isinstance(target, wells_py_ast.Subscript):
                    base = self._target_name(target.value)
                    if base:
                        return base + "[...]"
            except:
                pass

            return None

        def _constant_text(self, value):
            try:
                if isinstance(value, wells_py_ast.Constant):
                    return repr(value.value)

                if isinstance(value, wells_py_ast.Str):
                    return repr(value.s)

                if isinstance(value, wells_py_ast.Num):
                    return repr(value.n)
            except:
                pass

            return None

        def _condition_text(self, test):
            try:
                return wells_py_ast.unparse(test)
            except:
                pass

            try:
                return wells_py_ast.dump(test)
            except:
                pass

            return "condição"

        def _append(self, result, kind, text):
            if len(result) >= self.MAX_RESULTS:
                return

            if not text:
                return

            text = str(text).strip()

            if not text:
                return

            for old in result:
                if old.kind == kind and old.text == text:
                    return

            result.append(WellsWalkthroughConsequence(kind, text))

        def _analyze_python(self, source, result):
            try:
                tree = wells_py_ast.parse(source)
            except:
                return

            for node in wells_py_ast.walk(tree):

                if len(result) >= self.MAX_RESULTS:
                    return

                try:
                    if isinstance(node, wells_py_ast.AugAssign):
                        name = self._target_name(node.target)

                        if not name:
                            continue

                        if isinstance(node.op, wells_py_ast.Add):
                            value = self._constant_text(node.value)
                            if value:
                                self._append(result, "increase",
                                             "%s +%s" % (name, value))
                            else:
                                self._append(result, "increase",
                                             "%s aumenta" % name)

                        elif isinstance(node.op, wells_py_ast.Sub):
                            value = self._constant_text(node.value)
                            if value:
                                self._append(result, "decrease",
                                             "%s -%s" % (name, value))
                            else:
                                self._append(result, "decrease",
                                             "%s diminui" % name)

                        else:
                            self._append(result, "assign",
                                         "%s é alterado" % name)

                    elif isinstance(node, wells_py_ast.Assign):
                        for target in node.targets:
                            name = self._target_name(target)

                            if not name:
                                continue

                            value = self._constant_text(node.value)

                            if value is not None:
                                self._append(result, "assign",
                                             "%s = %s" % (name, value))
                            else:
                                self._append(result, "assign",
                                             "%s é alterado" % name)

                    elif isinstance(node, wells_py_ast.If):
                        condition = self._condition_text(node.test)
                        self._append(result, "condition",
                                     "? %s" % condition)

                except:
                    pass

        def _walk_renpy(self, node, result, seen):
            if node is None or len(result) >= self.MAX_RESULTS:
                return

            try:
                marker = id(node)
                if marker in seen:
                    return
                seen.add(marker)
            except:
                pass

            try:
                if isinstance(node, renpy.ast.PyCode):
                    source = self._python_source(node)
                    if source:
                        self._analyze_python(source, result)

                elif isinstance(node, renpy.ast.Jump):
                    target = getattr(node, "target", None)
                    if target:
                        self._append(result, "jump", "⇒ %s" % target)

                elif isinstance(node, renpy.ast.Call):
                    label = getattr(node, "label", None)

                    if label:
                        self._append(result, "call", "⇒ %s" % label)

                elif isinstance(node, renpy.ast.If):
                    entries = getattr(node, "entries", None)

                    if entries:
                        for condition, block in entries:
                            if condition:
                                self._append(result, "condition",
                                             "? %s" % condition)

                            if block:
                                for child in block:
                                    self._walk_renpy(child, result, seen)

                                    if len(result) >= self.MAX_RESULTS:
                                        return
            except:
                pass

            try:
                getter = getattr(node, "get_children", None)

                if getter:
                    children = getter(lambda child: True)

                    if children:
                        for child in children:
                            self._walk_renpy(child, result, seen)

                            if len(result) >= self.MAX_RESULTS:
                                return
            except:
                pass

        def analyze(self, block):
            result = []

            if not block:
                return result

            seen = set()

            try:
                for node in block:
                    self._walk_renpy(node, result, seen)

                    if len(result) >= self.MAX_RESULTS:
                        break
            except:
                pass

            return result


    class WellsWalkthroughMenuFinder(object):

        def __init__(self):
            self._last_menu_node = None
            self._last_captions = None
            self._menu_history = []

        def _runtime_caption(self, item):
            try:
                if hasattr(item, "caption"):
                    return str(item.caption)
            except:
                pass

            try:
                if isinstance(item, (tuple, list)):
                    return str(item[0])
            except:
                pass

            return ""

        def _captions(self, items):
            result = []

            try:
                for item in items:
                    result.append(self._runtime_caption(item))
            except:
                pass

            return result

        def _menu_captions(self, node):
            result = []

            try:
                for item in node.items:
                    result.append(str(item[0]))
            except:
                pass

            return result

        def _similarity(self, runtime, menu):
            if not runtime or not menu:
                return 0.0

            matched = 0

            for caption in runtime:
                for menu_caption in menu:
                    if str(caption).strip() == str(menu_caption).strip():
                        matched += 1
                        break

            return float(matched) / float(max(len(runtime), len(menu), 1))

        def _collect_menu_nodes(self):
            nodes = []

            try:
                namemap = renpy.game.script.namemap

                for node in namemap.values():
                    try:
                        if isinstance(node, renpy.ast.Menu):
                            nodes.append(node)
                    except:
                        pass
            except:
                pass

            return nodes

        def _find_from_last(self, captions):
            node = self._last_menu_node

            if node is None:
                return None

            try:
                score = self._similarity(captions, self._menu_captions(node))

                if score >= 0.80:
                    return node
            except:
                pass

            return None

        def find_menu_node(self, items):
            captions = self._captions(items)

            if not captions:
                return None, None

            node = self._find_from_last(captions)

            if node is not None:
                self._last_captions = captions
                return node, "last"

            best_node = None
            best_score = 0.0
            best_index = -1

            try:
                all_nodes = self._collect_menu_nodes()

                for index, candidate in enumerate(all_nodes):
                    candidate_captions = self._menu_captions(candidate)
                    score = self._similarity(captions, candidate_captions)

                    if score > best_score:
                        best_score = score
                        best_node = candidate
                        best_index = index

                    if score >= 0.999:
                        break

                if best_node is not None and best_score >= 0.80:
                    self._last_menu_node = best_node
                    self._last_captions = captions

                    self._menu_history.append(best_index)

                    if len(self._menu_history) > 20:
                        self._menu_history.pop(0)

                    return best_node, "caption"

            except:
                pass

            return None, None


    wells_walkthrough_analyzer = WellsWalkthroughAnalyzer()
    wells_walkthrough_menu_finder = WellsWalkthroughMenuFinder()


    def wells_walkthrough_format(consequences):
        if not consequences:
            return ""

        parts = []

        for consequence in consequences:
            try:
                if consequence.kind == "increase":
                    color = "#39ff14"
                elif consequence.kind == "decrease":
                    color = "#ff4040"
                elif consequence.kind == "condition":
                    color = "#ffff66"
                elif consequence.kind == "jump":
                    color = "#ffb347"
                elif consequence.kind == "call":
                    color = "#66ff99"
                else:
                    color = "#66ffff"

                parts.append("{color=%s}%s{/color}" %
                             (color, consequence.text))
            except:
                pass

        return "  ".join(parts)


    def wells_walkthrough_get_info(items, item):
        """
        Compatibilidade com wells_choices.rpy.

        A versão atual injeta a informação no caption antes da tela choice.
        Portanto esta função não deve inserir uma segunda cópia.
        """
        return ""


    def wells_walkthrough_text_size(base_size):
        try:
            size = int(base_size)

            if size < 12:
                size = 12

            return size
        except:
            return 18


    def wells_walkthrough_enhance_items(items):
        if not persistent.wells_walkthrough_enabled:
            return items

        try:
            menu_node, match_method = wells_walkthrough_menu_finder.find_menu_node(items)

            if menu_node is None:
                return items

            enhanced = []

            for index, item in enumerate(items):
                try:
                    caption = wells_walkthrough_menu_finder._runtime_caption(item)
                    block = None

                    # Ren'Py 7.4.x / 8.x: exports.menu receives
                    # (caption, condition, value) before calling store.menu.
                    if isinstance(item, (tuple, list)) and len(item) >= 3:
                        value = item[2]

                        if isinstance(value, int):
                            try:
                                block = menu_node.items[value][2]
                            except:
                                block = None

                    # Fallback: resolve the block by caption.
                    if block is None:
                        try:
                            for menu_item in menu_node.items:
                                if str(menu_item[0]).strip() == str(caption).strip():
                                    block = menu_item[2]
                                    break
                        except:
                            pass

                    consequences = wells_walkthrough_analyzer.analyze(block)

                    if consequences:
                        formatted = wells_walkthrough_format(consequences)

                        if formatted:
                            new_caption = str(caption) + "\n" + formatted

                            if isinstance(item, tuple):
                                if len(item) >= 3:
                                    item = (new_caption,) + tuple(item[1:])
                                else:
                                    item = (new_caption,) + tuple(item[1:])
                            elif isinstance(item, list):
                                item = [new_caption] + list(item[1:])
                            else:
                                try:
                                    item.caption = new_caption
                                except:
                                    pass

                    enhanced.append(item)

                except:
                    enhanced.append(item)

            return enhanced

        except:
            return items


    def wells_walkthrough_install():
        try:
            original_menu = renpy.exports.menu

            if getattr(original_menu, "_wells_walkthrough_wrapper", False):
                return

            def wells_walkthrough_wrapped_menu(items,
                                               set_expr=None,
                                               args=None,
                                               kwargs=None,
                                               item_arguments=None):

                try:
                    items = list(items)
                except:
                    pass

                try:
                    enhanced_items = wells_walkthrough_enhance_items(items)
                except:
                    enhanced_items = items

                return original_menu(
                    enhanced_items,
                    set_expr,
                    args,
                    kwargs,
                    item_arguments
                )

            wells_walkthrough_wrapped_menu._wells_walkthrough_wrapper = True
            wells_walkthrough_wrapped_menu._wells_original_menu = original_menu

            renpy.exports.menu = wells_walkthrough_wrapped_menu

        except:
            pass


    wells_walkthrough_install()
