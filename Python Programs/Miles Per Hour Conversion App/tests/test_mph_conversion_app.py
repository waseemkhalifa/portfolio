# ------------------------------------ imports --------------------------- #
import unittest

import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/"\
                "Python Programs/Miles Per Hour Conversion App/src")
import mph_conversion_app as mca


# ------------------------------------ tests --------------------------- #
class letter_counter_app_tests(unittest.TestCase):

    # test 1
    def test_1_no_decimal(self):
        self.mph = 23
        self.test_expected = round(self.mph * 0.4474, 2)
        self.test_output = mca.mph_converter(self.mph)
        self.assertEqual(self.test_output, self.test_expected)
    
    # test 2
    def test_2_decimal(self):
        self.mph = 23.629729272
        self.test_expected = round(self.mph * 0.4474, 2)
        self.test_output = mca.mph_converter(self.mph)
        self.assertEqual(self.test_output, self.test_expected)
    
    # test 3
    def test_3_minus(self):
        self.mph = -23.629729272
        self.test_expected = round(self.mph * 0.4474, 2)
        self.test_output = mca.mph_converter(self.mph)
        self.assertEqual(self.test_output, self.test_expected)


# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    unittest.main()
