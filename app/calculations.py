from _pytest.python_api import raises


def add(num1: int, num2: 2):
    return num1 + num2

def subtract(num1: int, num2: int):
    return num1 - num2

def multiply(num1: int, num2: int):
    return num1 * num2 

def divide(num1: int, num2: int):
    if num2 <= 0:
        raise ZeroDivisionError("Divisão por zero")
    else:    
        return num1 / num2 


class InsufficientFunds(Exception):
    pass

class BankAccount():
    def __init__(self, starting_balance=0):
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise InsufficientFunds("Saldo insuficiente")
        self.balance -= amount

    def collect_interest(self):
        self.balance *= 1.1   

