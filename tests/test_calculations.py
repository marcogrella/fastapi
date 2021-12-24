import pytest
from app.calculations import add, subtract, multiply, divide, BankAccount
from app.calculations import InsufficientFunds

# com a parametrização do pytest é possível realizar vários testes 

# o @fixture facilita na hora de reaproveitar códigos

@pytest.fixture
def zero_bank_account():
    return BankAccount()

@pytest.fixture
def default_bank_account():
    return BankAccount(50)


@pytest.mark.parametrize("num1, num2, expected", 
    [
    (3, 2, 5),
    (7, 1, 8),
    (20, 20, 40)
    ])
def test_add(num1, num2, expected):
    print()
    assert add(num1, num2) == expected

def test_subtract():
    assert subtract(9, 4) == 5


def test_multiply():
    assert multiply(9, 4) == 36


def test_divide():
    assert divide(10, 5) == 2

def test_divide_exception():
    with pytest.raises(ZeroDivisionError):
        assert divide(10, 0) == 2

# zero_bank_account faz referência ao método que já retorna um objeto do tipo BankAccount 
def test_bank_set_default_amount(zero_bank_account): 
   assert zero_bank_account.balance == 0


def test_bank_set_initial_amount(default_bank_account):
   assert default_bank_account.balance == 50


def test_bank_withdraw_amount(default_bank_account):
   default_bank_account.withdraw(30) 
   assert default_bank_account.balance == 20


def test_bank_deposit_amount(default_bank_account):
   default_bank_account.deposit(30) 
   assert default_bank_account.balance == 80   

def test_bank_collect_interest(default_bank_account):
    default_bank_account.collect_interest()
    assert round(default_bank_account.balance, 6) == 55   
 


def test_bank_transaction(zero_bank_account):
    zero_bank_account.deposit(200)
    zero_bank_account.withdraw(100)
    assert zero_bank_account.balance == 100

@pytest.mark.parametrize("deposited, withdrew, expected", [
    (200, 100, 100),
    (300, 150, 150),
    (1000, 120, 880)
    ])
def test_bank_many_transactions(zero_bank_account, deposited, withdrew, expected):
    zero_bank_account.deposit(deposited)
    zero_bank_account.withdraw(withdrew)
    assert zero_bank_account.balance == expected



def test_bank_insufficient_balance_transactions(default_bank_account):
    with pytest.raises(InsufficientFunds):
        default_bank_account.withdraw(200)