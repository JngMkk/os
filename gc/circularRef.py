import gc
import sys

gc.disable()  # Disable automatic gc


class Class:
    def __init__(self, name):
        self.ref = None
        self.name = name

    def __del__(self):
        print(f"Deleting {self.name}.")


a = Class("A")
b = Class("B")

a.ref = b
b.ref = a

print("Ref count of a:", sys.getrefcount(a))  # Ref count of a: 3
print("Ref count of b:", sys.getrefcount(b))  # Ref count of b: 3

del a
del b

print(gc.get_count())  # (83, 10, 0)
"""
gc.get_count(): 각 세대별 가비지 컬렉션 대기열의 크기(순서대로 0세대, 1세대, 2세대)
최근 생성된 객체는 0세대, 오래된 객체일수록 2세대이며 0세대일수록 더 자주 gc 수행

각 대기열에 어떤 객체가 존재하는지는 gc.get_objects()로 확인 가능
"""

print(gc.get_threshold())  # (700, 10, 10)
"""
gc.get_threshold(): gc 수행 임계값 확인
객체 생성 또는 해제가 700(0세대), 7000(1세대), 70000(2세대) 횟수를 초과하면 gc가 수행됨.

이 임계값들은 Python이 메모리를 효율적으로 관리할 수 있도록 도와줌.
gc를 너무 자주 실행하면 성능에 부정적인 영향을 미칠 수 있으며, 너무 드물게 실행하면 메모리 사용이 비효율적일 수 있음.

gc.set_threshold()를 통해 임계값 세팅 가능 (비권장)
"""

print(gc.collect())  # 4
"""
gc.collect(): 가비지 컬렉터가 실행되어 순환 참조에 있는 객체들을 회수(메모리 해제)
즉, 위 결과값 4는 가비지 컬렉터가 회수한 객체의 수를 의미.
"""

print(gc.garbage)  # []
"""
gc.garbage: 회수할 수 없는(메모리 해제를 할 수 없는) 객체 리스트
즉, 위 결과값 빈 list는 가비지 컬렉터가 순환 참조에 있는 객체들을 안전하게 회수하고, 해제할 수 없는 객체가 없다는 것을 의미. 
"""

gc.enable()  # Enable automatic gc

"""
1. gc.disable()을 했음에도 gc.collect()을 통해 가비지 컬렉션이 가능하다는 것을 알 수 있음.
2. Python gc는 참조 횟수가 0에 도달할 수는 없지만 순환 참조를 탐지하고 메모리 해제를 할 수 있다는 것을 알 수 있음.
3. 이를 통해, Python gc는 주로 참조 횟수 기반 gc 메커니즘을 사용하지만,
   트레이싱 기반 gc 메커니즘을 통해 순환 참조를 탐지하고 해결함을 알 수 있음.
4. But, __del__() 메서드가 복잡한 상호 작용을 하는 경우 순환 참조를 탐지하지 못하고 메모리 누수가 발생할 우려 있음.
   so, Python에서 메모리 누수에 대한 고려를 완전히 배제할 수는 없음.

? 순환 참조 알고리즘
    1. 도달 가능성 분석
        - 루트 객체(글로변 변수, 콜 스택 등 gc에 의해 접근 가능한 객체) 집합으로부터 시작하여 모든 객체를 추적함.
    2. 객체 그래프 탐색
        - 모든 객체는 그래프의 노드로 간주되며, 객체 간의 참조는 그래프의 엣지로 표현됨.
        - 이 그래프를 순회하면서 각 객체의 도달 가능성 체크.
    3. 도달할 수 없는 객체 탐지
        - 루트 객체로부터 도달할 수 없는 객체들은 순환 참조를 포함하고 있을 가능성이 높음.
        - 이러한 객체들은 서로 참조하고 있지만, 외부에서 더 이상 접근할 수 없는 상태이므로 메모리에서 해제될 수 있음.
    4. 순환 참조 그룹의 회수
        - 탐지된 순환 참조를 포함하는 객체 그룹은 메모리에서 해제됨.
        - 이 과정에서 __del__() 메서드가 정의된 객체가 있으면, 해당 메서드가 호출됨.

    순환 참조 탐지 알고리즘은 일정한 오버헤드를 수반하며, 큰 객체 그래프를 다루는 경우 성능에 영향을 끼칠 수 있음.
"""
