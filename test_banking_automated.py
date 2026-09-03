"""
Banking System - Q7: Testing using Automated Tools (pytest)

Automated unit/regression test suite for the Banking System,
run using the pytest framework (pip install pytest; pytest -v).
"""

import pytest
from banking_system import (
    Bank, Account, InsufficientFundsError, InvalidAmountError,
    AccountNotFoundError
)


@pytest.fixture
def bank():
    return Bank("Test Bank")


# ---------------------- Account Creation ----------------------

def test_open_account_with_initial_deposit(bank):
    acc = bank.open_account("Alice", 1000)
    assert acc.balance == 1000
    assert acc.owner_name == "Alice"


def test_open_account_default_zero_balance(bank):
    acc = bank.open_account("Bob")
    assert acc.balance == 0


def test_open_account_negative_deposit_raises(bank):
    with pytest.raises(InvalidAmountError):
        bank.open_account("Eve", -50)


def test_account_numbers_are_unique(bank):
    a1 = bank.open_account("User1")
    a2 = bank.open_account("User2")
    assert a1.account_number != a2.account_number


# ---------------------- Deposit ----------------------

def test_deposit_increases_balance(bank):
    acc = bank.open_account("Carol", 500)
    bank.deposit(acc.account_number, 200)
    assert bank.balance_inquiry(acc.account_number) == 700


@pytest.mark.parametrize("amount", [0, -10, -1000])
def test_deposit_invalid_amount_raises(bank, amount):
    acc = bank.open_account("Dave", 500)
    with pytest.raises(InvalidAmountError):
        bank.deposit(acc.account_number, amount)


def test_deposit_unknown_account_raises(bank):
    with pytest.raises(AccountNotFoundError):
        bank.deposit(99999, 100)


# ---------------------- Withdraw ----------------------

def test_withdraw_decreases_balance(bank):
    acc = bank.open_account("Frank", 1000)
    bank.withdraw(acc.account_number, 300)
    assert bank.balance_inquiry(acc.account_number) == 700


def test_withdraw_exact_balance_allowed(bank):
    acc = bank.open_account("Grace", 250)
    new_balance = bank.withdraw(acc.account_number, 250)
    assert new_balance == 0


def test_withdraw_more_than_balance_raises(bank):
    acc = bank.open_account("Heidi", 100)
    with pytest.raises(InsufficientFundsError):
        bank.withdraw(acc.account_number, 101)


@pytest.mark.parametrize("amount", [0, -50])
def test_withdraw_invalid_amount_raises(bank, amount):
    acc = bank.open_account("Ivan", 500)
    with pytest.raises(InvalidAmountError):
        bank.withdraw(acc.account_number, amount)


# ---------------------- Balance Inquiry ----------------------

def test_balance_inquiry_correct_value(bank):
    acc = bank.open_account("Judy", 3300)
    assert bank.balance_inquiry(acc.account_number) == 3300


def test_balance_inquiry_unknown_account_raises(bank):
    with pytest.raises(AccountNotFoundError):
        bank.balance_inquiry(424242)


# ---------------------- Transfer ----------------------

def test_transfer_moves_funds_correctly(bank):
    a = bank.open_account("Source", 1000)
    b = bank.open_account("Target", 200)
    src_bal, dst_bal = bank.transfer(a.account_number, b.account_number, 400)
    assert src_bal == 600
    assert dst_bal == 600


def test_transfer_insufficient_funds_raises(bank):
    a = bank.open_account("Source2", 50)
    b = bank.open_account("Target2", 200)
    with pytest.raises(InsufficientFundsError):
        bank.transfer(a.account_number, b.account_number, 100)
    # Ensure balances are unchanged after the failed transfer
    assert bank.balance_inquiry(a.account_number) == 50
    assert bank.balance_inquiry(b.account_number) == 200


def test_transfer_unknown_source_account_raises(bank):
    b = bank.open_account("Target3", 200)
    with pytest.raises(AccountNotFoundError):
        bank.transfer(11111, b.account_number, 50)


def test_transfer_unknown_target_account_raises(bank):
    a = bank.open_account("Source3", 200)
    with pytest.raises(AccountNotFoundError):
        bank.transfer(a.account_number, 22222, 50)


# ---------------------- Account Closure / Bank-level ----------------------

def test_close_account_removes_it(bank):
    acc = bank.open_account("Closing User", 100)
    bank.close_account(acc.account_number)
    with pytest.raises(AccountNotFoundError):
        bank.balance_inquiry(acc.account_number)


def test_total_assets_sums_all_accounts(bank):
    bank.open_account("A", 1000)
    bank.open_account("B", 2500)
    bank.open_account("C", 500)
    assert bank.total_assets() == 4000


# ---------------------- Transaction History ----------------------

def test_transaction_recorded_after_deposit(bank):
    acc = bank.open_account("Historian", 100)
    bank.deposit(acc.account_number, 50)
    assert len(acc.transactions) == 2  # OPEN + DEPOSIT
    assert acc.transactions[-1].txn_type == "DEPOSIT"
