#include <stdio.h>
#include <pthread.h>

int sum = 0;

void* produce(void *arg) {
    for (int i = 0; i < 100000; i++) {
        sum++;
    }

    return NULL;
}

void* consume(void *arg) {
    for (int i = 0; i < 100000; i++) {
        sum--;
    }

    return NULL;
}

int main(void) {
    printf("초기 합계: %d\n", sum);

    pthread_t producer, consumer;
    pthread_create(&producer, NULL, produce, NULL);
    pthread_create(&consumer, NULL, consume, NULL);
    pthread_join(producer, NULL);
    pthread_join(consumer, NULL);

    printf("producer/consumer 스레드 실행 이후 합계: %d\n", sum);

    return 0;
}

/*
초기 합계: 0
producer/consumer 스레드 실행 이후 합계: -46026
    => 동기화가 되지 않아서 생기는 문제!
*/
