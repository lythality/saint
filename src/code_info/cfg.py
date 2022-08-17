import clang.cindex
from clang.cindex import TypeKind, CursorKind, TokenKind

from code_info.cursor_util import get_if_body, get_else_body, get_while_body, get_switch_body, get_case_body, get_default_body
from code_info.util import getTokenString

clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')


class CFG:

    def __init__(self):
        self.func_name = ""
        self.node_map = {}
        self.control_flow = {}
        self.node_size = 0
        self.init_node_id = -1

    def initialize(self):
        self.func_name = ""
        self.node_map = {}
        self.control_flow = {}
        self.node_size = 0
        self.init_node_id = -1

    def construct_cfg_by_clang_func_decl(self, function_decl):
        self.initialize()

        self.func_name = function_decl.spelling

        self.init_node_id = self._get_new_node(DummyNode("INIT_node"))
        # There are at most one statement in function decl (mostly compound statement)
        # assert(len([i for i in self.function_decl.get_children()]) == 1)
        for c in function_decl.get_children():
            # skip param declarations
            if c.kind == CursorKind.PARM_DECL:
                continue

            # body iteration
            goto_node_ids = []
            label_node_ids = []
            start_node_id, end_node_id = self._construct_control_flow_common(c, [], [], goto_node_ids, label_node_ids)
            exit_node_id = self._get_new_node(DummyNode("EXIT_node"))
            self._connect(self.init_node_id, start_node_id)
            self._connect(end_node_id, exit_node_id)

            # handle goto->label
            for goto_node_id in goto_node_ids:
                goto_node = self.node_map[goto_node_id]
                goto_label = getTokenString(goto_node)
                if goto_label.startswith("goto"):
                    goto_label = goto_label[4:]
                for label_node_id in label_node_ids:
                    label_node = self.node_map[label_node_id]
                    if goto_label == label_node.spelling:
                        self._connect(goto_node_id, label_node_id)
                        break
            break

    def _connect(self, curr, next):
        if curr is None:
            return
        self.control_flow[curr].append(next)

    # We do not just passing callers parameter down to callee
    # Always, parent connect start and end nodes
    # return: tuple of (start_node, end_node) of the block
    def _construct_control_flow_common(self, curr_node, o_break_node_ids, o_cont_node_ids, o_goto_node_ids, o_label_node_ids):
        if curr_node.kind == CursorKind.COMPOUND_STMT:
            comp_start_node_id = self._get_new_node(DummyNode("COMP-START-"+getTokenString(curr_node)))
            before_node_id = comp_start_node_id

            for c in curr_node.get_children():
                start_node_id, end_node_id = self._construct_control_flow_common(c, o_break_node_ids, o_cont_node_ids, o_goto_node_ids, o_label_node_ids)
                self._connect(before_node_id, start_node_id)
                before_node_id = end_node_id

            comp_end_node_id = self._get_new_node(DummyNode("COMP-END-"+getTokenString(curr_node)))
            self._connect(before_node_id, comp_end_node_id)
            return comp_start_node_id, comp_end_node_id
        elif curr_node.kind == CursorKind.IF_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))

            if_body_node = get_if_body(curr_node)
            start_node_id, end_node_id = self._construct_control_flow_common(if_body_node, o_break_node_ids, o_cont_node_ids, o_goto_node_ids, o_label_node_ids)
            self._connect(curr_node_id, start_node_id)
            self._connect(end_node_id, merge_node_id)

            else_body_node = get_else_body(curr_node)
            if else_body_node is not None:
                start_node_id, end_node_id = self._construct_control_flow_common(else_body_node, o_break_node_ids, o_cont_node_ids, o_goto_node_ids, o_label_node_ids)
                self._connect(curr_node_id, start_node_id)
                self._connect(end_node_id, merge_node_id)
            else:
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

            while_body = get_while_body(curr_node)

            start_node_id, end_node_id = self._construct_control_flow_common(while_body, while_breaks, while_continues, o_goto_node_ids, o_label_node_ids)
            self._connect(curr_node_id, start_node_id)
            self._connect(end_node_id, merge_node_id)

            self._connect(merge_node_id, curr_node_id)
            self._connect(curr_node_id, while_next_node_id)
            for break_node_id in while_breaks:
                self._connect(break_node_id, while_next_node_id)
            for cont_node_id in while_continues:
                self._connect(cont_node_id, merge_node_id)
            return curr_node_id, while_next_node_id
        elif curr_node.kind == CursorKind.SWITCH_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))

            switch_breaks = []

            switch_body = get_switch_body(curr_node)

            start_node_id, end_node_id = self._construct_control_flow_common(switch_body, switch_breaks, o_cont_node_ids, o_goto_node_ids, o_label_node_ids)
            self._connect(curr_node_id, start_node_id)
            self._connect(end_node_id, merge_node_id)

            for break_node_id in switch_breaks:
                self._connect(break_node_id, merge_node_id)
            return curr_node_id, merge_node_id
        elif curr_node.kind == CursorKind.CASE_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))

            case_body = get_case_body(curr_node)

            start_node_id, end_node_id = self._construct_control_flow_common(case_body, o_break_node_ids,
                                                                             o_cont_node_ids, o_goto_node_ids, o_label_node_ids)
            self._connect(curr_node_id, start_node_id)
            self._connect(end_node_id, merge_node_id)

            self._connect(curr_node_id, merge_node_id)
            return curr_node_id, merge_node_id
        elif curr_node.kind == CursorKind.DEFAULT_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))

            default_body = get_default_body(curr_node)

            start_node_id, end_node_id = self._construct_control_flow_common(default_body, o_break_node_ids,
                                                                             o_cont_node_ids, o_goto_node_ids, o_label_node_ids)
            self._connect(curr_node_id, start_node_id)
            self._connect(end_node_id, merge_node_id)

            return curr_node_id, merge_node_id
        elif curr_node.kind == CursorKind.BREAK_STMT:
            curr_node_id = self._get_new_node(curr_node)
            o_break_node_ids.append(curr_node_id)
            return curr_node_id, None
        elif curr_node.kind == CursorKind.CONTINUE_STMT:
            curr_node_id = self._get_new_node(curr_node)
            o_cont_node_ids.append(curr_node_id)
            return curr_node_id, None
        elif curr_node.kind == CursorKind.GOTO_STMT:
            curr_node_id = self._get_new_node(curr_node)
            o_goto_node_ids.append(curr_node_id)
            return curr_node_id, curr_node_id
        elif curr_node.kind == CursorKind.LABEL_STMT:
            curr_node_id = self._get_new_node(curr_node)
            merge_node_id = self._get_new_node(DummyNode("MERGE-"+getTokenString(curr_node)))
            for c in curr_node.get_children():
                start_node_id, end_node_id = self._construct_control_flow_common(c, o_break_node_ids,
                                                                             o_cont_node_ids, o_goto_node_ids,
                                                                             o_label_node_ids)
                self._connect(curr_node_id, start_node_id)
                self._connect(end_node_id, merge_node_id)
            o_label_node_ids.append(curr_node_id)
            return curr_node_id, merge_node_id
        elif curr_node.kind == CursorKind.BINARY_OPERATOR \
                or curr_node.kind == CursorKind.UNARY_OPERATOR \
                or curr_node.kind == CursorKind.DECL_STMT \
                or curr_node.kind == CursorKind.RETURN_STMT:
            curr_node_id = self._get_new_node(curr_node)
            return curr_node_id, curr_node_id
        elif curr_node.kind == CursorKind.NULL_STMT:
            curr_node_id = self._get_new_node(DummyNode("empty statement"))
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
        ret = "=== " + self.func_name + " ===\n"
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
