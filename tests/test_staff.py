import unittest
import os
from people import Staff
from data import Data


class PeopleTest(unittest.TestCase):
    """Tests for Staff Class"""

    def setUp(self):
        self.data = Data()

    def test_create_staff(self):
        """
        Assert that a user can add a new staff member
        """
        staff = self.data.fetch_data("staff", False)
        self.assertEqual(0, len(staff))

        new_staff = self.data.create_staff('Dej', 'Loaf')
        self.assertTrue(new_staff)

        staff = self.data.fetch_data("staff", False)
        self.assertEqual(1, len(staff))

        self.data.create_office_spaces(['camelot', 'midgar'])
        new_staff = self.data.create_staff('Dej', 'Loaf')
        self.assertTrue(new_staff)

        staff = self.data.fetch_data("staff", False)
        self.assertEqual(2, len(staff))

    def test_reallocate_staff(self):
        """
        Assert that a fellow can be reallocated to another office space
        """
        self.data.create_office_spaces(['camelot'])
        self.data.create_staff('John', 'Kariuki')

        staff = Staff()
        invalid_id = staff.reallocate(
            {'<person_identifier>': 10, '<new_room_name>': 'camelot'})
        self.assertEqual('No staff by the provided staff id 10', invalid_id)

        invalid_allocation = staff.reallocate(
            {'<person_identifier>': 1, '<new_room_name>': 'camelot'})
        self.assertEqual(
            'John Kariuki already belongs in camelot', invalid_allocation)

        invalid_office = staff.reallocate(
            {'<person_identifier>': 1, '<new_room_name>': 'imaginaryroom'})
        self.assertEqual(
            'No office space by that name. Please try again', invalid_office)

        self.data.create_office_spaces(['midgar'])
        valid_allocation = staff.reallocate(
            {'<person_identifier>': 1, '<new_room_name>': 'midgar'})
        self.assertEqual(
            'John Kariuki is now residing in midgar', valid_allocation)

    def test_unallocated_staff(self):
        """Get a list of unallocated staff members"""
        self.data.create_staff("John", "Kariuki")
        self.data.create_staff("Jhene", "Aiko")
        self.data.create_staff("Dej", "Loaf")
        self.data.create_office_spaces(['camelot'])
        self.data.create_staff('Steph', 'Curry')

        staff = Staff()
        unallocated_staff = staff.unallocated_people("staff")
        self.assertEquals(3, len(unallocated_staff))

    def test_no_vacancies_in_office_spaces(self):
        """
        Assert that a use is notified when there are no vacant office spaces to
        allocate staff members
        """
        self.data.create_office_spaces(['camelot'])

        self.data.create_staff("John", "Kariuki")
        self.data.create_staff("Blue", "October")
        self.data.create_staff("Steph", "Curry")
        self.data.create_staff("Para", "More")
        self.data.create_staff("Evey", "Eve")
        self.data.create_staff("Some", "Body")

        unlucky_staff = self.data.create_staff("Amos", "Omondi")
        self.assertEqual(
            'There are no vacant office spaces. Please check in later to allocate Amos Omondi', unlucky_staff)

        self.data.create_office_spaces(['midgar'])

        staff = Staff()
        self.data.create_staff("Penny", "Wanjiru")

        lucky_staff = staff.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 7,
             '<new_room_name>': 'midgar'})
        self.assertEqual('Amos Omondi is now residing in midgar', lucky_staff)

        unlucky_staff = staff.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 8,
             '<new_room_name>': 'camelot'})
        self.assertEqual(
            'camelot is already fully occupied. Please try another room', unlucky_staff)

    def tearDown(self):
        """Delete the test database"""
        self.data.clear_test_db()

if __name__ == '__main__':
    unittest.main()
