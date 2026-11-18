
# 실습 5-3: 크기별 MAC 성능 분석

import time

from check_batch import calculate_mac
from make_data import generate_cross

REPEAT_COUNT = 100


# 1. MAC 평균 실행 시간 측정
def measure_mac(pattern, filter_matrix, repeats):
    if repeats < 10:
        raise ValueError("최소 10회 이상 측정해야 합니다.")

    # 측정 전 예열
    for _ in range(10):
        calculate_mac(pattern, filter_matrix)

    total_time = 0.0

    for _ in range(repeats):
        start = time.perf_counter()

        calculate_mac(pattern, filter_matrix)

        end = time.perf_counter()

        elapsed_ms = (end - start) * 1000
        total_time += elapsed_ms

    return total_time / repeats


# 2. 크기별 성능 표 출력
def main():
    sizes = [3, 5, 13, 25]

    print("=== MAC 성능 분석 ===")
    print("반복 측정:", REPEAT_COUNT, "회")

    print(
        f"{'크기':<10}"
        f"{'평균 시간(ms)':<18}"
        f"{'MAC 횟수':<12}"
    )

    print("-" * 40)

    for size in sizes:
        pattern = generate_cross(size)

        average_ms = measure_mac(
            pattern,
            pattern,
            REPEAT_COUNT
        )

        operations = size * size

        print(
            f"{size}x{size:<7}"
            f"{average_ms:<18.6f}"
            f"{operations:<12}"
        )


if __name__ == "__main__":
    main()
