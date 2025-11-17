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
