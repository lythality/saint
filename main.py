import sys
import clang.cindex

import re

int_constants = []

def getTokenString(n):
    ret = ""
    for token in n.get_tokens():
        ret += token.spelling
    return ret

def isConstCharType(n):
    typename = n.type.spelling
    return "const" in typename and "char" in typename and \
        ("*" in typename or "[" in typename)

def hasConstCharTypeConstants(n):
    if n.kind.name == "STRING_LITERAL":
        return True
    for c in n.get_children():
        if hasConstCharTypeConstants(c):
            return True
    return False

def is_assignment(n):
    return "=" in getTokenString(n)

def traverse(n, i=0):
    global int_constants

    print(' ' * i, end="")
    print(n.kind, end="")
    print(" : ", end="")
    print(n.type.spelling, end="")
    print(" :: ", end="")
    print(getTokenString(n), end="")
    print(dir(n.kind), end="")
    print("")

    if n.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        int_constants.append(n)

    if n.kind.is_expression():
        if is_assignment(n):
            if not isConstCharType(n):
                if hasConstCharTypeConstants(n):
                    print(" > const char is assigned on non const char type")

    for c in n.get_children():
        traverse(c, i=i+1)


def isOctet(text: str) -> bool:
    return re.match(r"^0[0-7]+$", text)

def isLowerLongCharUsed(text: str) -> bool:
    return "l" in text


# 스크립트를 실행하려면 여백의 녹색 버튼을 누릅니다.
if __name__ == '__main__':
    clang.cindex.Config.set_library_file('C:/Program Files/LLVM/bin/libclang.dll')

    afile = './test.c'

    index = clang.cindex.Index.create()
    translation_unit = index.parse(afile, ['-x', 'c++'])
    traverse(translation_unit.cursor)

    print("=== CONSTANTS ===")
    for c in int_constants:
        print(c.kind, end=" : ")
        print(c.spelling or c.displayname, end=" :: ")
        text = ""
        for t in c.get_tokens():
            print(t.spelling, end=" ")
            text = text + t.spelling
        print(c.type.spelling, end=" - ")
        print(c.kind.name, end="")
        print(" > OCTET IS USED" if isOctet(text) else "", end="")
        print(" > LOWER LONG IS USED" if isLowerLongCharUsed(text) else "", end="")
        print()
