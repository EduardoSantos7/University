#include <stdlib.h>

struct StackNode {
    int value;
    struct StackNode* next;
};

struct Stack{
    struct StackNode* top;
};

struct StackNode* createStackNode(int value, struct StackNode* next){
    struct StackNode* node = (struct StackNode*)malloc(sizeof(struct StackNode));
    node->value = value;
    node->next = next;
    return node;
}

void push(struct Stack* stack, int item){
    if(!stack->top){
        struct StackNode* node = createStackNode(item, NULL);
        stack->top = node;
    }
    else{
        struct StackNode* node = createStackNode(item, stack->top);
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
