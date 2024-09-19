from typing import List, Tuple
from random import randint

def generate_random_list(n: int, min_value: int = -1000000, max_value: int = 1000000) -> List[int]:
    return [randint(min_value, max_value) for _ in range(n)]

def generate_all_melodies(nums: List[int]) -> List[List[int]]:
    from itertools import combinations

    results = []
    n = len(nums)
    
    # Generate combinations of all possible lengths
    for r in range(1, n + 1):
        for combo in combinations(nums, r):
            if valid_melody(list(combo)):
                results.append((list(combo), set(combo)))
    
    return results

def valid_melody(melody: List[int]) -> bool:
    if len(melody) == 1: return True
    for index in range(len(melody) - 1):
        if (melody[index] % 7 != melody[index+1] % 7) and abs(melody[index] - melody[index+1]) != 1:
            return False
    return True