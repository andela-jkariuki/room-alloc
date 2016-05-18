#!/usr/bin/env python
"""Room Classes"""
import random
import tkFileDialog as tk
from db.dbManager import DBManager
from rooms import LivingSpace, OfficeSpace, Rooms


class Person:
    """Rooms class to handle behaviors common to both Fellows and staff"""

    def __init__(self):
        """Create instance of the database"""
        self.db = DBManager()

    def set_name(self, first_name, last_name):
        """Return a sentence cased name from first and last name

        Arguments:
                first_name (string) A person's first name
                last_name (string)  A person's last name
        """
        name = first_name + ' ' + last_name
        self.name = name.title()

    def unallocated(self, args):
        """Print out a list of all unallocated fellows and staff members"""
        unallocated_fellows = Fellow().unallocated_people("fellow")
        unallocated_staff = Staff().unallocated_people("staff")

        output = ''
        output += '*' * 30 + "\nSTAFF\n" + '*' * 30 + "\n"
        if unallocated_staff and len(unallocated_staff) != 0:
            output += "\n".join([str(i[1]) for i in unallocated_staff])
        else:
            output += 'All staff have been assigned'

        output += '\n\n' + '*' * 30 + "\nFELLOWS\n" + '*' * 30 + "\n"
        if unallocated_fellows and len(unallocated_fellows) != 0:
            output += "\n".join([str(i[1]) + '\t[' +
                                 str(i[2]) + ']' for i in unallocated_fellows])
        else:
            output += 'All fellows have been assigned'

        print(output)
        if args['--o'] is not None:
            with open('unallocated.txt', 'wt') as f:
                f.write(output)
                print("Unallocated people printed out to %s" %
                      ('unallocated.txt'))

    def allocate_from_file(self, args):  # pragma: no cover
        """Allocate rooms to users from a file"""
        file = tk.askopenfile(
            mode='rt', title='Load list of people to allocate rooms')

        fellows = []
        staff = []
        with open(file.name, 'r') as f:
            people = f.readlines()
            for person in people:
                person = person.split()
                person_type = 'F' if person[2] == 'FELLOW' else 'S'

                if person_type == 'F':
                    try:
                        fellow = {}
                        fellow['<first_name>'] = person[0]
                        fellow['<last_name>'] = person[1]
                        fellow['--a'] = person[3]
                        fellows.append(fellow)
                    except:
                        print("Invalid data in file")

                else:
                    staff_member = {}
                    staff_member['<first_name>'] = person[0]
                    staff_member['<last_name>'] = person[1]
                    staff.append(staff_member)

            for i in range(len(fellows)):
                print(Fellow().add_fellow(fellows[i]))

            for j in range(len(staff)):
                print(Staff().add_staff(staff[j]))

    def unallocated_people(self, person_type):
        """Get a list of unallocated people (fellows or staff)
        Arguments:
                person_type     type of unallocated people to get
                                (fellow or staff)
        Returns:
                List of unallocated fellows or False
        """
        if person_type == "fellow":
            unallocated = self.person.db.select("""SELECT * FROM fellows
                WHERE room_id is NULL or room_id = ''""")
        elif person_type == "staff":
            unallocated = self.person.db.select("""SELECT * FROM staff
            WHERE room_id is NULL or room_id = ''""")
        if unallocated:
            return unallocated


class Staff(Person):
    """Staff contains the characteristics and behaviors of a staff member"""

    def __init__(self):
        """Create instance of the database"""
        self.person = Person()

    def add_staff(self, args):
        """Add a new staff member to the system

        Arguments:
                args (dict) First Name and Last name of the user

        Returns:
            Boolean     True if successful, otherwise False
        """
        self.person.set_name(args['<first_name>'], args['<last_name>'])

        office_spaces = OfficeSpace().vacancies("office")
        if len(office_spaces) != 0:
            office_space = random.choice(office_spaces)
            new_staff = """INSERT INTO staff(name, room_id)
            VALUES ('%s', %d)""" % (self.person.name, office_space[0])

        else:
            new_staff = """INSERT INTO staff(name, room_id)
            VALUES ('%s', NULL)""" % (self.person.name)

        staff_id = self.person.db.insert(new_staff)

        if staff_id:
            print("%s succesfully added. Staff ID is %d" %
                  (self.person.name, staff_id))

            if len(office_spaces) != 0:
                print("%s's office space is in %s." %
                      (self.person.name, office_space[1]))
                return True

            return "There are no vacant office spaces. Please check in later to allocate %s" % (
                    self.person.name)

    def reallocate(self, args):
        """Reallocate a staff member to a new office space

        Arguments:
                args (dict) Person Identifier and the office to reallocate to

        Returns:
            Boolean     True if successful, otherwise False
        """

        staff_id = int(args['<person_identifier>'])
        staff = self.person.db.select_one(
            "SELECT * FROM staff WHERE id = %d" % (staff_id))

        if staff:
            if staff[-1] is not None:
                old_room = self.person.db.select_one(
                    """SELECT * FROM rooms
                    WHERE id = %d AND type='O'""" % (staff[-1]))
            else:
                old_room = [None, 'no prior office space']

            new_room_name = args['<new_room_name>']

            if old_room[1] != new_room_name:
                office = OfficeSpace()
                new_room = office.space("O", new_room_name)

                if new_room:
                    room_occupancy = office.occupancy("office", new_room[0])
                    if len(room_occupancy) < office.room_space:
                        if office.allocate_room("staff", staff_id, new_room[0]):
                            return "%s is now residing in %s" % (
                                staff[1], new_room_name)
                    else:
                        return "%s is fully occupied." % (new_room_name)
                else:
                    return "No office space by that name. Please try again"
            else:
                return "%s already belongs in %s" % (staff[1], new_room_name)
        else:
            return "No staff by the provided staff id %d" % staff_id


