
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


int main() {
    int a;

    a = 3+4+5+6+7;

    if (a==3) {

    } else if (a==4) {

    }

    return 0;
}