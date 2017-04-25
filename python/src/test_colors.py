import unittest

from colors import summarize_frequencies, count_color_classes


class TestColorsFunction(unittest.TestCase):
    def test_summarize_frequencies(self):
        self.assertEqual(summarize_frequencies({'000000': 1}), 1)
        self.assertEqual(summarize_frequencies({'000000': 1,
                                                'FFFFFF': 2}), 3)
        self.assertEqual(summarize_frequencies({'000000': 1,
                                                'AEAEAE': 2,
                                                'FFFFFF': 3}), 6)

    def test_count_color_classes(self):
        test_input = [
            {
                'frequency': 5,
                'color_class': '000000'
            },
            {
                'frequency': 4,
                'color_class': '000000'
            },
            {
                'frequency': 10,
                'color_class': 'FFFFFF'
            },
        ]
        expected_output = {'000000': 9, 'FFFFFF': 10}
        self.assertEqual(count_color_classes(test_input), expected_output)


if __name__ == '__main__':
    unittest.main()
