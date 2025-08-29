from collections.abc import Iterable
from typing import List

def assignment1(nums: Iterable[int]) -> List[int]:
    """
    [1,2,3] -> [1,8,27]
    규칙: 각 원소를 세제곱(cube)
    """
    return list(map(lambda x: x**3, nums))

def assignment2(words: Iterable[str]) -> List[int]:
    """
    ["a","bb"] -> [1,2]
    규칙: 각 문자열 길이를 계산
    """
    return list(map(lambda x: len(x), words))

def assignment3(nums: Iterable[float | int]) -> List[float]:
    """
    [10,20,30] -> [5.0,10.0,15.0]
    규칙: 각 원소를 절반으로
    """
    return list(map(lambda x: x/2, nums))
