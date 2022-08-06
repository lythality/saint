
extern int ext_arr_001[4];
extern int ext_arr_002[];

int dead_arr[4] = 3;

int arr[4] = {0,1,2,3};
int arr_indexed[2][2][2][2] = {[0][1][0][1]=1};

int t[2] = {[0]=1, 2};

int arr_2d[4][2]        = {{1,2},{3,4},{5,6},{7,8}};
int arr_2d_linear[4][2] = {1,2,3,4,5,6,7,8};
int arr_2d_dup[4][2]    = {{1,2},{3,4},{5,6},{7,8},[1][1]=9};

int arr_no_size[]       = {0,1};
int arr_no_size_2[]     = {[0]=1};

int arr_2d_some_idx_def[4][2] = {[0][0]=1, [0][1]=1, [1][0]=1, [1][1]=1,
                                [2][0]=1,           [3][0]=1, [3][1]=1, };
int arr_2d_full_idx_def[4][2] = {[0][0]=1, [0][1]=1, [1][0]=1, [1][1]=1,
                                [2][0]=1, [2][1]=1, [3][0]=1, [3][1]=1, };

//int arr_2d_indexed[4][2] = {[1]={1,2},{3,4}};
//int arr_2d_2d_idxed[4][2] = {[1][1]={2},{4}};

int main() {
    int a, b, c;
    long d;
    return c;
}