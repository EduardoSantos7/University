#include <stdlib.h>

struct StackNode {
    int value;
    int row;
    struct StackNode* next;
};

struct Stack{
    struct StackNode* top;
};

struct StackNode* createStackNode(int value, int row, struct StackNode* next){
    struct StackNode* node = (struct StackNode*)malloc(sizeof(struct StackNode));
    node->value = value;
    node->row = row;
    node->next = next;
    return node;
}

struct Stack* createStack(struct StackNode* top){
    struct Stack* stack = (struct Stack*)malloc(sizeof(struct Stack));
    stack->top = top;
    return stack;
}

void push(struct Stack* stack, int item, int row){
    if(!stack->top){
        
        struct StackNode* node = createStackNode(item, row, NULL);
        stack->top = node;
    }
    else{
        struct StackNode* node = createStackNode(item, row, stack->top);
        stack->top = node;
    }
}

struct StackNode* pop(struct Stack* stack){
    if(!stack->top){
        return NULL;
    }
    else{
        struct StackNode* node = stack->top;
        stack->top = stack->top->next;
        return node;
    }
}

int peek(struct Stack* stack){
    if(!stack->top){
        return -1;
    }
    else{
        return stack->top->value;
    }
}

int is_empty(struct Stack* stack){
    return (stack->top)? 0 : 1;
}
