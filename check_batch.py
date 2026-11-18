
# Codyssey Pre-course Week 3
# 실습 5-2C: JSON 일괄 MAC 분석

import json
import math
import re
from pathlib import Path

EPSILON = 1e-9
DATA_FILE = Path(__file__).resolve().parent / "data.json"


# 1. 라벨 정규화
def normalize_label(label):
    if not isinstance(label, str):
        raise ValueError("라벨은 문자열이어야 합니다.")

    cleaned = label.strip().lower()

    if cleaned in ("+", "cross"):
        return "Cross"
    if cleaned == "x":
        return "X"

    raise ValueError(f"지원하지 않는 라벨: {label}")


# 2. 패턴 키에서 크기 추출
def parse_pattern_key(key):
    if not isinstance(key, str):
        raise ValueError("패턴 키가 문자열이 아닙니다.")

    match = re.fullmatch(r"size_([1-9][0-9]*)_([1-9][0-9]*)", key)

    if match is None:
        raise ValueError(f"패턴 키 형식 오류: {key}")

    size = int(match.group(1))
    index = int(match.group(2))

    return size, index


# 3. N x N 배열 검증
def validate_matrix(matrix, size, name):
    if not isinstance(matrix, list) or len(matrix) != size:
        raise ValueError(f"{name}: 행 개수 또는 자료형 오류")

    for i, row in enumerate(matrix):
        if not isinstance(row, list) or len(row) != size:
            raise ValueError(f"{name}: {i+1}행 열 개수 오류")

        for j, value in enumerate(row):
            if type(value) not in (int, float):
                raise ValueError(
                    f"{name}: [{i}][{j}] 숫자 자료형 오류"
                )

            try:
                finite = math.isfinite(value)
            except OverflowError:
                finite = False

            if not finite:
                raise ValueError(
                    f"{name}: [{i}][{j}] 유한하지 않은 숫자"
                )


# 4. MAC 연산
def calculate_mac(pattern, filter_matrix):
    total = 0.0

    for i in range(len(pattern)):
        for j in range(len(pattern[i])):
            total += pattern[i][j] * filter_matrix[i][j]

    return total


# 5. Cross / X 판정
def classify_pattern(cross_score, x_score):
    if not math.isfinite(cross_score) or not math.isfinite(x_score):
        raise ValueError("MAC 점수가 유한하지 않습니다.")

    if abs(cross_score - x_score) < EPSILON:
        return "UNDECIDED"

    if cross_score > x_score:
        return "Cross"

    return "X"


# 6. 크기에 맞는 필터 찾기
def get_filters(filters, size):
    filter_key = f"size_{size}"

    if filter_key not in filters:
        raise ValueError(f"필터 없음: {filter_key}")

    raw_filters = filters[filter_key]

    if not isinstance(raw_filters, dict):
        raise ValueError("필터 데이터가 객체가 아닙니다.")

    normalized = {}

    for label, matrix in raw_filters.items():
        standard = normalize_label(label)

        if standard in normalized:
            raise ValueError(f"중복 필터 라벨: {standard}")

        validate_matrix(matrix, size, standard + " 필터")
        normalized[standard] = matrix

    if set(normalized) != {"Cross", "X"}:
        raise ValueError("Cross 또는 X 필터 누락")

    return normalized


# 7. 케이스 하나 분석
def analyze_case(case_id, case_data, filters):
    size, index = parse_pattern_key(case_id)

    if not isinstance(case_data, dict):
        raise ValueError("케이스 데이터가 객체가 아닙니다.")

    if "input" not in case_data or "expected" not in case_data:
        raise ValueError("input 또는 expected 누락")

    pattern = case_data["input"]
    expected = normalize_label(case_data["expected"])

    validate_matrix(pattern, size, "입력 패턴")

    selected_filters = get_filters(filters, size)

    cross_score = calculate_mac(
        pattern, selected_filters["Cross"]
    )
    x_score = calculate_mac(
        pattern, selected_filters["X"]
    )

    prediction = classify_pattern(cross_score, x_score)

    return cross_score, x_score, prediction, expected


# 8. 전체 케이스 분석 및 집계
def analyze_all(data):
    if not isinstance(data, dict):
        raise ValueError("JSON 최상위 구조 오류")

    filters = data.get("filters")
    patterns = data.get("patterns")

    if not isinstance(filters, dict):
        raise ValueError("filters는 객체여야 합니다.")

    if not isinstance(patterns, dict):
        raise ValueError("patterns는 객체여야 합니다.")

    passed = 0
    failures = []

    print("\n=== JSON 일괄 MAC 분석 ===")

    for case_id, case_data in patterns.items():
        print(f"\n--- {case_id} ---")

        try:
            cross_score, x_score, prediction, expected = (
                analyze_case(case_id, case_data, filters)
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
                    f"판정 불일치: {prediction} != {expected}"
                )
                print("결과: FAIL -", reason)
                failures.append((case_id, reason))

        except (ValueError, KeyError, TypeError, OverflowError) as error:
            reason = str(error)
            print("결과: FAIL -", reason)
            failures.append((case_id, reason))

    total = len(patterns)
    failed = len(failures)

    print("\n=== 결과 요약 ===")
    print("총 테스트:", total)
    print("통과:", passed)
    print("실패:", failed)

    if failures:
        print("\n실패 케이스:")
        for case_id, reason in failures:
            print(f"- {case_id}: {reason}")
    else:
        print("실패 케이스 없음")

    assert total == passed + failed


# 9. 프로그램 시작
def main():
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)

    except FileNotFoundError:
        print("오류: data.json 파일이 없습니다.")
        return

    except (json.JSONDecodeError, UnicodeError, OSError) as error:
        print("JSON 파일 읽기 오류:", error)
        return

    try:
        analyze_all(data)
    except (ValueError, TypeError) as error:
        print("전체 JSON 구조 오류:", error)


# 10. 실패 케이스 격리 테스트
def test_failure_isolation():
    with open(DATA_FILE, "r", encoding="utf-8") as file:
        data = json.load(file)

    # 원본 파일은 변경하지 않고 메모리에만 추가
    data["patterns"]["size_5_2"] = {
        "input": [
            [0, 0, 1, 0],
            [0, 0, 1, 0, 0],
            [1, 1, 1, 1, 1],
            [0, 0, 1, 0, 0],
            [0, 0, 1, 0, 0]
        ],
        "expected": "+"
    }

    data["patterns"]["size_5_3"] = {
        "input": data["filters"]["size_5"]["x"],
        "expected": "x"
    }

    print("\n=== 실패 격리 테스트 ===")
    analyze_all(data)

if __name__ == "__main__":
    main()
