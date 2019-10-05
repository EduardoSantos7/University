#include <stdio.h>

void print(int m, int n, char* arr[][n]){
    int i, j;
    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            printf("%s ", arr[i][j]);
        }
        printf("\n");
    }
}

void replace(char* old_value, char* new_value, int m, int n, char* arr[][n]){
    int i, j;
    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            if (arr[i][j] == old_value){
                arr[i][j] = new_value;
            }
        }
    }
}

int* indexes(char* target, int m, int n, char* arr[][n], int avoidRow){
    int i, j;
    static int output[2] = {-1, -1};
    for(i = 0; i < m; i++){
        if (avoidRow == i)
            continue;

        for(j = 0; j < n; j++){
            if (arr[i][j] == target){
                output[0] = i;
                output[1] = j;
            }
        }
    }
    return output;
}