import unittest
from program import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account = BankAccount("Olena Golovach", 1000)

    def test_deposit(self):
        self.account.deposit(500)
        self.assertEqual(self.account.balance, 1500)

    def test_deposit_negative(self):
        with self.assertRaises(ValueError,msg="Deposit negative amount"):
            self.account.deposit(-1000)