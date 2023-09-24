# ------------------------------------ imports --------------------------- #
import unittest

import sys
sys.path.append("/home/waseem/Documents/Self-Development/git_repos/portfolio/"\
                "Python Programs/Letter Counter App/src")
import letter_counter_app as lca

# ------------------------------------ tests --------------------------- #
class letter_counter_app_tests(unittest.TestCase):

    # test 1
    def test_1(self):
        self.name = "waseem"

        self.message = "hello"

        self.letter = "l"

        self.count_of_letters = lca.count_letter_occurence(self.letter, 
                                                           self.message)

        self.test_output = lca.app_output(self.name, 
                                          self.letter,
                                          self.count_of_letters)
        self.test_expected = "waseem, your message has 2 l's in it."
        self.assertEqual(self.test_output, self.test_expected)
    

    # test 2
    def test_2_zero(self):
        self.name = "waseem"

        self.message = "hello"

        self.letter = "x"

        self.count_of_letters = lca.count_letter_occurence(self.letter, 
                                                           self.message)

        self.test_output = lca.app_output(self.name, 
                                          self.letter,
                                          self.count_of_letters)
        self.test_expected = "waseem, your message has 0 x's in it."
        self.assertEqual(self.test_output, self.test_expected)


    # test 3
    def test_3_capital(self):
        self.name = "waseem"

        self.message = "helloHHH"

        self.letter = "h"

        self.count_of_letters = lca.count_letter_occurence(self.letter, 
                                                           self.message)

        self.test_output = lca.app_output(self.name, 
                                          self.letter,
                                          self.count_of_letters)
        self.test_expected = "waseem, your message has 4 h's in it."
        self.assertEqual(self.test_output, self.test_expected)


# ------------------------------------ main --------------------------- #
if __name__ == "__main__":
    unittest.main()
