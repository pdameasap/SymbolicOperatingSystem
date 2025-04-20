# test_secl.py
# Basic runtime validation for SECLInterpreter and symbolic math resolver

from cortex.interpreter import SECLInterpreter

if __name__ == "__main__":
    interpreter = SECLInterpreter()

    test_cases = [
        "%∑(Z1, Z3, 😭)",
        "%∂(Z5 ∘ 😭)",
        "%↻(Z13, Z12)",
        "%emoji|😭"
    ]

    for case in test_cases:
        print(f"Input: {case}")
        result = interpreter.interpret(case)
        print("Output:", result)
        print("-" * 40)
