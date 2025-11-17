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























def run_tests():
    """Run all tests and generate report"""
    # Create test suite
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Add all test classes
    suite.addTests(loader.loadTestsFromTestCase(TestRunModule))
    # suite.addTests(loader.loadTestsFromTestCase(TestCardHolderModule))
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
