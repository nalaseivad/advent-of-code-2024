import sys
import re
from itertools import product


def evaluate_rpn_expression(expression):
    stack = []
    operators = { "+" : lambda x, y : x + y, "*" : lambda x, y : x * y, "||" : lambda x, y : int(f"{x}{y}") }
    tokens = expression.split()
    for token in tokens:
        if token in operators:
            b = stack.pop()
            a = stack.pop()
            result = operators[token](a, b)
            stack.append(result)
        else:
            stack.append(int(token))
    return stack[0]


def generate_rpn_expressions(operands, operators):
    operator_combinations = product(operators, repeat=len(operands) - 1)
    expressions = []
    for ops in operator_combinations:
        expression = str(operands[0]) + " " + " ".join(str(operands[i + 1]) + " " + ops[i] for i in range(len(ops)))
        expressions.append(expression)
    return expressions


def test_equations(equations, operators):
    answers = set()
    for equation in equations:
        answer, operands = equation
        expressions = generate_rpn_expressions(operands, operators)
        for expression in expressions:
            if answer == evaluate_rpn_expression(expression):
                answers.add(answer)
                break
    return sum(answers)


def part_1(equations):
    return test_equations(equations, ['+', '*'])


def part_2(equations):
    return test_equations(equations, ["+", "*", "||"])


def part_n(file_path, fn):
    equations = []
    with open(file_path, "r") as lines:
        for line in lines:
            answer, x = re.split(r':\s*', line.rstrip("\n"))
            operands = [int(n) for n in re.split(r'\s+', x)]
            equations.append([int(answer), operands])
    print(fn(equations))


if len(sys.argv) != 3:
    print(f"Usage: python3 {sys.argv[0]} <part> <file_path>")
    exit(1)

part = sys.argv[1]
file_path = sys.argv[2]

if part == "1":
    part_n(file_path, part_1)
elif part == "2":
    part_n(file_path, part_2)
else:
    print("Unknown part")
    exit(1)
