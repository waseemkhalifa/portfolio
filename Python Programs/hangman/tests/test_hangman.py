import unittest

# ------------------------------------ functions --------------------------- #
# this function will replace the word with dashes
def dash_word(word):
    word_list = []
    for letter in range(0, len(word)):
        word_list.append("_")
    word_dashed = " ".join(word_list)
    return word_dashed


# ------------------------------------ tests --------------------------- #
class word_frequency_finder_tests(unittest.TestCase):

    # test for dash_word function
    def test_dash_word(self):
        self.test_input = "hello"
        self.test_expected = "_ _ _ _ _"
        self.test_output = dash_word(self.test_input)
        self.assertEqual(self.test_output, self.test_expected)











# ------------------------------------ main --------------------------- #
if __name__ == "__main__":
    unittest.main()
