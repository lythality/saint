import clang.cindex
from clang.cindex import TypeKind, CursorKind, TokenKind

from code_info.cursor_util import get_if_body, get_else_body, get_while_body, get_switch_body, get_case_body, get_default_body
from code_info.util import getTokenString
from code_info.cfg import CFG

clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')


class SWorkspace:

    def __init__(self):
        self.source_files = []

        self.translation_unit = []
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

            self.translation_unit.extend(t_unit.translation_unit)
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

        self.translation_unit = []
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
        if n.kind == CursorKind.TRANSLATION_UNIT:
            self.translation_unit.append(n)
        elif n.kind == CursorKind.COMPOUND_STMT:
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
        self.cfg = CFG()
        self.cfg.construct_cfg_by_clang_func_decl(function_decl)