class Fellow(Person):
    """Class Fellow contains the characteristics and behaviors of the
    a Fellow
    """

    def __init__(self):
        """Create instance of the database"""
        self.person = Person()

    def add_fellow(self, args):
        """Add a new fellow to the system"""
        self.person.set_name(args['<first_name>'], args['<last_name>'])

        self.accomodation = 'Y' if args['--a'] is not None\
                            and args['--a'].lower() == 'y' else 'N'

        fellow_id = self.person.db.insert(
            """INSERT INTO fellows(name, accomodation)
            VALUES('{name}', '{accomodation}')""".format(
                name=self.person.name,
                accomodation=self.accomodation))

        if fellow_id:
            print("%s succesfully added. Fellow ID is %d" %
                  (self.person.name, fellow_id))
            if self.accomodation == 'Y':
                print('Searching for accomodation for the fellow...')
                return self.accomodate_fellow(fellow_id)
            else:
                return 'accomodation not provided for fellow.'

    def accomodate_fellow(self, fellow_id):
        """Accomodate a new fellow in the living spaces"""

        vacant_living_spaces = Rooms().vacancies("living")

        if len(vacant_living_spaces) != 0:
            living_space = random.choice(vacant_living_spaces)
            query = """UPDATE fellows
            SET room_id = %d WHERE id = %d""" % (
                living_space[0], fellow_id)

            if self.person.db.update(query):
                print("{} is now accommodated in {}".format(
                    self.person.name, living_space[1]))
                return True
        else:
            return "No vacant living spaces. Check later to accommodate %s" % (
                self.person.name)

    def reallocate(self, args):
        """Reallocate an existing fellow to a new room

         Arguments:
                args (dict) Person ID and the living space to reallocate to

        Returns:
            Boolean     True if successful, otherwise False
        """
        fellow_id = int(args['<person_identifier>'])
        fellow = self.person.db.select_one(
            "SELECT * FROM fellows WHERE id = %d" % (fellow_id))
        if fellow:
            if fellow[2] == 'N':
                accommodate = raw_input(
                    """%s has opted out of amity accomodation. Would you like to accomodate the fellow?[y/n]""" % (fellow[1]))

                if accommodate.upper() == 'Y':
                    self.allocate_new_fellow(fellow, fellow_id, args)
                else:
                    print("%s has not been allocated into any room." %
                          format(fellow[1]))
            else:
                return self.reallocate_fellow(fellow, fellow_id, args)
        else:
            return "No fellow by the provided fellow id %d" % fellow_id

    def reallocate_fellow(self, fellow, fellow_id, args):
        """Reallocate an existing fellow to a new room

         Arguments:
                fellow  (List)  The fellow details
                fellow_id (Int) The unique ID of the fellow
                args (dict)     The request as received from the user

        Returns:
                Boolean     True if successful, otherwise False
        """
        if fellow[-1] is not None:
            old_room = self.person.db.select_one(
                """SELECT * FROM rooms
                WHERE id = %d AND type='L'""" % (fellow[-1]))
        else:
            old_room = [None, 'no prior office space']

        new_room_name = args['<new_room_name>']

        if old_room[1] != new_room_name:
            living = LivingSpace()
            new_room = living.space("L", new_room_name)
            if new_room:
                room_occupancy = living.occupancy("living", new_room[0])
                if len(room_occupancy) < living.room_space:
                    if living.allocate_room("fellow", fellow_id, new_room[0]):
                        return "%s is now residing in %s" % (
                            fellow[1], new_room_name)
                else:
                    return "%s is fully occupied." % (new_room_name)
            else:
                return "No living space by that name. Please try again"
        else:
            return "%s already belongs in %s" % (fellow[1], new_room_name)

    def allocate_new_fellow(self, fellow, fellow_id, args):
        """Reallocate an existing fellow to a new room

         Arguments:
                fellow  (List)  The fellow details
                fellow_id (Int) The unique ID of the fellow
                args (dict)     The request as received from the user

        Returns:
                Boolean     True if successful, otherwise False
        """
        new_room_name = args['<new_room_name>']
        living = LivingSpace()
        new_room = living.space("L", new_room_name)
        if new_room:
            room_occupancy = living.occupancy("living", new_room[0])
            if len(room_occupancy) < living.room_space:
                if living.allocate_room("fellow", fellow_id, new_room[0]):
                    return "%s is now residing in %s" % (
                        fellow[1], new_room_name)
            else:
                return "%s is fully occupied." % (new_room_name)
        else:
            return "No living space by that name. Please try again"
