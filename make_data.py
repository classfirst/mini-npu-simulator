
# 실습 5-3: JSON 데이터 자동 생성

import json
from pathlib import Path

DATA_FILE = Path(__file__).resolve().parent / "data.json"

SIZES = [5, 13, 25]


# 1. Cross 패턴 생성
def generate_cross(size):
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


# 2. X 패턴 생성
def generate_x(size):
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


# 3. 전체 JSON 데이터 생성
def create_data():
    data = {
        "filters": {},
        "patterns": {}
    }

    for size in SIZES:
        cross = generate_cross(size)
        x_pattern = generate_x(size)

        # 크기별 필터 저장
        data["filters"][f"size_{size}"] = {
            "cross": cross,
            "x": x_pattern
        }

        # 첫 번째 케이스: Cross
        data["patterns"][f"size_{size}_1"] = {
            "input": cross,
            "expected": "+"
        }

        # 두 번째 케이스: X
        data["patterns"][f"size_{size}_2"] = {
            "input": x_pattern,
            "expected": "x"
        }

    return data


# 4. JSON 파일 저장
def main():
    data = create_data()

    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(
            data,
            file,
            ensure_ascii=False,
            indent=2
        )

    print("=== JSON 데이터 생성 완료 ===")

    print("필터 크기:")
    for key in data["filters"]:
        print("-", key)

    print("패턴 목록:")
    for key in data["patterns"]:
        print("-", key)

    print("총 패턴:", len(data["patterns"]))
    print("저장 파일:", DATA_FILE)


if __name__ == "__main__":
    main()
