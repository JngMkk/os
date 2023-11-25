from threading import Lock

from attr import attrib, attrs


@attrs  # 일반적인 상용구 코드(__init__(), ...)를 자동으로 포함시킬 수 있음
class Cutlery:
    knives = attrib(default=0)  # 속성 생성 및 기본값 지정을 쉽게 처리할 수 있음.
    forks = attrib(default=0)
    lock = attrib(default=Lock())

    def give(self, to: "Cutlery", knives: int = 0, forks: int = 0) -> None:
        with self.lock:
            self.change(-knives, -forks)
        with to.lock:
            to.change(knives, forks)

    def change(self, knives: int, forks: int) -> None:
        self.knives += knives
        self.forks += forks
