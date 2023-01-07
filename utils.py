def solveQuestion(operands, operation):
    if operation == "ADD":
        return operands["first"] + operands["second"]
    if operation == "SUB":
        return operands["first"] - operands["second"]
    if operation == "MUL":
        return operands["first"] * operands["second"]
    if operation == "DIV":
        return round(operands["first"] / operands["second"])