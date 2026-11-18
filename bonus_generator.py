
# Codyssey Pre-course Week 3
# Bonus 2: Cross / X Pattern Generator

from check_batch import calculate_mac
from benchmark import measure_mac

REPEAT_COUNT = 100


# 1. 입력 크기 검증
def validate_size(size):
    if type(size) is not int:
        raise ValueError("크기는 정수여야 합니다.")

    if size < 3:
        raise ValueError("크기는 3 이상이어야 합니다.")

    if size % 2 == 0:
        raise ValueError("홀수 크기만 사용할 수 있습니다.")


# 2. Cross 패턴 생성
def generate_cross(size):
    validate_size(size)

    matrix = []
    center = size // 2

    for i in range(size):
        row = []

        for j in range(size):
            if i == center or j == center:
                row.append(1)
            else:
                row.append(0)

        matrix.append(row)

    return matrix


# 3. X 패턴 생성
def generate_x(size):
    validate_size(size)

    matrix = []

    for i in range(size):
        row = []

        for j in range(size):
            if i == j or i + j == size - 1:
                row.append(1)
            else:
                row.append(0)

        matrix.append(row)

    return matrix


# 4. 패턴 출력
def print_matrix(matrix):
    for row in matrix:
        print(" ".join(str(value) for value in row))


# 5. MAC 점수 검증
def verify_patterns(size, cross, x_pattern):
    cross_score = calculate_mac(cross, cross)
    x_score = calculate_mac(x_pattern, x_pattern)
    overlap_score = calculate_mac(cross, x_pattern)

    expected_score = 2 * size - 1

    if cross_score != expected_score:
        raise AssertionError("Cross 점수 오류")

    if x_score != expected_score:
        raise AssertionError("X 점수 오류")

    if overlap_score != 1:
        raise AssertionError("Cross/X 겹침 점수 오류")

    print("\n[MAC 검증]")
    print("Cross 자기 점수:", cross_score)
    print("X 자기 점수:", x_score)
    print("Cross/X 겹침 점수:", overlap_score)
    print("검증 결과: PASS")


# 6. 성능 분석
def show_performance(size, cross):
    average_ms = measure_mac(
        cross,
        cross,
        REPEAT_COUNT
    )

    print("\n[성능 분석]")
    print("크기:", f"{size}x{size}")
    print("평균 시간(ms):", f"{average_ms:.6f}")
    print("MAC 횟수:", size * size)
    print("반복 측정:", REPEAT_COUNT)


# 7. 사용자 입력
def input_size():
    while True:
        text = input(
            "\n생성할 크기 N 입력 "
            "(3 이상의 홀수, 종료 q): "
        ).strip()

        if text.lower() == "q":
            return None

        try:
            size = int(text)
            validate_size(size)

            return size

        except ValueError as error:
            print("입력 오류:", error)
            print("예: 3, 5, 7, 13, 25")


# 8. 메인 프로그램
def main():
    print("=== Cross / X Pattern Generator ===")

    while True:
        size = input_size()

        if size is None:
            print("패턴 생성기를 종료합니다.")
            break

        cross = generate_cross(size)
        x_pattern = generate_x(size)

        print(f"\n[{size}x{size} Cross]")
        print_matrix(cross)

        print(f"\n[{size}x{size} X]")
        print_matrix(x_pattern)

        verify_patterns(size, cross, x_pattern)
        show_performance(size, cross)

        print("\n패턴 생성 완료!")


if __name__ == "__main__":
    try:
        main()
    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 종료합니다.")
