import clang.cindex
from clang.cindex import TypeKind, CursorKind, TokenKind

from code_info.util import getTokenString

clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')


class SWorkspace:

    def __init__(self):
        self.source_files = []

        self.integer_literal = []
        self.character_literal = []
        self.string_literal = []
        self.function_decl = []
        self.function = []
        self.var_decl = []
        self.field_decl = []
        self.enum_decl = []
        self.expression = []
        self.comments = []

    def start_trav(self):
        index = clang.cindex.Index.create()
        for t_unit in self.source_files:
            t_unit.start_trav()

            self.integer_literal.extend(t_unit.integer_literal)
            self.character_literal.extend(t_unit.character_literal)
            self.string_literal.extend(t_unit.string_literal)
            self.function_decl.extend(t_unit.function_decl)
            self.function.extend(t_unit.function)
            self.var_decl.extend(t_unit.var_decl)
            self.field_decl.extend(t_unit.field_decl)
            self.enum_decl.extend(t_unit.enum_decl)
            self.expression.extend(t_unit.expression)
            self.comments.extend(t_unit.comments)

    def add_file(self, cfile):
        self.source_files.append(STranslationUnit(cfile))


class STranslationUnit:

    def __init__(self, cfile):
        self.cfile = cfile

        self.integer_literal = []
        self.character_literal = []
        self.string_literal = []
        self.function_decl = []
        self.function = []
        self.var_decl = []
        self.field_decl = []
        self.enum_decl = []
        self.expression = []
        self.comments = []

        # self.names_typedef = []
        # self.names_external_vars = []
        # self.names_internal_vars = []
        # self.names_local_vars = []
        # self.names_field_names = []
        # self.names_tags = []
        # self.external_vars = []

    def start_trav(self):
        index = clang.cindex.Index.create()
        translation_unit = index.parse(self.cfile, ['-x', 'c++'])
        self.traverse(translation_unit.cursor)
        self.collect_comments(translation_unit.cursor.get_tokens())

    def collect_comments(self, tokens):
        for t in tokens:
            if t.kind == TokenKind.COMMENT:
                self.comments.append(t)

    def traverse(self, n, i=0):
        self.print_info(n, i)

        var_names_inside_comp_stmt = []
        if n.kind == CursorKind.COMPOUND_STMT:
            self.hook_enter_comp_stmt(n, var_names_inside_comp_stmt)
        elif n.kind == CursorKind.INTEGER_LITERAL:
            self.integer_literal.append(n)
        elif n.kind == CursorKind.VAR_DECL:
            self.var_decl.append(n)
        elif n.kind == CursorKind.FIELD_DECL:
            self.field_decl.append(n)
        elif n.kind == CursorKind.ENUM_DECL:
            self.enum_decl.append(n)
        elif n.kind == CursorKind.CHARACTER_LITERAL:
            self.character_literal.append(n)
        elif n.kind == CursorKind.STRING_LITERAL:
            self.string_literal.append(n)
        elif n.kind == CursorKind.FUNCTION_DECL:
            self.function_decl.append(n)
            self.function.append(Function(n))
        elif n.kind.is_expression():
            self.expression.append(n)

        # iterate recursively
        for c in n.get_children():
            self.traverse(c, i+1)

        if n.kind == CursorKind.COMPOUND_STMT:
            self.hook_exit_comp_stmt(n, var_names_inside_comp_stmt)

        self.post_visit(n)

    def hook_enter_comp_stmt(self, n: CursorKind, var_names_inside_comp_stmt):
        pass

    def hook_exit_comp_stmt(self, n: CursorKind, var_names_inside_comp_stmt):
        pass

    def post_visit(self, n):
        pass

    def print_info(self, n, tab: int):
        print('\t' * tab, end="")
        print(n.kind, end="")
        print(" : ", end="")
        print(n.type.spelling, end="")
        print(" :: ", end="")
        print(n.spelling, end="")
        print(" :: ", end="")
        print(getTokenString(n), end="")
        print("")
        # print(n.data.__str__())


