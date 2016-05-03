import random
from db.dbManager import DBManager
from rooms import Rooms, LivingSpace, OfficeSpace
from pprint import pprint as pp

class Person:
    def __init__(self, first_name, last_name):
        self.name = first_name + ' ' + last_name

class Staff(Person):
    def __init__(self, args):
        self.person = Person(args['<first_name>'], args['<last_name>'])
        self.db = DBManager('room_alloc.db')
        self.add_staff()

    def add_staff(self):
        """add a new staff to the system"""
        office_spaces = OfficeSpace().office_spaces()
        office_space = random.choice([i for i in office_spaces if i[-1] < OfficeSpace.room_space])
        new_staff = "INSERT INTO staff(name, room_id) VALUES ('%s', %d)" % (self.person.name, office_space[0])

        staff_id = self.db.insert(new_staff)

        if staff_id:
            print("New Staff succesfully added. Staff ID is %d" % (staff_id))
            print('%s office space is in %s.' % (self.person.name, office_space[1]))
        else:
            print("Error adding new staff. Please try again")


class Fellow(Person):
    def __init__(self, args):
        self.person = Person(args['<first_name>'], args['<last_name>'])
        self.accomodation  = 'Y' if args['--a'].lower() == 'y' else 'N'

        self.db = DBManager('room_alloc.db')
        self.add_fellow()

    def add_fellow(self):
        """add a new fellow to the system"""
        new_fellow_query = "INSERT INTO fellows(name, accomodation) VALUES('{name}', '{accomodation}')".format(name = self.person.name, accomodation =  self.accomodation)

        fellow_id = self.db.insert(new_fellow_query)

        if fellow_id:
            print("New fellow succesfully added. Fellow ID is %d" % (fellow_id))
            if self.accomodation == 'Y':
                print('Searching for accomodation for the fellow...')
                self.accomodate_fellow(fellow_id)
            else:
                print('accomodation not provided for fellow.')
        else:
            print("Error adding new fellow. Please try again")

    def accomodate_fellow(self, fellow_id):
        """Accomodate a new fellow"""
        vacant_living_spaces = LivingSpace().living_spaces()
        living_space = random.choice([i for i in vacant_living_spaces if i[-1] < OfficeSpace.room_space])
        query = "UPDATE fellows SET room_id = %d WHERE id = %d" % (living_space[0], fellow_id)
        if self.db.update(query):
            print("{} is now accommodated in {}".format(self.person.name, living_space[1]))
        else:
            print("Error acomomdating {}".format(self.person.name))



