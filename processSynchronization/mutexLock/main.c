#include <stdio.h>
#include <pthread.h>

#define NUM_THREADS 4

pthread_mutex_t mutex = PTHREAD_MUTEX_INITIALIZER; // mutex lock 초기화
int shared = 0;

void* foo() {
    // acquire
    pthread_mutex_lock(&mutex);
    for (int i = 0; i < 10000; ++i) {
        shared += 1;
    }
    // release 
    pthread_mutex_unlock(&mutex);

    return NULL;
}

int main() {
    pthread_t threads[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_create(&threads[i], NULL, foo, NULL);
    }

    for (int i = 0; i < NUM_THREADS; ++i) {
        pthread_join(threads[i], NULL);
    }

    printf("final result is %d\n", shared);
    return 0;
}

/*
final result is 40000
*/
