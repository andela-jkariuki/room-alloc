import unittest

class AmityTest(unittest.TestCase):
    def test_true(self):
        self.assertTrue(True)
    def test_false(self):
        self.assertFalse(False)

if __name__ == '__main__':
    unittest.main()