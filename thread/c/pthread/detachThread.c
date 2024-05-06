#include <pthread.h>
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

/*
    pthread_join 함수로 종료 처리를 수행하지 않으면 메모리 누출이 되므로 반드시 join을 해야 함.
    한편 스레드 종료 시 자동으로 스레드용 리소스를 해제하는 방법도 있으며, 그런 스레드를 detach thread라 부름.

    방법
        1. pthread_create 함수 호출 시 어트리뷰트로 지정하는 방법
        2. pthread_detach 함수를 호출하는 법
*/

void* thread_func(void *arg) {
    for (int i = 0; i < 5; i++) {
        printf("i = %d\n", i);
        sleep(1);
    }

    return NULL;
}

int main(int argc, char *argv[]) {
    // 어트리뷰트 초기화
    pthread_attr_t attr;
    if (pthread_attr_init(&attr) != 0) {
        perror("pthread_attr_init");
        return -1;
    }

    // detach thread로 설정. 이외에도 스레드 스택 크기나 CPU affinity (스레드를 어떤 CPU에서 작동시킬 것인지에 관한 정보) 등도 설정할 수 있음.
    if (pthread_attr_setdetachstate(&attr, PTHREAD_CREATE_DETACHED) != 0) {
        perror("pthread_attr_setdetachstate");
        return -1;
    }

    pthread_t thread;
    if (pthread_create(&thread, &attr, thread_func, NULL) != 0) {
        perror("pthread_create");
        return -1;
    }

    if (pthread_attr_destroy(&attr) != 0) {
        perror("pthread_attr_destroy");
        return -1;
    }

    sleep(10);
    return 0;
}

/*
    스레드를 생성한 뒤 디태치 스레드로 만드는 예

    void* thread_func(void *arg) {
        pthread_detach(pthread_self());
        ...
        return NULL;
    }
*/
