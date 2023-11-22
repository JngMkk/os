#include <stdio.h>
#include <unistd.h>

void foo(void) {
    printf("executed!\n\n");
}

int main(void) {
    /*
        fork를 통해 자식 프로세스 생성
        fork() => 결과로 반환되는 값이 0인 프로세스는 자식 프로세스.
                  결과로 반환되는 값이 자식프로세스의 PID인 프로세스는 부모 프로세스.
        
        fork가 된 순간 동일한 코드를 실행하는 자식 프로세스가 생성됨.
        자식 프로세스는 얼마든지 또 다른 자식 프로레스를 생성할 수도 있고,
        부모 프로세스 또한 또다른 자식 프로세스를 생성할 수 있음.
    */
    if (fork() == 0) {
        if (fork() == 0) {
            printf("Child of Child PID is %d\n", getpid());
            foo();
        } else {
            printf("Child2 PID is %d\n", getpid());
            foo();
        }
    } else {
        if (fork() == 0) {
            printf("Child1 PID is %d\n", getpid());
            foo();
        } else {
            printf("Parent PID is %d\n", getpid());    
            foo();
        }
    }

    return 0;
}

/*
Child1 PID is 5405
executed!

Parent PID is 5403
executed!

Child2 PID is 5404
executed!

Child of Child PID is 5406                                                                                                                                                   
executed!
*/
