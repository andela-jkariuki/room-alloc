#!/usr/bin/env python
"""Room Classes"""
from db.dbManager import DBManager
from itertools import groupby


class Rooms:
    """Rooms class to handle behaviors common to both Offices and Living Spaces
    """
    def __init__(self, db_name=""):
        """Create instance of the database"""
        self.db = DBManager(db_name)

    def create_rooms(self, args):
        """Add new rooms to the rooms table

        Arguments:
                args (dict) Type of room space to add and list of all the new
                            rooms to be added.
        Returns:
            Boolean     True if the rooms were created.
                        False if the rooms were not created
        """
        room_type = 'L' if args['living'] else 'O'
        room_list = tuple((room, room_type) for room in args['<room_name>'])

        if self.db.run_many_queries("INSERT INTO rooms(name, type) VALUES (?, ?)", room_list):
            print('New rooms succesfully created')
            return True
        else:
            print('Duplicate entries: A room already exist with provided name')
            return False

    def room_allocations(self, args):
        """Print out a list of all room allocations

        Arguments:
                args (dict) Filename to print out the output (optional)
        """
        office_spaces = self.db.select("SELECT rooms.id, rooms.name, rooms.type, staff.name FROM rooms LEFT JOIN staff ON rooms.id = staff.room_id WHERE rooms.type='O'")

        living_spaces = self.db.select("SELECT rooms.id, rooms.name, rooms.type, fellows.name FROM rooms LEFT JOIN fellows ON rooms.id = fellows.room_id WHERE rooms.type='L'")

        office_space_allocations = {}
        living_space_allocations = {}

        for key, group in groupby(office_spaces, lambda x: x[0]):
            staff_occupancy = list(group)
            room_name = str(staff_occupancy[0][1])
            office_space_allocations[room_name] = []
            for staff in staff_occupancy:
                office_space_allocations[room_name].append(staff[-1])

        for key, group in groupby(living_spaces, lambda x: x[0]):
            staff_occupancy = list(group)
            room_name = str(staff_occupancy[0][1])
            living_space_allocations[room_name] = []
            for staff in staff_occupancy:
                living_space_allocations[room_name].append(staff[-1])

        div = max(max([len(", ".join(i)) for i in
                       office_space_allocations.values() if i[0] is not None]),
                  max([len(", ".join(i)) for i in
                      living_space_allocations.values() if i[0] is not None]))

        output = ''
        output += '\n' + '*' * div + "\nOFFICE SPACES\n" + '*' * div + "\n\n"
        if len(office_space_allocations) != 0:
            for name, occupants in office_space_allocations.iteritems():
                if occupants[0] is not None:
                    members = ", ".join(occupants)
                    output += name + "\n" + '-' * div + "\n" + members + "\n\n"
        else:
            output += "no office spaces are occupied"

        output += '\n' + '*' * div + "\nLIVING SPACES\n" + '*' * div + "\n\n"

        if len(living_space_allocations) != 0:
            for name, occupants in living_space_allocations.iteritems():
                if occupants[0] is not None:
                    members = ", ".join(occupants)
                    output += name + "\n" + '-' * div + "\n" + members + "\n\n"
        else:
            output += "no living spaces are occupied"

        print(output)

        if args['--o'] is not None:
            with open(args['--o'], 'wt') as f:
                f.write(output)
                print("Room allocations printed out to %s" % (args['--o']))

    def room_allocation(self, args):
        """Print out the rooom allocations for a particular room
        Arguments:
                args (dict) Room name
                            File name to print out room allocation(optional)
        """
        room_name = args['<room_name>']
        office_space = OfficeSpace()
        office = office_space.office_space(room_name)
        living_space = LivingSpace()
        living = living_space.living_space(room_name)

        if office:
            room_type = "OFFICE SPACE"
            occupants = office_space.office_space_occupancy(office[0])
        elif living:
            room_type = "LIVING SPACE"
            occupants = living_space.living_space_occupancy(living[0])
        else:
            print("No room exists in amity with that name. please try again")
            return
        occupants = ", ".join([str(i[1]) for i in occupants])
        div = len(occupants)

        output = '*' * div + "\n"
        output += room_name.upper() + " (" + room_type + ")\n"
        output += '*' * div + "\n"

        if len(occupants) == 0:
            output += "%s has no occupants" % (room_name)
        else:
            output += occupants
        print(output)

        if args['--o'] is not None:
            with open(room_name + ".txt", 'wt') as f:
                f.write(output)
                print("%s occupants printed out to %s" % (room_name, room_name + ".txt"))


