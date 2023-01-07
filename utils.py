from random import random

def createQuestionAndGetAnswer(operationOptions):
    selectedOperation = operationOptions[
        round(3*random())
    ]
    print("selectedOperation is ", selectedOperation)
    firstOperand = round(10*random())
    secondOperand = round(10*random())
    solution = solveQuestion({
        "first": firstOperand,
        "second": secondOperand
    }, selectedOperation)
    return {
        "solution": solution,
        "firstOperand": firstOperand,
        "secondOperand": secondOperand,
        "operation": selectedOperation
    }

def solveQuestion(operands, operation):
    if operation == "ADD":
        return operands["first"] + operands["second"]
    if operation == "SUB":
        return operands["first"] - operands["second"]
    if operation == "MUL":
        return operands["first"] * operands["second"]
    if operation == "DIV":
        return round(operands["first"] / operands["second"])