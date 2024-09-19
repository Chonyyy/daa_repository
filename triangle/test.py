import sys
from pydantic import BaseModel, conlist
from typing import List, Tuple
from utils import generate_random_list, generate_all_melodies
import random

FIXED_CASES = [
        [1, 2, 3, 7, 14, 21, 4, 1, 8, 9]
]

FIXED_CASES_SOLUTIONS = [
    
]

# Define the structure of the input list using Pydantic
class InputCase(BaseModel):
    values: List[int]
    
def brute_force_solution(all_melodies: List[Tuple]) -> List:
    from itertools import combinations
    
    max = 0
    solution = []
    
    for (melody_1, notes_1), (melody_2, notes_2), (melody_3, notes_3), (melody_4, notes_4) in combinations(all_melodies, 4):
        #TODO: handle them having the same indexes
        different_notes = len(notes_1 | notes_2 | notes_3 | notes_4)
        if different_notes > max:
            max = different_notes
            solution = [melody_1, melody_2, melody_3, melody_4]
    return solution
    
def solve_input_case(input_case: InputCase) -> int:
    return sum(input_case.values)

def solve_random_cases(amount: int = 1, list_size: int = -1, max_value: int = 10, min_value: int = -10) -> List[List[int]]:
    return [[random.randint(min_value, max_value) for _ in range(list_size)] for _ in range(amount)]

def solve_fixed_cases() -> List[List[int]]:
    for case in FIXED_CASES:
        print(f'Case: {case}')
        melodies = generate_all_melodies(case)
        solution = brute_force_solution(melodies)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py --input <input_case> | --random <amount> <list_size> <max_value> <min_value> | --fixed")
        sys.exit(1)

    if sys.argv[1] == '--input':
        # Handle input case
        input_case = InputCase(values=list(map(int, sys.argv[2:])))
        result = solve_input_case(input_case)
        print("Result from input case:", result)

    elif sys.argv[1] == '--random':
        # Handle random cases
        if len(sys.argv) != 6:
            print("Usage: script.py --random <amount> <list_size> <max_value> <min_value>")
            sys.exit(1)
        amount = int(sys.argv[2])
        list_size = int(sys.argv[3])
        max_value = int(sys.argv[4])
        min_value = int(sys.argv[5])
        random_cases = solve_random_cases(amount, list_size, max_value, min_value)
        for case in random_cases:
            result = solve_input_case(InputCase(values=case))
            print(f"Result from random case {case}: {result}")

    elif sys.argv[1] == '--fixed':
        # Handle fixed cases
        fixed_cases = solve_fixed_cases()
        for case in fixed_cases:
            result = solve_input_case(InputCase(values=case))
            print(f"Result from fixed case {case}: {result}")

    else:
        print("Unknown option. Use --input, --random, or --fixed.")
        sys.exit(1)