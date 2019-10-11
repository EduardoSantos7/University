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

void printInt(int m, int n, int arr[][n]){
    int i, j;
    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            printf("%d ", arr[i][j]);
        }
        printf("\n");
    }
}

void replace(char* old_value, char* new_value, int m, int n, char* arr[m][n]){
    int i, j;
    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            if (arr[i][j] == old_value){
                arr[i][j] = new_value;
            }
        }
    }
}

void replaceIntMat(int old_value, int new_value, int m, int n, int arr[m][n])
{
    int i, j;
    for (i = 0; i < m; i++)
    {
        for (j = 0; j < n; j++)
        {
            if (arr[i][j] == old_value)
            {
                arr[i][j] = new_value;
            }
        }
    }
}

int* indexes(int target, int m, int n, char* arr[][n], int avoidRow){
    int i, j;
    static int output[2] = {-1, -1};

    for(i = 0; i < m; i++){
        if (avoidRow == i)
            continue;

        for(j = 0; j < n; j++){
            if (((*arr[i][j]) - 48) == target){
                output[0] = i;
                output[1] = j;
                break;
            }
            else{
                output[0] = -1;
                output[1] = -1;
            }
        }

        if(output[0] != -1 || output[1] != -1)
            break;
    }

    return output;
}

void nums_to_internal(int m, int n, char* arr[m][n]){
    int i, j;
    for(i = 0; i < m; i++){
        for(j = 0; j < n; j++){
            if (*arr[i][j] > 48 && *arr[i][j] < 58){
                arr[i][j] = "I";
            }
            
        }
    }
}