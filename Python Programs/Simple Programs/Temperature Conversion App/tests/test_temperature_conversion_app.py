# ------------------------------------ imports --------------------------- #
import unittest

import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/"\
                "Python Programs/Temperature Conversion App/src")
import temperature_conversion_app as tca


# ------------------------------------ tests --------------------------- #
class temperature_conversion_app_tests(unittest.TestCase):

    # fahrenheit to celsius tests 
    def test_f_to_c_1(self):
        self.fahrenheit = 23
        self.test_expected = (self.fahrenheit-32) * (5/9)
        self.test_output = tca.f_to_c_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_f_to_c_2(self):
        self.fahrenheit = 123.88899007222
        self.test_expected = (self.fahrenheit-32) * (5/9)
        self.test_output = tca.f_to_c_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_f_to_c_3(self):
        self.fahrenheit = -123.88899007222
        self.test_expected = (self.fahrenheit-32) * (5/9)
        self.test_output = tca.f_to_c_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_f_to_c_4(self):
        self.fahrenheit = -123
        self.test_expected = (self.fahrenheit-32) * (5/9)
        self.test_output = tca.f_to_c_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    

    # fahrenheit to kelvin tests 
    def test_f_to_k_1(self):
        self.fahrenheit = 23
        self.test_expected = (self.fahrenheit-32) * (5/9) + 273.15
        self.test_output = tca.f_to_k_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_f_to_k_2(self):
        self.fahrenheit = 123.88899007222
        self.test_expected = (self.fahrenheit-32) * (5/9) + 273.15
        self.test_output = tca.f_to_k_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_f_to_k_3(self):
        self.fahrenheit = -123.88899007222
        self.test_expected = (self.fahrenheit-32) * (5/9) + 273.15
        self.test_output = tca.f_to_k_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_f_to_k_4(self):
        self.fahrenheit = -123
        self.test_expected = (self.fahrenheit-32) * (5/9) + 273.15
        self.test_output = tca.f_to_k_converter(self.fahrenheit)
        self.assertEqual(self.test_output, self.test_expected)
    

# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    unittest.main()
