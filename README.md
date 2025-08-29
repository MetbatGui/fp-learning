# 파이썬 함수형 학습 (Functional Programming in Python)

이 저장소는 **파이썬으로 함수형 프로그래밍 개념을 학습**하기 위한 실험실(lab)입니다.  
`uv`로 초기화된 패키지 구조를 기반으로, 이론 정리(Jupyter Notebook)와 실습 코드(.py 모듈, pytest)를 함께 다룹니다.

---

## 📂 디렉터리 구조
```

fp-learning/
src/fp/               # 함수형 유틸 모듈 (map/flatmap, Maybe, Either 등)
tests/                # pytest 기반 테스트
notebooks/            # 개념·실험 노트북(.ipynb)
pyproject.toml        # uv/ruff/mypy/pytest 설정
README.md             # 프로젝트 설명
justfile              # 자주 쓰는 명령 모음

````

---

## 🚀 시작하기

### 1) 환경 준비
```bash
# Python 3.13 환경에서 uv 초기화
uv init --lib --package -p 3.13

# 의존성 설치
uv sync
````

### 2) 개발용 의존성 추가

```bash
uv add --dev pytest ruff mypy jupyter
```

### 3) 노트북 실행

```bash
uv run jupyter lab
```

---

## 🧪 테스트

```bash
uv run pytest
```

---

## 📘 학습 방법

* **notebooks/** : 개념 실험 및 정리
  (예: `01_map_flatmap.ipynb`, `02_maybe_either.ipynb`)
* **src/fp/** : 재사용 가능한 순수 함수와 타입 정의
* **tests/** : pytest로 함수형 법칙(결합, 항등 등) 검증

---

## 🎯 목표

* 함수형 기본 개념: map, flatmap, filter, reduce, lambda
* 자료구조: Option/Maybe, Either, Monoid, Functor, Monad
* 순수성, 불변성, 합성 중심 코드 스타일
* 실습과 이론을 연결해 **Pythonic Functional Programming** 감각 익히기

```

---