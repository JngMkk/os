#include <stdio.h>
#include <unistd.h>
#include <pthread.h>


void* foo() {
    long tID = (long int) pthread_self();
    printf("foo => PID: %d, Thread ID: %ld\n", getpid(), tID);
    return NULL;
}

void* bar() {
    long tID = (long int) pthread_self();
    printf("bar => PID: %d, Thread ID: %ld\n", getpid(), tID);
    return NULL;
}

void* baz() {
    long tID = (long int) pthread_self();
    printf("baz => PID: %d, Thread ID: %ld\n", getpid(), tID);
    return NULL;
}

int main(void) {
    pthread_t t1, t2, t3;
    pthread_create(&t1, NULL, foo, NULL);
    pthread_create(&t2, NULL, bar, NULL);
    pthread_create(&t3, NULL, baz, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    return 0;
}

/*
foo => PID: 6585, Thread ID: 6093860864
bar => PID: 6585, Thread ID: 6094434304
baz => PID: 6585, Thread ID: 6095007744
*/
