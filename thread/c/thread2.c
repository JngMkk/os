#include <stdio.h>
#include <unistd.h>
#include <pthread.h>


void* foo() {
    long tID = (long int) pthread_self();

    printf("PID is %d\n", getpid());
    printf("Thread ID is %ld\n", tID);

    return NULL;
}

int main(void) {
    pthread_t t1, t2, t3;
    pthread_create(&t1, NULL, foo, NULL);
    pthread_create(&t2, NULL, foo, NULL);
    pthread_create(&t3, NULL, foo, NULL);
    pthread_join(t1, NULL);
    pthread_join(t2, NULL);
    pthread_join(t3, NULL);

    return 0;
}

/*
PID is 6385
Thread ID is 6158266368
PID is 6385
Thread ID is 6158839808
PID is 6385
Thread ID is 6159413248
*/
