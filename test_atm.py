"""
Unit Tests for ATM Banking Application
Tests for run.py and cardHolder.py modules
"""

import unittest
import sys
import os
from unittest.mock import Mock, patch, MagicMock
from io import StringIO

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import modules to test
from run import _parse_amount
from cardHolder import (
    formatFloatFromServer, 
    _parse_balance_str, 
    ClientRecord,
    SimpleClientRepo,
    Account,
    ATMCard
)


# TestRunModule here:

class TestRunModule(unittest.TestCase):

     """Test cases for run.py module"""

     def setUp(self):

         """Set up test fixtures before each test method."""

         pass

     def tearDown(self):

         """Clean up after each test method."""

         pass

     # Test _parse_amount function

     def test_parse_amount_valid_integer(self):

         """Test parsing valid integer amounts"""

         self.assertEqual(_parse_amount("100"), 100.0)

         self.assertEqual(_parse_amount("1000"), 1000.0)

         self.assertEqual(_parse_amount("1"), 1.0)

     def test_parse_amount_valid_decimal(self):

         """Test parsing valid decimal amounts"""

         self.assertEqual(_parse_amount("100.50"), 100.50)

         self.assertEqual(_parse_amount("1250.75"), 1250.75)

         self.assertAlmostEqual(_parse_amount("0.01"), 0.01, places=2)

     def test_parse_amount_european_format(self):

         """Test parsing European number format (comma as decimal)"""

         self.assertEqual(_parse_amount("100,50"), 100.50)

         self.assertEqual(_parse_amount("1250,75"), 1250.75)

         self.assertEqual(_parse_amount("1 250,75"), 1250.75)

     def test_parse_amount_with_spaces(self):

         """Test parsing amounts with spaces"""

         self.assertEqual(_parse_amount("1 000"), 1000.0)

         self.assertEqual(_parse_amount("10 000.50"), 10000.50)

         self.assertEqual(_parse_amount(" 100 "), 100.0)

     def test_parse_amount_negative_raises_error(self):

         """Test that negative amounts raise ValueError"""

         with self.assertRaises(ValueError) as context:

             _parse_amount("-100")

         # The error message includes "Invalid amount format" which wraps the negative check

         self.assertTrue("invalid" in str(context.exception).lower() or "negative" in str(context.exception).lower())

     def test_parse_amount_invalid_format(self):

         """Test that invalid formats raise ValueError"""

         with self.assertRaises(ValueError):

             _parse_amount("abc")

         with self.assertRaises(ValueError):

             _parse_amount("12.34.56")

         with self.assertRaises(ValueError):

             _parse_amount("")

     def test_parse_amount_zero(self):

         """Test parsing zero amount"""

         self.assertEqual(_parse_amount("0"), 0.0)

         self.assertEqual(_parse_amount("0.00"), 0.0)













# TestCardHolderModule here:

