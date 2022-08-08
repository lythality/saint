
int g;

void nested_compound() {
    int n;

    {
        {
            {
                n=1;
            }
        }
    }
}

void basic_if() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {

    } else if (a==4) {

    }
}

void basic_while() {
    while (g==3) {

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

//void complicated_while() {
//    while (g==1) {
//        g==2;
//        if (g==3) {
//            break;
//        }
//        if (g==4) {
//            continue;
//        }
//        break;
//    }
//    g==5;
//}

int main() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {

    } else if (a==4) {

    }

    return 0;
}