
# Codyssey Pre-course Week 3
# Mini NPU Simulator - Final Integration

import json
import math
from pathlib import Path

from check_batch import (
    analyze_case,
    calculate_mac,
    classify_pattern,
)
from benchmark import measure_mac
from make_data import generate_cross

import bonus_flatten
import bonus_generator


DATA_FILE = Path(__file__).resolve().parent / "data.json"
REPEAT_COUNT = 100


# 1. 3x3 사용자 입력
def input_matrix(name):
    print(f"\n{name} (3줄 입력, 공백 구분)")

    matrix = []

    while len(matrix) < 3:
        row_number = len(matrix) + 1
        text = input(f"{row_number}행 입력: ")
        values = text.split()

        if len(values) != 3:
            print(
                "입력 형식 오류: 각 줄에 숫자 3개를 "
                "공백으로 구분해 입력하세요."
            )
            continue

        try:
            row = []

            for value in values:
                number = float(value)

                if not math.isfinite(number):
                    raise ValueError("유한하지 않은 숫자")

                row.append(number)

            matrix.append(row)

        except ValueError:
            print("입력 오류: 유효한 숫자만 입력하세요.")

    return matrix


# 2. MAC 성능 분석 표
def print_performance(sizes):
    print("\n=== MAC 성능 분석 ===")
    print(f"반복 측정: {REPEAT_COUNT}회")

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

        print(
            f"{size}x{size:<7}"
            f"{average_ms:<18.6f}"
            f"{size * size:<12}"
        )


# 3. 모드 1: 직접 입력
def run_manual_mode():
    print("\n=== 모드 1: 사용자 입력 ===")

    print("\n[1] 필터 입력")
    filter_a = input_matrix("필터 A")
    filter_b = input_matrix("필터 B")

    print("\n필터 저장 완료")
    print("필터 A:", filter_a)
    print("필터 B:", filter_b)

    print("\n[2] 패턴 입력")
    pattern = input_matrix("입력 패턴")

    print("\n[3] MAC 연산 및 판정")
    score_a = calculate_mac(pattern, filter_a)
    score_b = calculate_mac(pattern, filter_b)

    if not math.isfinite(score_a) or not math.isfinite(score_b):
        print("오류: MAC 점수가 유한하지 않습니다.")
        return

    prediction = classify_pattern(score_a, score_b)

    if prediction == "Cross":
        result = "A"
    elif prediction == "X":
        result = "B"
    else:
        result = "UNDECIDED"

    print("A 점수:", score_a)
    print("B 점수:", score_b)
    print("판정:", result)

    print_performance([3])


# 4. 모드 2: JSON 분석
def run_json_mode():
    print("\n=== 모드 2: JSON 분석 ===")

    print("\n[1] JSON 파일 로드")

    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        print("JSON 읽기 오류:", error)
        return

    if not isinstance(data, dict):
        print("JSON 구조 오류: 최상위 객체가 아닙니다.")
        return

    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict):
        print("JSON 구조 오류: filters가 객체가 아닙니다.")
        return

    if not isinstance(patterns, dict):
        print("JSON 구조 오류: patterns가 객체가 아닙니다.")
        return

    print("필터 로드 완료")
    print("필터 크기:", list(filters.keys()))
    print("패턴 로드 완료")
    print("패턴 수:", len(patterns))

    print("\n[2] 케이스별 MAC 분석")

    passed = 0
    failures = []

    for case_id, case_data in patterns.items():
        print(f"\n--- {case_id} ---")

        try:
            (
                cross_score,
                x_score,
                prediction,
                expected
            ) = analyze_case(
                case_id,
                case_data,
                filters
            )

            print("Cross 점수:", cross_score)
            print("X 점수:", x_score)
            print("판정:", prediction)
            print("예상 정답:", expected)

            if prediction == expected:
                print("결과: PASS")
                passed += 1

            else:
                reason = (
                    f"판정 불일치: "
                    f"{prediction} != {expected}"
                )
                print("결과: FAIL -", reason)
                failures.append((case_id, reason))

        except (
            ValueError,
            TypeError,
            KeyError,
            OverflowError
        ) as error:
            reason = str(error)
            print("결과: FAIL -", reason)
            failures.append((case_id, reason))

    # 5. 성능 분석을 먼저 출력
    print("\n[3] 크기별 성능 분석")
    print_performance([3, 5, 13, 25])

    # 6. 결과 요약은 마지막에 출력
    total = len(patterns)
    failed = len(failures)

    print("\n[4] 최종 결과 요약")
    print("전체 테스트:", total)
    print("통과:", passed)
    print("실패:", failed)

    if failures:
        print("\n실패 케이스 목록:")

        for case_id, reason in failures:
            print(f"- {case_id}: {reason}")

    else:
        print("실패 케이스 없음")

    assert total == passed + failed


# 7. 메인 메뉴
def main():
    print("=== Mini NPU Simulator ===")

    while True:
        print("\n[모드 선택]")
        print("1. 사용자 입력 (3x3)")
        print("2. data.json 분석")
        print("3. 보너스 1: 2D / 1D MAC 비교")
        print("4. 보너스 2: Cross / X 패턴 생성")
        print("0. 종료")

        choice = input("선택: ").strip()

        if choice == "1":
            run_manual_mode()

        elif choice == "2":
            run_json_mode()

        elif choice == "3":
            bonus_flatten.main()

        elif choice == "4":
            bonus_generator.main()

        elif choice == "0":
            print("프로그램을 종료합니다.")
            break

        else:
            print("잘못된 선택입니다. 다시 입력하세요.")


if __name__ == "__main__":
    try:
        main()

    except (KeyboardInterrupt, EOFError):
        print("\n입력이 중단되어 종료합니다.")