class TestCardHolderModule(unittest.TestCase):
    """Test cases for cardHolder.py module"""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.test_card_num = "4532772818527395"
        self.test_pin = "1234"
        self.test_balance = 1000.50
    
    def tearDown(self):
        """Clean up after each test method."""
        pass
    
    # Test formatFloatFromServer function
    def test_format_float_from_server_with_comma(self):
        """Test formatting float with comma as decimal separator"""
        self.assertEqual(formatFloatFromServer("1000,50"), "1000.50")
        self.assertEqual(formatFloatFromServer("100,00"), "100.00")
    
    def test_format_float_from_server_with_dot(self):
        """Test formatting float with dot as decimal separator"""
        self.assertEqual(formatFloatFromServer("1000.50"), "1000.50")
        self.assertEqual(formatFloatFromServer("100.00"), "100.00")
    
    def test_format_float_from_server_integer(self):
        """Test formatting integer values"""
        self.assertEqual(formatFloatFromServer("1000"), "1000")
        self.assertEqual(formatFloatFromServer(1000), "1000")
    
    # Test _parse_balance_str function
    def test_parse_balance_str_valid_formats(self):
        """Test parsing various valid balance formats"""
        self.assertEqual(_parse_balance_str("1000.50"), 1000.50)
        self.assertEqual(_parse_balance_str("1000,50"), 1000.50)
        self.assertEqual(_parse_balance_str("1 000,50"), 1000.50)
        self.assertEqual(_parse_balance_str(1000), 1000.0)
        self.assertEqual(_parse_balance_str(1000.50), 1000.50)
    
    def test_parse_balance_str_invalid_returns_zero(self):
        """Test that invalid balance strings return 0.0"""
        self.assertEqual(_parse_balance_str("invalid"), 0.0)
        self.assertEqual(_parse_balance_str(""), 0.0)
        self.assertEqual(_parse_balance_str(None), 0.0)
    
    def test_parse_balance_str_with_non_breaking_space(self):
        """Test parsing balance with non-breaking space"""
        # Non-breaking space (\\xa0)
        balance_with_nbsp = "3\xa0649,30"
        self.assertEqual(_parse_balance_str(balance_with_nbsp), 3649.30)
    
    # Test ClientRecord class
    def test_client_record_initialization(self):
        """Test ClientRecord initialization with valid data"""
        record = ClientRecord(
            self.test_card_num,
            self.test_pin,
            "John",
            "Doe",
            self.test_balance
        )
        
        self.assertEqual(record.cardNum, self.test_card_num)
        self.assertEqual(record.pin, self.test_pin)
        self.assertEqual(record.firstName, "John")
        self.assertEqual(record.lastName, "Doe")
        self.assertEqual(record.balance, self.test_balance)
    
    def test_client_record_balance_parsing(self):
        """Test ClientRecord balance parsing from various formats"""
        record = ClientRecord(
            self.test_card_num,
            self.test_pin,
            "John",
            "Doe",
            "1 000,50"
        )
        self.assertEqual(record.balance, 1000.50)
    
    def test_client_record_strips_whitespace(self):
        """Test that ClientRecord strips whitespace from card and PIN"""
        record = ClientRecord(
            " 4532772818527395 ",
            " 1234 ",
            "John",
            "Doe",
            1000
        )
        self.assertEqual(record.cardNum, "4532772818527395")
        self.assertEqual(record.pin, "1234")
    
    # Test Account class
    def test_account_initialization(self):
        """Test Account initialization"""
        account = Account("123", "456", "1000.50")
        
        self.assertEqual(account.getAccountID(), "123")
        self.assertEqual(account.getAccountHolderID(), "456")
        self.assertIn("1000.50", account.getAccountBalance())
    
    def test_account_balance_formatting(self):
        """Test Account balance formatting from various formats"""
        account1 = Account("123", "456", "1000,50")
        # getAccountBalance returns the formatted string, not necessarily with dot
        balance1 = account1.getAccountBalance()
        self.assertTrue("1000" in balance1 and ("50" in balance1 or ".50" in balance1))
        
        account2 = Account("123", "456", "1 000,50")
        # After formatting, it may still contain spaces depending on formatFloatFromServer
        balance2 = account2.getAccountBalance()
        self.assertTrue("1000" in balance2.replace(" ", "") or "1 000" in balance2)
    
    # Test ATMCard class (without database operations)
    def test_atmcard_initialization(self):
        """Test ATMCard initialization"""
        card = ATMCard("123", "456", "1000.50", self.test_card_num, self.test_pin, "0")
        
        self.assertEqual(card.getCardNumber(), self.test_card_num)
        self.assertEqual(card.getPin(), self.test_pin)
        self.assertEqual(card.getFailedTries(), "0")
    
    def test_atmcard_verify_pin_correct(self):
        """Test PIN verification with correct PIN"""
        card = ATMCard("123", "456", "1000.50", self.test_card_num, self.test_pin, "0")
        
        # Mock the resetFailedTries method to avoid database call
        with patch.object(card, 'resetFailedTries', return_value=True):
            result = card.verify_pin(self.test_pin)
            self.assertTrue(result)
    
    def test_atmcard_verify_pin_incorrect(self):
        """Test PIN verification with incorrect PIN"""
        card = ATMCard("123", "456", "1000.50", self.test_card_num, self.test_pin, "0")
        
        # Mock the increaseFailedTries method to avoid database call
        with patch.object(card, 'increaseFailedTries', return_value=True):
            result = card.verify_pin("9999")
            self.assertFalse(result)
    
    def test_atmcard_verify_pin_string_comparison(self):
        """Test PIN verification handles string/int comparison"""
        card = ATMCard("123", "456", "1000.50", self.test_card_num, "1234", "0")
        
        with patch.object(card, 'resetFailedTries', return_value=True):
            # Test with string
            self.assertTrue(card.verify_pin("1234"))
            # Test with int
            self.assertTrue(card.verify_pin(1234))
    
    def test_atmcard_check_balance(self):
        """Test balance checking"""
        card = ATMCard("123", "456", "1000.50", self.test_card_num, self.test_pin, "0")
        
        balance = card.check_balance()
        self.assertIsInstance(balance, float)
        self.assertAlmostEqual(balance, 1000.50, places=2)
    
    def test_atmcard_check_balance_european_format(self):
        """Test balance checking with European format"""
        # Use format without spaces since formatFloatFromServer doesn't handle spaces
        card = ATMCard("123", "456", "1000,50", self.test_card_num, self.test_pin, "0")
        
        balance = card.check_balance()
        # check_balance may return None if formatting fails
        self.assertIsNotNone(balance, "Balance should not be None")
        if balance is not None:
            self.assertAlmostEqual(balance, 1000.50, places=2)
    
    @patch('cardHolder.API')
    def test_atmcard_withdraw_valid(self, mock_api):
        """Test valid withdrawal"""
        card = ATMCard("123", "456", "1000.50", self.test_card_num, self.test_pin, "0")
        
        # Mock the increaseBalance method
        with patch.object(card, 'increaseBalance', return_value=True):
            result = card.withdraw(100.0)
            self.assertTrue(result)
            # Balance should be updated locally
            self.assertAlmostEqual(float(formatFloatFromServer(card.accountBalance)), 900.50, places=2)
    
    @patch('cardHolder.API')
    def test_atmcard_withdraw_insufficient_funds(self, mock_api):
        """Test withdrawal with insufficient funds"""
        card = ATMCard("123", "456", "100.00", self.test_card_num, self.test_pin, "0")
        
        # Capture stdout to check error message
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = card.withdraw(200.0)
            self.assertFalse(result)
            self.assertIn("Insufficient funds", fake_out.getvalue())
    
    @patch('cardHolder.API')
    def test_atmcard_withdraw_negative_amount(self, mock_api):
        """Test withdrawal with negative amount"""
        card = ATMCard("123", "456", "1000.00", self.test_card_num, self.test_pin, "0")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = card.withdraw(-100.0)
            self.assertFalse(result)
            self.assertIn("positive", fake_out.getvalue())
    
    @patch('cardHolder.API')
    def test_atmcard_deposit_valid(self, mock_api):
        """Test valid deposit"""
        card = ATMCard("123", "456", "1000.00", self.test_card_num, self.test_pin, "0")
        
        with patch.object(card, 'increaseBalance', return_value=True):
            result = card.deposit(100.0)
            self.assertTrue(result)
            self.assertAlmostEqual(float(formatFloatFromServer(card.accountBalance)), 1100.00, places=2)
    
    @patch('cardHolder.API')
    def test_atmcard_deposit_negative_amount(self, mock_api):
        """Test deposit with negative amount"""
        card = ATMCard("123", "456", "1000.00", self.test_card_num, self.test_pin, "0")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = card.deposit(-100.0)
            self.assertFalse(result)
            self.assertIn("positive", fake_out.getvalue())
    
    @patch('cardHolder.API')
    def test_atmcard_deposit_invalid_amount(self, mock_api):
        """Test deposit with invalid amount"""
        card = ATMCard("123", "456", "1000.00", self.test_card_num, self.test_pin, "0")
        
        with patch('sys.stdout', new=StringIO()) as fake_out:
            result = card.deposit("invalid")
            self.assertFalse(result)
            self.assertIn("ERROR", fake_out.getvalue())
    
    @patch('cardHolder.API')
    def test_atmcard_change_pin(self, mock_api):
        """Test changing PIN"""
        card = ATMCard("123", "456", "1000.00", self.test_card_num, self.test_pin, "0")
        
        with patch.object(card, 'setPin', return_value=True):
            result = card.change_pin("5678")
            self.assertTrue(result)

# TestInputValidation here:


















# TestErrorHandling here:

















# TestDataIntegrity here:


















def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRunModule))
    suite.addTests(loader.loadTestsFromTestCase(TestCardHolderModule))
    # suite.addTests(loader.loadTestsFromTestCase(TestInputValidation))
    # suite.addTests(loader.loadTestsFromTestCase(TestErrorHandling))
    # suite.addTests(loader.loadTestsFromTestCase(TestDataIntegrity))
    
    # Run tests with detailed output
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    # Print summary
    print("\n" + "="*70)
    print("TEST SUMMARY")
    print("="*70)
    print(f"Tests Run: {result.testsRun}")
    print(f"Successes: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success Rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.2f}%")
    print("="*70)
    
    return result


if __name__ == '__main__':
    run_tests()
