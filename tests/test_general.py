import typing as t
import unittest


class first_test(unittest.TestCase):
    """Main test case"""

    @t.overload
    def test_stuff(self):  # type: () -> None
        """First test"""
        self.assertEqual(sum([1, 2, 3]), 6, "Should be 6")


if __name__ == '__main__':
    unittest.main()
