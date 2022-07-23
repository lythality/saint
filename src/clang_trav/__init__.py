import clang.cindex
from clang.cindex import TypeKind, CursorKind

class ClangTrav:

    def start_trav(self, cfile):
        clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')

        index = clang.cindex.Index.create()
        translation_unit = index.parse(cfile, ['-x', 'c++'])
        self.traverse(translation_unit.cursor)

    def traverse(self, n, i=0):
        global var_names_scope
        self.print_info(n, i)

        var_names_inside_comp_stmt = []
        if n.kind == CursorKind.COMPOUND_STMT:
            self.hook_enter_comp_stmt(n, var_names_inside_comp_stmt)

        if n.kind == CursorKind.INTEGER_LITERAL:
            self.hook_integer_literal(n)

        if n.kind == CursorKind.FIELD_DECL:
            self.hook_field_decl(n)

        if n.kind == CursorKind.ENUM_DECL:
            self.hook_enum(n)

        if n.kind == CursorKind.CHARACTER_LITERAL:
            self.hook_char_literal(n)

        if n.kind == CursorKind.STRING_LITERAL:
            self.hook_string_literal(n)

        if n.kind.is_expression():
            self.hook_expression(n)

        # iterate recursively
        for c in n.get_children():
            self.traverse(c, i+1)

        if n.kind == CursorKind.COMPOUND_STMT:
            self.hook_exit_comp_stmt(n, var_names_inside_comp_stmt)

        self.post_visit(n)

    def hook_enter_comp_stmt(self, n: CursorKind):
        pass

    def hook_exit_comp_stmt(self, n: CursorKind):
        pass

    def hook_integer_literal(self, n: CursorKind):
        pass

    def hook_char_literal(self, n):
        pass

    def hook_string_literal(self, n):
        pass

    def hook_expression(self, n: CursorKind):
        pass

    def hook_field_decl(self, n: CursorKind):
        pass

    def hook_enum(self, n: CursorKind):
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
        print("")