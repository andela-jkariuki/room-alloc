import unittest
from db.dbManager import DBManager


class RoomTest(unittest.TestCase):
    """Test for rooms (living spaces and Office spaces)"""
    def setUp(self):
        self.db = DBManager('test.db')

    def test_true(self):
        self.assertTrue(True)

    def test_false(self):
        self.assertFalse(False)

if __name__ == '__main__':
    unittest.main()
