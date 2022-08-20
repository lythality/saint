import clang.cindex
from clang.cindex import TypeKind, CursorKind, TokenKind

from code_info.cfg import CFG
from code_info.cursor_util import get_if_body, get_else_body, get_while_body, get_switch_body, get_case_body, get_default_body
from code_info.util import getTokenString


class CFGTraverser:

    def __init__(self, _cfg):
        self.CFG = _cfg

    def traverse(self):
        self._traverse(self.CFG.init_node_id, [])

    def _traverse(self, curr_node_id, visited):
        # 1. check visited
        if curr_node_id in visited:
            return 0
        visited.append(curr_node_id)

        # 2. visit this node
        self.hook_each_node(curr_node_id)

        # 3. get next nodes
        next_node_ids = self.CFG.next(curr_node_id)

        # 4. visit next nodes
        for next_node_id in next_node_ids:
            self._traverse(next_node_id, visited)

    def hook_each_node(self, n):
        pass


class PathVisitor(CFGTraverser):

    def __init__(self, _cfg):
        super().__init__(_cfg)

    def traverse(self):
        self._traverse(self.CFG.init_node_id, [])

    def _traverse(self, curr_node_id, visited):
        # 1. get next nodes
        next_node_ids = self.CFG.next(curr_node_id)

        # 2. visit this path
        if not next_node_ids:
            visited.append(curr_node_id)
            self.hook_each_node(curr_node_id)
            self.hook_each_path(visited)
            visited.pop()
            return

        # 3. check visited (skip if every next node is visited / also visit if any next node is not visited)
        if self._is_all_edge_visited(visited, curr_node_id):
            return
        visited.append(curr_node_id)

        # 4. visit this node
        self.hook_each_node(curr_node_id)

        # 5. visit next nodes
        for next_node_id in next_node_ids:
            self._traverse(next_node_id, visited)
        visited.pop()

    def _is_all_edge_visited(self, path, curr_node_id):
        next_node_ids = self.CFG.next(curr_node_id)
        for next_node_id in next_node_ids:
            if not self._is_edge_passes(path, (curr_node_id, next_node_id)):
                return False
        return True

    @staticmethod
    def _is_edge_passes(path, edge):
        for i in range(len(path)-1):
            if path[i] == edge[0] and path[i+1] == edge[1]:
                return True
        return False

    def hook_each_path(self, path):
        pass