class OfficeSpace(Rooms):
    """Class OfficeSpace contains the characteristics and behaviors of the
    office spaces at amity
    """
    room_space = 6

    def __init__(self, db_name=""):
        """Create instance of the database"""
        self.db = DBManager(db_name)

    def office_spaces(self):
        """Return a list of office spaces with a vacancy"""

        office_space = self.db.select("SELECT rooms.id, rooms.name, rooms.type, COUNT(*) AS occupants FROM rooms LEFT JOIN staff ON rooms.id = staff.room_id WHERE rooms.type='O' GROUP BY rooms.id")
        return office_space

    def office_space(self, office_id):
        """
        Get the details of an office space

        Arguments:
                office_id  The unique Id for the room

        Returns:
                List       The office space record in the database
        """
        if isinstance(office_id, str):
            query = "SELECT * FROM rooms WHERE name = '%s' AND type='O'" % (office_id)
        elif isinstance(office_id, int):
            query = "SELECT * FROM rooms where id = %d AND type='O'" % (office_id)
        office = self.db.select_one(query)
        if office:
            return office
        return False

    def office_space_occupancy(self, office_id):
        """
        Get the details of an office space

        Arguments:
                office_id The unique Id for the room
        Returns:
            list      Records of the staff occupying the office
        """
        room = self.office_space(office_id)
        if room:
            return self.db.select(
                "SELECT * FROM staff WHERE room_id = %d" % (room[0]))
        return False

    def allocate_room(self, staff_id, room_id):
        """Allocate an office space to a staff member

        Arguments:
                staff_id  The unique ID of the staff member
                room_id   The uniquer ID of the office space to be allocated

        Returns:
            Boolean   True if updated, otherwise False
        """
        update_room = "UPDATE staff SET room_id = %d WHERE id = %d" % (room_id, staff_id)

        if self.db.update(update_room):
            return True
        return False


class LivingSpace(Rooms):
    """Class LivingSpace contains the characteristics and behaviors of the
    living spaces at Amity
    """
    room_space = 4

    def __init__(self, db_name=""):
        """Create instance of the database"""
        self.db = DBManager(db_name)

    def living_spaces(self):
        """View a list of rooms with at least one vacancy"""

        living_spaces = self.db.select("SELECT rooms.id, rooms.name, rooms.type, COUNT(*) AS occupants FROM rooms LEFT JOIN fellows ON rooms.id = fellows.room_id WHERE rooms.type='L' GROUP BY rooms.id")
        return living_spaces

    def living_space(self, room_id):
        """
        Get the details of a living space

        Arguments:
                room_id The unique Id for the living space
        Returns:
            List    Record of a living space
        """
        if isinstance(room_id, str):
            query = "SELECT * FROM rooms WHERE name = '%s' AND type='L'" % (room_id)
        elif isinstance(room_id, int):
            query = "SELECT * FROM rooms where id = %d AND type='L'" % (room_id)
        room = self.db.select_one(query)
        if room:
            return room
        return False

    def living_space_occupancy(self, room_id):
        """
        Get the details of a living space

        Arguments:
                room_id The unique Id for the room
        Returns:
            list    Records of the fellows accoomodated in a room
        """
        room = self.living_space(room_id)
        if room:
            return self.db.select("SELECT * FROM fellows WHERE room_id = %d" % (room[0]))
        return False

    def allocate_room(self, fellow_id, room_id):
        """Allocate a living space to a fellow

        Arguments:
                fellow_id  The unique ID of the fellow
                room_id    The uniquer ID of the living space to be accomodated

        Returns:
                Boolean  True if updated, otherwise False
        """
        update_room = "UPDATE fellows SET room_id = %d, accomodation = 'Y' WHERE id = %d" % (room_id, fellow_id)

        if self.db.update(update_room):
            return True
        return False
