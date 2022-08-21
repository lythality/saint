
typedef int MY_INT;

int main() {
    int a, b, c;
    long d;

    const char* const_str;
    char* just_str;


    // octet check
    a = 234580;
    b = 31328;
    c = a + b + 013;

    // non-obvious signed int check
    a = 0x8000 // non-compliant
    a = 0x7fff // compliant

    // long check
    d = 123l
    d = 234L

    // string check
    const_str = "AA";
    just_str = "AA";

    // escape seq
    const char *hexa1 = "\x41g";
    const char *hexa2 = "\x41" "g";
    const char *hexa3 = "\x41\x67";

    int octal1 = '\141t';
    int octal2 = '\141\t';

    return c;
}