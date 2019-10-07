#include <string.h>
#include "MatrixUtils.h"
#include "Stack.h" 


/*Return the number next to character as int i.e. in: s1 out: 1*/
int get_event_number(char* event){
    return *(event + 1) - 48;
}

int max(int a, int b){
    return (a > b) ? a : b;
}

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

void calculate(int m, int n, char* arr[m][n]){

    struct Stack* receives_stack = createStack(NULL);
    int out[m][n];
    int send_events[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int i, j, before, max_count;

    do{
        struct StackNode* previous_receive = pop(receives_stack);
        int init_i = (previous_receive) ? previous_receive->value : 0;
        int init_j = (previous_receive) ? previous_receive->row : 0;

        for (i=init_i; i < m; i++){
            int count = 0;
            for (j=init_j; j < n; j++){
                if(!arr[i][j])
                    continue;
                /* Check if the event type is send*/
                if(strncmp(arr[i][j], "s", 1) == 0){
                    before = (j > 0) ? out[i][j-1] : 0;
                    out[i][j] = before + 1;
                    send_events[get_event_number(arr[i][j]) - 1] = before + 1;
                }
                /* Check if the event type is receive*/
                else if(strncmp(arr[i][j], "r", 1) == 0){
                    /*Check if the send event of rx is already known*/
                    int send = send_events[get_event_number(arr[i][j]) - 1];
                    if(send){
                        out[i][j] = send + 1;
                    }
                    else{
                        push(receives_stack, i, j);
                        break;
                    }
                }
                else{
                    before = (j > 0) ? out[i][j-1] : 0;
                    max_count = max(count++, before);
                    out[i][j] = max_count + 1;
                }
            }   
        }
    }
    while(!is_empty(receives_stack));

    printInt(m,n,out);
}

int main(){
    char* in[3][4] = {
        {"1", "2", "8", "9"},
        {"1", "6", "7", "0"},
        {"2", "3", "4", "5"},
    };
    char* in2[3][4] = {
        {"a", "s1", "r3", "b"},
        {"c", "r2", "s3", NULL},
        {"r1", "d", "s2", "e"},
    };
    //verify(3, 4, in);
    calculate(3, 4, in2);

    return 0;
}