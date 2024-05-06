#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

#define NUM_THREADS 10

// pthread에서 스레드용 함수는 void* 타입의 값을 받아 void* 타입의 값을 반환하는 함수여야 함.
// 인수 arg는 스레드 생성 시 전달되며 void* 타입임.
// 스레드용 함수. 이 함수가 동시에 동작함.
void* thread_func(void *arg) {
    int id = (int)arg;
    for (int i = 0; i < 5; i++) {
        printf("id = %d, i = %d\n", id, i);
        sleep(1);
    }

    return "finished!";
}

int main(int argc, char *argv[]) {
    pthread_t v[NUM_THREADS];

    for (int i = 0; i < NUM_THREADS; i++) {
        /*
            첫 번째 인수에 pthread_t 타입의 포인터를 받음.
            두 번째 인수에 스레드의 특징을 나타내는 어트리뷰트를 전달함. NULL을 전달해 기본 어트리뷰트를 적용함.
            세 번째 인수에는 스레드 생성용 함수를 전달하고, 네 번째 인수에는 세 번째 인수에 전달한 함수의 인수를 전달함.
        */
        if (pthread_create(&v[i], NULL, thread_func, (void*)i) != 0) {
            perror("pthread_create");
            return -1;
        }
    }

    for (int i = 0; i < NUM_THREADS; i++) {
        char *ptr;
        if (pthread_join(v[i], (void **)&ptr) == 0) {
            printf("msg = %s\n", ptr);
        } else {
            perror("pthread_join");
            return -1;
        }
    }

    return 0;
}
