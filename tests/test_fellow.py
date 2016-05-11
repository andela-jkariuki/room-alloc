import unittest
import os
from people import Fellow
from data import Data


class PeopleTest(unittest.TestCase):
    """Tests for Fellow class"""

    def setUp(self):
        self.data = Data()

    def test_create_fellow(self):
        """
        Assert that a user can add a new fellow
        """
        fellows = self.data.fetch_data("fellows", False)
        self.assertEqual(0, len(fellows))

        self.data.create_living_spaces(['woodwing', 'westwing', 'eastwing'])

        new_fellow = self.data.create_fellow("John", "Kariuki", "y")
        self.assertTrue(new_fellow)

        new_fellow = self.data.create_fellow("John", "Kariuki", "n")
        self.assertEqual("accomodation not provided for fellow.", new_fellow)

        fellows = self.data.fetch_data("fellows", False)
        self.assertEqual(2, len(fellows))

    def test_reallocate_fellow(self):
        """
        Assert that a user can reallocate a staff member
        """
        self.data.create_living_spaces(['woodwing'])
        self.data.create_fellow("John", "Kariuki", "y")

        fellow = Fellow()

        invalid_id = fellow.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 10,
             '<new_room_name>': 'camelot'})

        self.assertEqual('No fellow by the provided fellow id 10', invalid_id)

        invalid_allocation = fellow.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 1,
             '<new_room_name>': 'woodwing'})
        self.assertEqual(
            'John Kariuki already belongs in woodwing', invalid_allocation)

        invalid_room = fellow.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 1,
             '<new_room_name>': 'randomnam3'})
        self.assertEqual(
            'No living space by that name. Please try again', invalid_room)

        self.data.create_living_spaces(['midgar'])

        valid_allocation = fellow.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 1,
             '<new_room_name>': 'midgar'})
        self.assertEqual(
            'John Kariuki is now residing in midgar', valid_allocation)

    def test_unallocated_fellows(self):
        """Get a list of unallocated fellows"""
        self.data.create_living_spaces(['woodwing'])
        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_fellow("John", "Kariuki", "n")
        self.data.create_fellow("John", "Kariuki", "n")

        fellow = Fellow()
        unallocated_fellows = fellow.unallocated()
        self.assertEquals(2, len(unallocated_fellows))

    def test_no_vacancies_in_living_spaces(self):
        """
        Assert that a use is notified when there are no vacant living spaces to
        allocate fellows
        """
        self.data.create_living_spaces(['woodwing'])

        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_fellow("Blue", "October", "y")
        self.data.create_fellow("Steph", "Curry", "y")
        self.data.create_fellow("Para", "More", "y")

        unlucky_fellow = self.data.create_fellow("Amos", "Omondi", "y")
        self.assertEqual(
            'There are no vacant living spaces for now. Please check in later to accommodate Amos Omondi', unlucky_fellow)

        self.data.create_living_spaces(['bluewing'])

        fellow = Fellow()
        self.data.create_fellow("Penny", "Wanjiru", "y")

        unlucky_fellow = fellow.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 6,
             '<new_room_name>': 'woodwing'})
        self.assertEqual(
            'woodwing is already fully occupied. Please try another room', unlucky_fellow)

    def test_allocate_new_fellow(self):
        """Test allocate new fellow method
        """
        self.data.create_living_spaces(['woodwing'])
        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_living_spaces(['bluewing'])

        fellow = Fellow()
        wrong_space = fellow.allocate_new_fellow(
            (2, 'John Kariuki', 'N', None), 2, {'<new_room_name>': 'random3'})
        self.assertEqual(
            'No living space by that name. Please try again', wrong_space)

        allocate = fellow.allocate_new_fellow(
            (2, 'John Kariuki', 'N', None), 2, {'<new_room_name>': 'bluewing'})
        self.assertEqual(
            "John Kariuki is now residing in bluewing", allocate)

        for i in range(7):
            self.data.create_fellow("John", "Kariuki", "y")

        full_space = fellow.allocate_new_fellow(
            (2, 'John Kariuki', 'N', None), 2, {'<new_room_name>': 'bluewing'})
        self.assertEqual(
            "bluewing is already fully occupied. Please try another room",
            full_space)

    def tearDown(self):
        """Delete the test database"""
        self.data.clear_test_db()

if __name__ == '__main__':
    unittest.main()
