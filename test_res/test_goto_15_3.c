void f_15_3(int a) {
    if ( a <= 0 ) {
        goto L2;
    }

    goto L1;

    if ( a == 0 ) {
        goto L1;
    }

    goto L2;
L1:
    if ( a > 0 ) {
    L2:
        ;
    }

}
