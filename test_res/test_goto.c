
void f(void) {
    int j = 0;
L1:
    ++j;
    if (10 == j) {
        goto L2;
    }

    goto L1;

L2:
    ++j;
}