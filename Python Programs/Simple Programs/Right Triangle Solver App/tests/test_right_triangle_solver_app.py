# ------------------------------------ imports --------------------------- #
import unittest

import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/"\
                "Python Programs/Right Triangle Solver App/src")
import right_triangle_solver_app as rts

import math


# ------------------------------------ tests --------------------------- #
class right_triangle_solver_app_tests(unittest.TestCase):

    # hypotenuse tests 
    def test_hypotenuse_1(self):
        self.height = 10
        self.base = 20
        self.test_expected = math.hypot(self.height, self.base)
        self.test_output = rts.calc_hypotenuse(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_hypotenuse_2(self):
        self.height = 10.0000023234424
        self.base = 23.11232432
        self.test_expected = math.hypot(self.height, self.base)
        self.test_output = rts.calc_hypotenuse(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_hypotenuse_3(self):
        self.height = -23
        self.base = -5
        self.test_expected = math.hypot(self.height, self.base)
        self.test_output = rts.calc_hypotenuse(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_hypotenuse_4(self):
        self.height = -100
        self.base = 40
        self.test_expected = math.hypot(self.height, self.base)
        self.test_output = rts.calc_hypotenuse(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    

    # area tests 
    def test_area_1(self):
        self.height = 10
        self.base = 20
        self.test_expected = (self.height*self.base)/2
        self.test_output = rts.calc_area(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_area_2(self):
        self.height = 10.0000023234424
        self.base = 23.11232432
        self.test_expected = (self.height*self.base)/2
        self.test_output = rts.calc_area(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_area_3(self):
        self.height = -23
        self.base = -5
        self.test_expected = (self.height*self.base)/2
        self.test_output = rts.calc_area(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    
    def test_area_4(self):
        self.height = -100
        self.base = 40
        self.test_expected = (self.height*self.base)/2
        self.test_output = rts.calc_area(self.height, self.base)
        self.assertEqual(self.test_output, self.test_expected)
    

# ------------------------------------ run program ---------------------------#
if __name__ == "__main__":
    unittest.main()
