#include <string.h>
#include "MatrixUtils.h"
#include "Stack.h" 

void verify(int m, int n, char* arr[m][n]){

    // Mark receives events
    int count_receives = 1;
    struct Stack* receives_stack = createStack(NULL);
    int i, j;

    /*Check if the difference is 1*/
    for(i = 0; i < m; i++){
        for(j = 1; j < n; j++){
            if(strlen(arr[i][j-1]) == 2){
                if(*arr[i][j] != '0' && *arr[i][j] - peek(receives_stack) != 1){
                    printf("ewfw");
                    push(receives_stack, *arr[i][j], i);
                    size_t len = strlen("r");
                    char *str2 = malloc(len + 1 + 1 ); /* one for extra char, one for trailing zero */
                    strcpy(str2, "r");
                    str2[len] = count_receives++ + '0'; // Cast
                    str2[len + 1] = '\0';
                    arr[i][j] = str2;
                }
            }
            else if(*arr[i][j] != '0' && *arr[i][j] - *arr[i][j-1] != 1){
                push(receives_stack, *arr[i][j], i);
                size_t len = strlen("r");
                char *str2 = malloc(len + 1 + 1 ); /* one for extra char, one for trailing zero */
                strcpy(str2, "r");
                str2[len] = count_receives++ + '0'; // Cast
                str2[len + 1] = '\0';
                arr[i][j] = str2;
            }
        }
    }
    /*Check if the first element in each row is 1*/
    for(i = 0; i < m; i++){
        if(strcmp(arr[i][0], "1") != 0){
            push(receives_stack,  *arr[i][0], i);
            size_t len = strlen("r");
            char *str2 = malloc(len + 1 + 1 ); /* one for extra char, one for trailing zero */
            strcpy(str2, "r");
            str2[len] = count_receives++ + '0'; // Cast
            str2[len + 1] = '\0';
            arr[i][0] = str2;
        }
    }

    /*Search the send message*/
    while(!is_empty(receives_stack)){
        struct StackNode* node = pop(receives_stack);
        int* inds = indexes(node->value - 1, m, n, arr, -1);

        if(inds[0] == -1 || inds[1] == -1){
            printf("INCORRECT\n");
            break;
        }

        size_t len = strlen("s");
        char *str2 = malloc(len + 1 + 1 ); /* one for extra char, one for trailing zero */
        strcpy(str2, "s");
        str2[len] = --count_receives + '0'; // Cast
        str2[len + 1] = '\0';
        arr[inds[0]][inds[1]] = str2;
    }
    replace("0", NULL, m, n, arr);
    print(m,n, arr);

}

int main(){
    char* in[3][4] = {
        {"1", "2", "8", "9"},
        {"1", "6", "7", "0"},
        {"2", "3", "4", "5"},
    };
    verify(3, 4, in);

    return 0;
}