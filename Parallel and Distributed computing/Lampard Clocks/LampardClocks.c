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

char* create_event(char* type, int number){
    size_t len = strlen(type);
    char *str2 = malloc(len + 1 + 1 ); /* one for extra char, one for trailing zero */
    strcpy(str2, type);
    str2[len] = number + '0'; // Cast
    str2[len + 1] = '\0';
    return str2;
}

void verify(int m, int n, char* arr[m][n]){
    int semaphores[25] = {0,0,0,0,0,0,0,0,0, 0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0};
    struct Stack* receives_stack = createStack(NULL);
    char*  out[m][n];
    int i, j;

    // Copy arr in out
    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            out[i][j] = arr[i][j];
        }
    }

    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            if(!strcmp(arr[i][j], "0"))
                continue;
            // Detection of receive events
            // Check if the first element in a row is not 1
            if( (j == 0) && strcmp(arr[i][j], "1") != 0 ){
                push(receives_stack,  *arr[i][j] - 48, i, j);
            }
            else if(j > 0 && (*arr[i][j] - *arr[i][j-1] != 1) ){
                push(receives_stack,  *arr[i][j] - 48, i, j);
            }
        }
    }

    int counter = 1;
    int flag = 1;

    while(!is_empty(receives_stack)){
        struct StackNode* elem = pop(receives_stack);

        // Check if the value have beenn searched before
        if (semaphores[elem->value - 1]){ // Using Thruthy values
            out[elem->row][elem->column] = create_event("r", semaphores[elem->value - 1]);
        }
        else{
            int* ind = indexes(elem->value - 1, m, n, arr, elem->row);
            // // If there is no a value print invalid
            if (ind[0] == -1){
                flag = 0;
                printf("INVALID\n");
                break;
            }

            // Update counter and change the output
            out[elem->row][elem->column] = create_event("r", counter);
            out[ind[0]][ind[1]] = create_event("s", counter);
            semaphores[elem->value - 1] = counter++;
        }
        free(elem);
    }

    free(receives_stack);

    if(flag){
        nums_to_internal(m, n, out);
        replace("0", NULL, m, n, out);
        print(m, n, out);
    }


}

void calculate(int m, int n, char* arr[m][n]){

    struct Stack* receives_stack = createStack(NULL);
    int out[m][n];
    int send_events[10] = {0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    int i, j, before, max_count;

    do{
        struct StackNode* previous_receive = pop(receives_stack);
        int init_i = (previous_receive) ? previous_receive->row : 0;
        int init_j = (previous_receive) ? previous_receive->column : 0;

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
                        push(receives_stack, 0, i, j);
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

    replaceIntMat((int)NULL, 0, m, n, out);
    printInt(m,n,out);
}

int main(){
    char* in[3][4] = {
        {"1", "2", "8", "9"},
        {"1", "6", "7", "0"},
        {"2", "3", "4", "5"},
    };
    char* in2[3][4] = {
        {"s1", "b", "r3", "e"},
        {"a", "r2", "s3", NULL},
        {"r1", "c", "d", "s2"},
    };
    verify(3, 4, in);
    calculate(3, 4, in2);

    return 0;
}