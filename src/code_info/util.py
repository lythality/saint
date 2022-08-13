
def getTokenString(n):
    if n is None:
        return "NONE"
    ret = ""
    for token in n.get_tokens():
        ret += token.spelling
    return ret