class Function:

    def __init__(self, function_decl):
        self.function_decl = function_decl
        self.node_map = {}
        self.control_flow = {}
        self.node_size = 0
        # self._construct_control_flow()

    def _construct_control_flow(self):
        init_node_id = self._get_new_node(DummyNode("INIT_node"))
        # There are at most one statement in function decl (mostly compound statement)
        assert(len([i for i in self.function_decl.get_children()]) == 1)
        for c in self.function_decl.get_children():
            start_node_id, end_node_id = self._construct_control_flow_common(c, [], [])
            exit_node_id = self._get_new_node(DummyNode("EXIT_node"))
            self._connect(init_node_id, start_node_id)
            self._connect(end_node_id, exit_node_id)
            break

    def _connect(self, curr, next):
        if curr is None:
            return
        self.control_flow[curr].append(next)

    # We do not just passing callers parameter down to callee
    # Always, parent connect start and end nodes
    # return: tuple of (start_node, end_node) of the block
    def _construct_control_flow_common(self, curr_node, o_break_node_ids, o_cont_node_ids):
        if curr_node.kind == CursorKind.COMPOUND_STMT:
            comp_start_node_id = self._get_new_node(DummyNode("COMP-START-"+getTokenString(curr_node)))
            before_node_id = comp_start_node_id

            for c in curr_node.get_children():
                start_node_id, end_node_id = self._construct_control_flow_common(c, o_break_node_ids, o_cont_node_ids)
                self._connect(before_node_id, start_node_id)
                before_node_id = end_node_id

            comp_end_node_id = self._get_new_node(DummyNode("COMP-END-"+getTokenString(curr_node)))
            self._connect(before_node_id, comp_end_node_id)
            return comp_start_node_id, comp_end_node_id
        elif curr_node.kind == CursorKind.IF_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))
            IF_CONDITION = 0
            IF_TRUE_STATEMENT = 1
            IF_FALSE_STATEMENT = 2
            IF_FULLY_ITERATED = 3
            state = IF_CONDITION
            for c in curr_node.get_children():
                if state == IF_CONDITION:
                    state = IF_TRUE_STATEMENT
                    continue
                elif state == IF_TRUE_STATEMENT:
                    start_node_id, end_node_id = self._construct_control_flow_common(c, o_break_node_ids, o_cont_node_ids)
                    self._connect(curr_node_id, start_node_id)
                    self._connect(end_node_id, merge_node_id)
                    state = IF_FALSE_STATEMENT
                elif state == IF_FALSE_STATEMENT:
                    start_node_id, end_node_id = self._construct_control_flow_common(c, o_break_node_ids, o_cont_node_ids)
                    self._connect(curr_node_id, start_node_id)
                    self._connect(end_node_id, merge_node_id)
                    state = IF_FULLY_ITERATED

            if state != IF_FULLY_ITERATED:
                dummy_else_node_id = self._get_new_node(DummyNode("EMPTY ELSE-" + getTokenString(curr_node)))
                self._connect(curr_node_id, dummy_else_node_id)
                self._connect(dummy_else_node_id, merge_node_id)
            return curr_node_id, merge_node_id
        elif curr_node.kind == CursorKind.WHILE_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))
            while_next_node_id = self._get_new_node(DummyNode("WHILE-NEXT-" + getTokenString(curr_node)))

            while_breaks = []
            while_continues = []

            WHILE_CONDITION = 0
            WHILE_BODY = 1
            WHILE_FULLY_ITERATED = 2
            state = WHILE_CONDITION
            for c in curr_node.get_children():
                if state == WHILE_CONDITION:
                    state = WHILE_BODY
                    continue
                elif state == WHILE_BODY:
                    start_node_id, end_node_id = self._construct_control_flow_common(c, while_breaks, while_continues)
                    self._connect(curr_node_id, start_node_id)
                    self._connect(end_node_id, merge_node_id)
                    state = WHILE_FULLY_ITERATED
            self._connect(merge_node_id, curr_node_id)
            self._connect(curr_node_id, while_next_node_id)
            for break_node_id in while_breaks:
                self._connect(break_node_id, while_next_node_id)
            for cont_node_id in while_continues:
                self._connect(cont_node_id, merge_node_id)
            return curr_node_id, while_next_node_id
        elif curr_node.kind == CursorKind.BREAK_STMT:
            curr_node_id = self._get_new_node(curr_node)
            o_break_node_ids.append(curr_node_id)
            return curr_node_id, None
        elif curr_node.kind == CursorKind.CONTINUE_STMT:
            curr_node_id = self._get_new_node(curr_node)
            o_cont_node_ids.append(curr_node_id)
            return curr_node_id, None
        elif curr_node.kind == CursorKind.BINARY_OPERATOR \
                or curr_node.kind == CursorKind.DECL_STMT \
                or curr_node.kind == CursorKind.RETURN_STMT:
            curr_node_id = self._get_new_node(curr_node)
            return curr_node_id, curr_node_id

        # not matched any
        print("UNKNOWN KIND:", getTokenString(curr_node), curr_node.kind)
        return None

    def _get_new_node(self, n):
        new_id = self.node_size
        self.node_size += 1

        # remember node id to node object
        self.node_map[new_id] = n
        self.control_flow[new_id] = []

        return new_id

    def get_control_flow_graph_info(self):
        ret = "=== " + self.function_decl.spelling + " ===\n"
        for n in self.node_map.keys():
            if self.node_map[n] is not None:
                ret += "%s %s %s\n" %(str(n), str(self.control_flow[n]), getTokenString(self.node_map[n]))
            else:
                ret += "%s %s\n" % (str(n), str(self.control_flow[n]))
        return ret

class DummyToken:

    def __init__(self, name):
        self.spelling = name

class DummyNode:

    def __init__(self, name):
        self.tokens = [DummyToken(txt) for txt in name.split()]

    def get_tokens(self):
        return self.tokens
