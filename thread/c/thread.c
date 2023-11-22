#include <stdio.h>
#include <unistd.h>
#include <pthread.h>


void* foo() {
    long tID = (long int) pthread_self();   // 스레드 고유 식별자

    printf("PID is %d\n", getpid());
    printf("Thread ID is %ld\n", tID);

    return NULL;
}

int main(void) {
    pthread_t t1;
    pthread_create(&t1, NULL, foo, NULL);   // t1은 foo를 실행하도록 생성
    pthread_join(t1, NULL);                 // t1 실행

    return 0;
}

/*
PID is 6278
Thread ID is 6122893312
*/
