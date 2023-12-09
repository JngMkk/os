import sys

# 객체 생성
a = []

# 참조 카운트 확인
# sys.getrefcount()는 해당 객체를 인자로 받는 동안 임시 참조를 생성하므로 실제 참조 카운트보다 1이 높게 나타남.
print("Ref count of a:", sys.getrefcount(a))  # Ref count of a: 2

# 다른 변수에 할당하여 참조 카운트 증가 확인
b = a
print("Ref count of a:", sys.getrefcount(a))  # Ref count of a: 3

# 참조 제거 후 참조 카운트 확인
del b
print("Ref count of a:", sys.getrefcount(a))  # Ref count of a: 2
