#include <stdio.h>
#include <unistd.h>

void foo(void) {
    printf("execute foo\n\n");
}

void bar(void) {
    printf("execute bar\n\n");
}

void baz(void) {
    printf("execute baz\n\n");
}

int main() {
    if (fork() == 0) {
        if (fork() == 0) {
            // 자식의 자식
            foo();
        } else {
            // 자식 프로세스
            bar();
        }
    } else {
        // 부모 프로세스
        baz();
    }
}

/*
execute baz

execute bar                                                                                                                                                                  

execute foo
*/
