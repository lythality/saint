import sys
import clang.cindex

import re

constants = []

def traverse(n, i=0):
    global constants

    print(' ' * i, end="")
    print(n.kind, end="")
    print(" : ", end="")
    print(n.spelling, end="")
    print("")

    if n.kind == clang.cindex.CursorKind.INTEGER_LITERAL:
        constants.append(n)

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
    for c in constants:
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
