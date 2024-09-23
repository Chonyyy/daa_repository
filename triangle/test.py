import sys
from pydantic import BaseModel
from typing import List, Tuple
from utils import generate_random_list, generate_all_melodies, min_cost_flow, count_notes

FIXED_CASES = [
    [1, 2, 3, 7, 14, 21, 4, 1, 8, 9]
]

# Define the structure of the input list using Pydantic
class InputCase(BaseModel):
    values: List[int]
    
def brute_force_solution(all_melodies: List[Tuple[List[int], set[int]]]) -> List[List[int]]:
    from itertools import combinations
    
    max_notes = 0
    solution = []
    
    for (melody_1, indexes_1), (melody_2, indexes_2), (melody_3, indexes_3), (melody_4, indexes_4) in combinations(all_melodies, 4):
        if indexes_1 & indexes_2 or indexes_1 & indexes_3 or indexes_1 & indexes_4 or indexes_2 & indexes_3 or indexes_2 & indexes_4 or indexes_3 & indexes_4:
            continue
        
        different_notes = len(indexes_1 | indexes_2 | indexes_3 | indexes_4)
        if different_notes > max_notes:
            max_notes = different_notes
            solution = [melody_1, melody_2, melody_3, melody_4]
    
    return solution

def solve_input_case(input_case: InputCase) -> List[List[int]]:
    melodies = generate_all_melodies(input_case.values)
    
    # Use brute-force solution
    brute_force_result = brute_force_solution(melodies)
    
    # Use the flow-based solution
    _, flow_result = min_cost_flow(input_case.values)
    return flow_result

def solve_random_cases(amount: int = 1, list_size: int = -1, max_value: int = 10, min_value: int = -10) -> None:
    for _ in range(amount):
        random_case = generate_random_list(list_size, min_value, max_value)
        print(f'Random case: {random_case}')
        solution = solve_input_case(InputCase(values=random_case))
        print(f'Solution: {solution}')

def solve_fixed_cases() -> None:
    for case in FIXED_CASES:
        print(f'Fixed case: {case}')
        solution = solve_input_case(InputCase(values=case))
        print(f'Solution: {solution}')

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: script.py --input <input_case> | --random <amount> <list_size> <max_value> <min_value>")
        sys.exit(1)

    if sys.argv[1] == '--input':
        input_case = InputCase(values=[int(x) for x in sys.argv[2:]])
        print(solve_input_case(input_case))
    
    elif sys.argv[1] == '--random':
        amount = int(sys.argv[2])
        list_size = int(sys.argv[3])
        max_value = int(sys.argv[4])
        min_value = int(sys.argv[5])
        solve_random_cases(amount, list_size, max_value, min_value)
    
    else:
        solve_fixed_cases()
