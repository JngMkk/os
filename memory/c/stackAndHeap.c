#include <stdlib.h>
#include <stdio.h>

int* func1(int a) {
    int *tmp = (int*)malloc(sizeof(int));       // 힙 메모리 확보 (stack pointer 3)
    *tmp = a * 20;                              // stack pointer 3가 heap memory(a * 20)을 가리킴
    printf("%p\n", &*tmp);                      // 힙 메모리 주소
    printf("%p\n", &tmp);                       // 포인터 변수 tmp의 주소
    return tmp;                                 // stack pointer 3 해제
}

void func2() {
    int a = 10;                                 // stack pointer 1
    int *b = func1(a);                          // stack pointer 2가 heap memory(a * 20)을 가리킴
    free(b);                                    // heap memory 해제
}

int main() {
    func2();
    // stack pointer 2 해제
    // stack pointer 1 해제
    return 0;
}
