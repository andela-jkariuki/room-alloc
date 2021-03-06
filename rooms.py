#!/usr/bin/env python
"""Room Classes"""
from db.dbManager import DBManager
from itertools import groupby


class Rooms:
    """Rooms class to handle behaviors common to both Offices and Living Spaces
    """
    room_space = 4

    def __init__(self):
        """Create instance of the database"""
        self.db = DBManager()

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

        if self.db.run_many_queries("""INSERT INTO rooms(name, type)
             VALUES (?, ?)""", room_list):
            return 'New rooms succesfully created'
        else:
            raise ValueError(
                'Duplicate entries: A room already exist with provided name')

    def room_allocations(self, args):
        """Print out a list of all room allocations

        Arguments:
                args (dict) Filename to print out the output (optional)
        """
        office_spaces = self.db.select(
            """SELECT rooms.id, rooms.name, rooms.type, staff.name
            FROM rooms
            LEFT JOIN staff ON rooms.id = staff.room_id
            WHERE rooms.type='O'""")

        living_spaces = self.db.select(
            """SELECT rooms.id, rooms.name, rooms.type, fellows.name
            FROM rooms
            LEFT JOIN fellows ON rooms.id = fellows.room_id
            WHERE rooms.type='L'""")

        office_space_allocations = {}
        living_space_allocations = {}

        for _, group in groupby(office_spaces, lambda x: x[0]):
            staff_occupancy = list(group)
            room_name = str(staff_occupancy[0][1])
            office_space_allocations[room_name] = []
            for staff in staff_occupancy:
                office_space_allocations[room_name].append(staff[-1])

        for _, group in groupby(living_spaces, lambda x: x[0]):
            staff_occupancy = list(group)
            room_name = str(staff_occupancy[0][1])
            living_space_allocations[room_name] = []
            for staff in staff_occupancy:
                living_space_allocations[room_name].append(staff[-1])

        try:
            office_space = [len(", ".join(i)) for i
                            in office_space_allocations.values()
                            if i[0] is not None]

            living_space = [len(", ".join(i)) for i
                            in living_space_allocations.values()
                            if i[0] is not None]

            div = max(max(office_space),
                      max(living_space),
                      len('OFFICE SPACES'),
                      len('LIVING SPACES'))
        except ValueError:
            div = 30

        output = ''
        output += '\n' + '*' * div + "\nOFFICE SPACES\n" + '*' * div + "\n\n"
        if len(office_space) != 0:
            for name, occupants in office_space_allocations.iteritems():
                if occupants[0] is not None:
                    members = ", ".join(occupants)
                    output += name + "\n" + '-' * div + "\n" + members + "\n\n"
        else:
            output += "no office spaces are occupied"

        output += '\n' + '*' * div + "\nLIVING SPACES\n" + '*' * div + "\n\n"

        if len(living_space) != 0:
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

        rooms = Rooms()
        office = rooms.space("O", room_name)
        living = rooms.space("L", room_name)

        if office:
            room_type = "OFFICE SPACE"
            occupants = rooms.occupancy("office", office[0])
        elif living:
            room_type = "LIVING SPACE"
            occupants = rooms.occupancy("living", living[0])
        else:
            return "No room exists in amity with that name. please try again"

        occupants = ", ".join([str(i[1]) for i in occupants])
        div = max([len(occupants), len(room_type)])

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
                print("%s occupants printed out to %s" %
                      (room_name, room_name + ".txt"))

    def allocate_room(self, person_type, person_id, room_id):
        """Allocate a living space to a fellow

        Arguments:
                person_type     Type of person to allocate room
                                (fellow or staff)
                fellow_id       Unique ID of the fellow or Staff member
                room_id         Unique ID of the room space to be allocated

        Returns:
                Boolean  True if updated, otherwise False
        """
        if person_type == "fellow":
            update_room = """UPDATE fellows
            SET room_id = %d, accomodation = 'Y'
            WHERE id = %d""" % (room_id, person_id)
        elif person_type == "staff":
            update_room = """UPDATE staff
            SET room_id = %d
            WHERE id = %d""" % (room_id, person_id)

        if self.rooms.db.update(update_room):
            return True

    def occupancy(self, space_type, room_id):
        """
        Get the details of a living space or office space

        Arguments:
                space_type  The type of space [living or office]
                room_id     The unique Id for the room
        Returns:
            list    Records of the people allocated to the room
        """
        if space_type == "living":
            room = self.space("L", room_id)
            if room:
                return self.db.select("""SELECT * FROM fellows
                    WHERE room_id = %d""" % (room[0]))
        elif space_type == "office":
            room = self.space("O", room_id)
            if room:
                return self.db.select(
                    """SELECT * FROM staff
                    WHERE room_id = %d""" % (room[0]))

    def vacancies(self, space_type):
        if space_type == "living":
            return self.db.select(
                """SELECT rooms.id, rooms.name, rooms.type,
                COUNT(*) AS occupants
                FROM rooms
                LEFT JOIN fellows ON rooms.id = fellows.room_id
                WHERE rooms.type='L' GROUP BY rooms.id
                HAVING occupants < %d """ % (LivingSpace.room_space))
        elif space_type == "office":
            return self.db.select(
                """SELECT rooms.id, rooms.name, rooms.type,
                COUNT(*) AS occupants
                FROM rooms
                LEFT JOIN staff ON rooms.id = staff.room_id
                WHERE rooms.type='O' GROUP BY rooms.id
                HAVING occupants < %d """ % (OfficeSpace.room_space))

    def space(self, space_type, room_id):
        """
        Get the details of a living space

        Arguments:
                room_id The unique Id for the living space
        Returns:
            List    Record of a living space
        """
        if isinstance(room_id, str):
            query = "SELECT * FROM rooms WHERE name = '%s' AND type='%s'" % (
                room_id, space_type)
        elif isinstance(room_id, int):
            query = "SELECT * FROM rooms where id = %d AND type='%s'" % (
                room_id, space_type)
        room = self.db.select_one(query)
        if room:
            return room
        return False


class OfficeSpace(Rooms):
    """Class OfficeSpace contains the characteristics and behaviors of the
    office spaces at amity
    """
    room_space = 6

    def __init__(self):
        """Create instance of the database"""
        self.rooms = Rooms()
        self.db = DBManager()


class LivingSpace(Rooms):
    """Class LivingSpace contains the characteristics and behaviors of the
    living spaces at Amity
    """
    def __init__(self):
        """Create instance of the database"""
        self.rooms = Rooms()
        self.db = DBManager()
