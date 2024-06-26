from celery import Celery
from kombu import Queue

redis_url = "redis://localhost:6379/0"
app = Celery("tasks", broker=redis_url, backend=redis_url)

# 큐(태스크 흐름)를 분리해 얻을 수 있는 장점은?
# 그룹화하여 쉽게 모니터링할 수 있음
# 작업자가 특정 큐 소비에 전념할 수 있기에 성능 개선 가능
# 우수한 성능을 갖춘 머신의 브로커에 무거운 태스크가 있는 큐를 배포할 수 있음.
app.conf.task_queues = (
    Queue("sqrt_queue", routing_key="sqrt"),
    Queue("fibo_queue", routing_key="fibo"),
)


"""
샐러리는 네트워크로 서로 연결되는 머신 사이 또는 로컬 작업자 사이에 메세지를 교환함으로써 작업 단위(태스크)를 분산하는 개념으로 작동.
태스크는 샐러리의 핵심 개념이며, 분산해야 하는 어떠한 작업을 태스크에 미리 캡슐화해야 함.


why use?
    - 네트워크에서 퍼진 작업자 사이나 로컬 작업자들에게 투명한 방법으로 태스크를 분산함.
    - 설정을 통해 작업자의 동시성을 간단한 방법으로 변경함. (프로세스, 스레드, Gevent, Eventlet)
    - 동기식, 비동기식, 주기식, 태스크 스케줄링을 지원함.
    - 오류가 났을 때 태스크를 다시 실행함.


비동기 태스크 vs 실시간 태스크
    
    실시간 태스크인 경우 이 태스크는 실행돼야 하는 제한된 시간 구간을 가짐.
    이런 경우가 발생하지 않는다면 태스크가 중단되거나 다음에 실행하기 위해 중지됨.
    반면, 비동기 태스크는 수행 즉시 결과를 반환함.


샐러리는 클라이언트 컴포넌트가 생성한 태스크를 선택된 브로커(메세지 전송)에 디스패치하는 기능이 있음.
태스크 호출을 수행하면 AsyncResult 타입의 객체를 반환함.
AsyncResult 객체는 태스크 상태가 끝났는지 아니면 분명히 존재하는지 점검한 후에 존재하면 반환하는 객체.
이 메커니즘을 사용하려면 result backend를 활성화해야 함.


태스크 디스패치 메서드
    - apply_async((args,), {"kwargs": value}): 태스크 실행을 위한 파라미터 설정을 허용함
        - cutdown: 태스크 실행을 시작하도록 미래에 사용할 수 있는 초 단위의 경과 시간을 나타냄.
        - expires: 특정 태스크가 더 이상 실행되지 않을 시간 또는 날짜 주기
        - retry: 태스크 연결이나 전송에 실패했을 경우 retry 횟수
        - queue: 참조되어야 하는 태스크가 있는 queue
        - serializer: 디스크에 태스크를 직렬화하는 데이터 포맷 (json, yaml 등)
        - link: 태스크를 성공적으로 실행했을 경우에 실행될 하나 이상의 태스크 링크
        - link_error: 태스크 실행 과정에서 실패할 경우 실행될 하나 이상의 태스크 링크
    
    - delay(args, kwargs=value): apply_async 메서드를 호출하는 간단한 방법

    - apply((args,), {"kwargs": value}): 로컬 프로세스에서 비동기식으로 태스크를 실행함. 따라서 결과를 준비할 때까지 봉쇄.


메세지 전송 브로커
    
    브로커를 통해 메세지를 주고 받으며, 작업자와 통신함.
    브로커는 태스크를 보내고 작업자가 태스크를 실행하는 클라이언트 애플리케이션 간의 통신 수단을 제공함 (태스크 큐를 이용해 수행).


workers

    작업자는 수신한 태스크를 실행하는 역할.
    샐러리는 작업자 동작을 제어하는 최적의 방법을 찾기 위한 일련의 메커니즘을 제공.

        - 동시성 모드: 작업자가 수행하는 모드로 프로세스, 스레드, 이벤트렛, 게벤트가 있음.
        - 원격 모드: 동작의 변경에 목적(작업자의 실행 시간 등)을 둔 최우선 순위 큐를 통해 특정 작업자나 작업자 목록에 직접 메세지를 전달할 수 있음.
        - 태스크 취소: 하나 이상의 작업자에게 하나 또는 여러 태스크 실행을 무시하라고 명령할 수 있음.


result backend

    result backend 컴포넌트는 태스크의 상태와 결과를 저장하고, 클라이언트 애플리케이션에 반환하는 역할을 함.
"""
