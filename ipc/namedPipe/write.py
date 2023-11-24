import os


def write_message(input_pipe: str, message: str) -> None:
    # FIFO 파일에 데이터 쓰기와 읽기 관리를 허용하는 파일 디스크립터 반환
    fd = os.open(input_pipe, os.O_WRONLY)
    os.write(fd, f"{message} from PID {os.getpid()}".encode())
    os.close(fd)


if __name__ == "__main__":
    named_pipe = "my_pipe"

    if not os.path.exists(named_pipe):
        # 네임드 파이프를 통해 쓰고 읽기 위한 FIFO 메커니즘을 구현한 특수 파일 생성
        os.mkfifo(named_pipe)

    write_message(named_pipe, "Hello")


"""
프로세스 간 통신(Inter-Process Communication, IPC)은 프로세스 사이에 정보를 교환할 수 있는 메커니즘.

IPC를 구현하는 여러 가지 방법이 있으며 일반적으로 선택한 실행 환경의 아키텍처에 의존함.
프로세스가 동일한 머신에서 실행하는 곳일 경우, 공유 메모리, 메시지 큐, 파이프와 같은 여러 통신 종류를 사용할 수 있음.
클러스터에서 프로세스가 물리적으로 분산된 경우, 소켓과 원격 프로시저 호출(Remote Procedure Call, RPC)을 사용할 수 있음.

네임드 파이프는 구현하는 특정 파일과 관련된 파일 디스크립터 사용을 통한 IPC 통신은 허용함.
예로, 데이터를 쓰고 읽기 위한 FIFO 구조를 들 수 있음.
네임드 파이프는 정보를 관리할 수 있는 방법으로 일반 파이프와 구분함.
네임드 파이프는 파일 디스크립터와 파일 시스템의 특수한 파일을 사용하는 반면에 일반 파이프는 메모리에 생성됨.
"""
