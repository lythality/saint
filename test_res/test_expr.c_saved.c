int main() {
    char char001 = 'k';
    char char002 = '??\'';

    const char* str001 = "?\?!";
    const char* str002;
    const char* str003;
    char* str004 = "abcde";

    bool boolVar = false;
    char charVar;
    int signedVar;
    unsigned char unsignedVar;
    float floatingVar;

    // array access
    str004[boolVar] = 'a';
    str004[charVar] = 'a';
    str004[signedVar] = 'a';
    str004[unsignedVar] = 'a';W
    str004[floatingVar] = 'a';

    // unary access
    +boolVar;
    +charVar;
    +signedVar;
    +unsignedVar;
    -unsignedVar;
    +floatingVar;

    // + - access
    boolVar+charVar;
    signedVar+unsignedVar;

    int a;
    // unary operator
    a = +1;
    a = -1;

    // binary operator
    a = 2 + 3;
    a = 2 * a;
    a = a % 7;

    // conditional operator
    a = 3 < 2;
    a = 2 > 3;
    a = a <= 3;
    a = a >= 3;
    a = a == 3;
    a = a != 3;
    a = !false;
    a = a && 3;
    a = a || 3;

    // shift operator
    a = a << 3;

    // conditional operator 2
    a = ~ 3;
    a = a & 3;
    a = a | 3;
    a = a ^ 3;

    // ternary
    a == 3 ? 7 : 3;

    return 0;
}
