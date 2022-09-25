
void one_return_vio() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {
        return ;
    } else {

    }
}

void two_return_vio() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {
        return ;
    } else {
        return ;
    }
}

void compliant001() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {

    } else {

    }
    return ;
}

void compliant002() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {

    } else {

    }
}

void one_return_while() {
    while (g==3) {
        return;
    }
}

void break_while() {
    while (g==1) {
        g==2;
        break;
    }
    g==5;
}

void cont_while() {
    while (g==1) {
        g==2;
        continue;
    }
    g==5;
}
