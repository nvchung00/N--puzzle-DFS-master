import sys, math
from solver import Solver


def print_mat(mat):
    res = ""
    for row in mat:
        for x in row:
            if x == 0:
                res += "_".rjust(4)
            else:
                res += str(x).rjust(4)
        res += "\n"
    print(res)


def inp_list(promt):
    input_list = input(promt)
    input_list = list(map(int, input_list.split(",")))

    n2 = len(input_list)
    n = math.isqrt(len(input_list))

    if n**2 != n2:
        print("Length must be a square.")
        sys.exit()

    if set(input_list) != set(range(n2)):
        print("Input list must contain all numbers from 0 to n^2 - 1.")
        sys.exit()

    return input_list


def main():
    """"Main driver function"""

    init_list = inp_list("Init list (comma seperated): ")
    goal_list = inp_list("Goal list (comma seperated): ")

    solver = Solver(init_list, goal_list)

    print("[+] Initial state:\n")
    print_mat(solver.initial_state)
    print("[+] Goal state:\n")
    print_mat(solver.goal_state)

    solution_metrics = solver.dfs()

    print("[+] Path to goal:\n")
    for mat in solution_metrics.path_to_goal:
        print_mat(mat)
        print("-" * 30)

    print("[+] Path length:", len(solution_metrics.path_to_goal))
    print("[+] Search time (ms):", solution_metrics.search_time)


if __name__ == "__main__":
    main()
