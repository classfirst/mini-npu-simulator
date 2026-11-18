
# Codyssey Pre-course Week 3
# Bonus 1: 2D vs 1D MAC Performance

import time

from make_data import generate_cross, generate_x

REPEAT_COUNT = 1000
SIZES = [3, 5, 13, 25]


# 1. 2차원 배열을 1차원으로 변환
def flatten_matrix(matrix):
    flat = []

    for row in matrix:
        for value in row:
            flat.append(value)

    return flat


# 2. 기존 방식: 2차원 MAC
def mac_2d(pattern, filter_matrix):
    total = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            total += pattern[i][j] * filter_matrix[i][j]

    return total


# 3. 새로운 방식: 1차원 MAC
def mac_1d(flat_pattern, flat_filter):
    if len(flat_pattern) != len(flat_filter):
        raise ValueError("1차원 배열 길이가 다릅니다.")

    total = 0.0

    for i in range(len(flat_pattern)):
        total += flat_pattern[i] * flat_filter[i]

    return total


# 4. 동일한 함수를 여러 번 측정
def measure_average(function, arg1, arg2, repeats):
    if repeats < 10:
        raise ValueError("최소 10회 이상 반복해야 합니다.")

    # 예열: 측정에 포함하지 않음
    for _ in range(20):
        function(arg1, arg2)

    start = time.perf_counter()

    for _ in range(repeats):
        function(arg1, arg2)

    end = time.perf_counter()

    # 전체 실행 시간 / 반복 횟수
    average_ms = (end - start) * 1000 / repeats

    return average_ms


# 5. 크기별 비교
def compare_size(size):
    cross = generate_cross(size)
    x_pattern = generate_x(size)

    flat_cross = flatten_matrix(cross)
    flat_x = flatten_matrix(x_pattern)

    # 2차원과 1차원 계산 결과 비교
    score_2d = mac_2d(cross, x_pattern)
    score_1d = mac_1d(flat_cross, flat_x)

    if score_2d != score_1d:
        raise AssertionError(
            f"{size}x{size}: MAC 계산 결과가 다릅니다."
        )

    # Cross와 Cross를 비교하는 경우도 검증
    same_2d = mac_2d(cross, cross)
    same_1d = mac_1d(flat_cross, flat_cross)

    if same_2d != same_1d:
        raise AssertionError(
            f"{size}x{size}: 동일 패턴 점수가 다릅니다."
        )

    # 동일한 입력 데이터로 연산 시간 비교
    time_2d = measure_average(
        mac_2d, cross, x_pattern, REPEAT_COUNT
    )

    time_1d = measure_average(
        mac_1d, flat_cross, flat_x, REPEAT_COUNT
    )

    # Flatten 변환 시간은 별도 측정
    start = time.perf_counter()

    for _ in range(REPEAT_COUNT):
        flatten_matrix(cross)
        flatten_matrix(x_pattern)

    end = time.perf_counter()

    conversion_ms = (
        (end - start) * 1000 / REPEAT_COUNT
    )

    return (
        score_2d,
        score_1d,
        time_2d,
        time_1d,
        conversion_ms
    )


# 6. 전체 결과 출력
def main():
    print("=== Bonus 1: 2D vs 1D MAC ===")
    print("반복 횟수:", REPEAT_COUNT)

    for size in SIZES:
        (
            score_2d,
            score_1d,
            time_2d,
            time_1d,
            conversion_ms
        ) = compare_size(size)

        print(f"\n[{size}x{size}]")
        print("2D MAC 점수:", score_2d)
        print("1D MAC 점수:", score_1d)
        print("점수 일치: PASS")

        print(f"2D 평균 시간: {time_2d:.6f} ms")
        print(f"1D 평균 시간: {time_1d:.6f} ms")
        print(f"Flatten 변환 시간: {conversion_ms:.6f} ms")

        if time_1d < time_2d:
            print("MAC 연산만 비교: 1D가 빠름")
        elif time_2d < time_1d:
            print("MAC 연산만 비교: 2D가 빠름")
        else:
            print("MAC 연산만 비교: 측정값 동일")

    print("\n전체 크기 검증 완료!")


if __name__ == "__main__":
    main()
