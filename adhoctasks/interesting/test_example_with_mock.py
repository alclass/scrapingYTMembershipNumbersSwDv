#!/usr/bin/env python3
"""
  docstring
"""

from unittest import TestCase
from unittest import mock
import adhoctasks.interesting.example_with_mock as ewm


class TestTarget(TestCase):
  def test_get_user_input(self):
    responses = ('Gregory', 'Lucas', '42', 'n')
    expected = "Your are Gregory Lucas and you're 42 years old"
    with mock.patch('builtins.input', side_effects=responses):
      self.assertEqual(ewm.get_user_input(), expected)


def process():
  pass


if __name__ == '__main__':
  process()
