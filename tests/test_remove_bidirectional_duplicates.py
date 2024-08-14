""" Test the conversion module. """
import os
import sys
import unittest
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from sgconversion import remove_bidirectional_duplicates, Tuple  # pylint: disable=wrong-import-position

class TestConversion(unittest.TestCase):
    """
    Test for bidirectional duplicates removal.
    """

    @patch('builtins.open')
    def test_filter_bidirectional(self):
        """Test the filter_log_file function."""
        # Mock the file content
        #in_tuples = [('a', 'left', 'b'), ('b', 'right', 'a')]
        in_tuples = [Tuple('a', 'left', 'b'), Tuple('b', 'right', 'a')]

        out_tuples = remove_bidirectional_duplicates(in_tuples)

        self.assertEqual(len(out_tuples), 1)
        o_tuple = out_tuples[0]
        self.assertTrue(
            (o_tuple.x == 'a' and o_tuple.y == 'left' and o_tuple.z == 'b') or
            (o_tuple.x == 'b' and o_tuple.y == 'right' and o_tuple.z == 'a')
        )

    @patch('builtins.open')
    def test_filter_dublictaed(self):
        """Test the filter_log_file function."""
        # Mock the file content
        #in_tuples = [('a', 'left', 'b'), ('b', 'right', 'a')]
        in_tuples = [Tuple('a', 'left', 'b'), Tuple('a', 'left', 'b')]

        out_tuples = remove_bidirectional_duplicates(in_tuples)

        self.assertEqual(len(out_tuples), 1)
        o_tuple = out_tuples[0]
        self.assertTrue(
            o_tuple.x == 'a' and o_tuple.y == 'left' and o_tuple.z == 'b'
        )

    @patch('builtins.open')
    def test_filter_single(self):
        """Test the filter_log_file function."""
        # Mock the file content
        #in_tuples = [('a', 'left', 'b'), ('b', 'right', 'a')]
        in_tuples = [Tuple('a', 'left', 'b')]

        out_tuples = remove_bidirectional_duplicates(in_tuples)

        self.assertEqual(len(out_tuples), 1)
        o_tuple = out_tuples[0]
        self.assertTrue(
            o_tuple.x == 'a' and o_tuple.y == 'left' and o_tuple.z == 'b'
        )

    @patch('builtins.open')
    def test_filter_two_biderections1(self):
        """Test the filter_log_file function."""
        # Mock the file content
        #in_tuples = [('a', 'left', 'b'), ('b', 'right', 'a')]
        in_tuples = [Tuple('a', 'left', 'b'), Tuple('b', 'right', 'a'),
                     Tuple('a', 'beneath', 'b'), Tuple('b', 'above', 'a')]

        out_tuples = remove_bidirectional_duplicates(in_tuples)

        self.assertEqual(len(out_tuples), 2)
        o_tuple = out_tuples[0]
        self.assertTrue(
            (o_tuple.x == 'a' and o_tuple.y == 'left' and o_tuple.z == 'b') or
            (o_tuple.x == 'b' and o_tuple.y == 'right' and o_tuple.z == 'a')
        )
        o_tuple = out_tuples[1]
        self.assertTrue(
            (o_tuple.x == 'a' and o_tuple.y == 'beneath' and o_tuple.z == 'b') or
            (o_tuple.x == 'b' and o_tuple.y == 'above' and o_tuple.z == 'a')
        )

    @patch('builtins.open')
    def test_filter_two_biderections2(self):
        """Test the filter_log_file function."""
        # Mock the file content
        #in_tuples = [('a', 'left', 'b'), ('b', 'right', 'a')]
        in_tuples = [Tuple('a', 'left', 'b'), Tuple('b', 'right', 'a'),
                     Tuple('a', 'in front of', 'b'), Tuple('b', 'behind', 'a'),
                     Tuple('a', 'beneath', 'b'), Tuple('b', 'above', 'a'),
                     Tuple('x', 'in front of', 'y'), Tuple('y', 'behind', 'x'),
                     Tuple('x', 'beneath', 'y'), Tuple('y', 'above', 'x'),
                     Tuple('x', 'same level', 'y'), Tuple('y', 'same level', 'x')]

        out_tuples = remove_bidirectional_duplicates(in_tuples)

        self.assertEqual(len(out_tuples), 6)

if __name__ == '__main__':
    unittest.main()
