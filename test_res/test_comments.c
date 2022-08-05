
typedef int MY_INT;

int main() {
    int a, b, c;
    long d;

    // one line comment
    a = 10;

    // one line comment with escape \
    d = 20;
    d = 30;

    /* multi line comment
     *
    end*/
    b = 30;

    /* multi line comment with comment char - slash star
     * /*
    */
    c = a + b + 13;

    /* multi line comment with comment char - double slash
     * //
    */
    return c;
}