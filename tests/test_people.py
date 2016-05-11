import unittest
import os
from data import Data
from people import Staff, Fellow, Person


class PeopleTest(unittest.TestCase):
    """Test for Pople (Staff and People)"""

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
        unallocated_staff = staff.unallocated()
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

        unlucky_staff = staff.reallocate(
            {'fellow': True, 'staff': False, '<person_identifier>': 8,
             '<new_room_name>': 'camelot'})
        self.assertEqual(
            'camelot is already fully occupied. Please try another room', unlucky_staff)

    def test_unallocated_people(self):
        """
        Get a list of all unallocated people printed on the screen
        and in a text file
        """
        self.data.create_office_spaces(['midgar'])
        self.data.create_living_spaces(['woodwing'])

        self.data.create_fellow("John", "Kariuki", "y")
        self.data.create_fellow("Blue", "October", "y")
        self.data.create_fellow("Blue", "October", "n")

        self.data.create_staff("John", "Kariuki")
        self.data.create_staff("Blue", "October")

        people = Person()
        people.unallocated({'--o': 'y'})
        self.assertTrue(os.path.exists('unallocated.txt'))

        with open('unallocated.txt') as f:
            lines = f.readlines()
            self.assertTrue('All staff have been assigned\n' in lines)
            self.assertTrue('Blue October\t[N]' in lines)
        os.remove('unallocated.txt')

    def tearDown(self):
        """Delete the test database"""
        if os.path.exists('room_alloc.db'):
            os.remove('room_alloc.db')

if __name__ == '__main__':
    unittest.main()
