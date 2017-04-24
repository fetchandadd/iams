import unittest

from colors import summarize_frequencies


class TestColorsFunction(unittest.TestCase):
    def test_summarize_frequencies(self):
        self.assertEqual(summarize_frequencies({'000000': 1}), 1)
        self.assertEqual(summarize_frequencies({'000000': 1,
                                                'FFFFFF': 2}), 3)
        self.assertEqual(summarize_frequencies({'000000': 1,
                                                'AEAEAE': 2,
                                                'FFFFFF': 3}), 6)


if __name__ == '__main__':
    unittest.main()
