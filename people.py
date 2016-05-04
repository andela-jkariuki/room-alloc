import random
from db.dbManager import DBManager
from rooms import Rooms, LivingSpace, OfficeSpace
from pprint import pprint as pp

class Person:
    def __init__(self, first_name, last_name):
        self.db = DBManager('room_alloc.db')
        self.name = first_name + ' ' + last_name

class Staff(Person):
    def __init__(self):
        self.db = DBManager('room_alloc.db')

    def add_staff(self, args):
        """Add a new staff member to the system"""

        self.person = Person(args['<first_name>'], args['<last_name>'])

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

    def reallocate(self, args):
        """Reallocate a staff member to a new office space"""

        staff_id = int(args['<person_identifier>'])
        staff = self.db.select_one("SELECT * FROM staff WHERE id = %d"% (staff_id))

        if staff:
            old_room = self.db.select_one("SELECT * FROM rooms WHERE id = %d AND type='O'" % (staff[-1]))
            new_room_name = args['<new_room_name>']

            if old_room[1] != new_room_name:
                office = OfficeSpace()
                new_room = office.office_space(new_room_name)

                if new_room:
                    room_occupancy = office.office_space_occupancy(new_room[0])
                    if len(room_occupancy) < office.room_space:
                        if office.allocate_room(staff_id, new_room[0]):
                            print("%s is now residing in %s" % (staff[1], new_room_name))
                    else:
                        print("%s is already fully occupied. Please try another room" % (new_room_name))
                else:
                    print("No office space by that name. Please try again")
            else:
                print("%s already belongs in %s" % (staff[1], new_room_name))
        else:
            print("No staff by the provided staff id '%d'" % staff_id)


class Fellow(Person):
    def __init__(self):
        self.db = DBManager('room_alloc.db')

    def add_fellow(self, args):
        """Add a new fellow to the system"""

        self.person = Person(args['<first_name>'], args['<last_name>'])
        self.accomodation  = 'Y' if args['--a'].lower() == 'y' else 'N'
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
        """Accomodate a new fellow in the living spaces"""

        vacant_living_spaces = LivingSpace().living_spaces()
        print(OfficeSpace.room_space)
        living_space = random.choice([i for i in vacant_living_spaces if i[-1] < LivingSpace.room_space])
        query = "UPDATE fellows SET room_id = %d WHERE id = %d" % (living_space[0], fellow_id)
        if self.db.update(query):
            print("{} is now accommodated in {}".format(self.person.name, living_space[1]))
        else:
            print("Error acomomdating {}".format(self.person.name))

    def reallocate(self, args):
        """Reallocate an existing fellow to a new room"""

        fellow_id = int(args['<person_identifier>'])
        fellow = self.db.select_one("SELECT * FROM fellows WHERE id = %d"% (fellow_id))
        if fellow:
            old_room = self.db.select_one("SELECT * FROM rooms WHERE id = %d AND type='L'" % (fellow[-1]))
            new_room_name = args['<new_room_name>']
            if old_room[1] != new_room_name:
                living = LivingSpace()
                new_room = living.living_space(new_room_name)
                if new_room:
                    room_occupancy = living.living_space_occupancy(new_room[0])
                    if len(room_occupancy) < living.room_space:
                        if living.allocate_room(fellow_id, new_room[0]):
                            print("%s is now residing in %s" % (fellow[1], new_room_name))
                    else:
                        print("%s is already fully occupied. Please try another room" % (new_room_name))
                else:
                    print("No living space by that name. Please try again")
            else:
                print("%s already belongs in %s" % (fellow[1], new_room_name))
        else:
            print("No fellow by the provided fellow id '%d'" % fellow_id)



