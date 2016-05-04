from pprint import pprint as pp
from db.dbManager import DBManager
from itertools import groupby

class Rooms:
    def create_rooms(self, args):
        """Add new rooms to the rooms table

        Args:
            args -  A dictionary that consists of the type of room space
                    and the list of all the new rooms to be added.
        """

        room_type = 'L' if args['living'] else 'O'
        room_list = tuple((room, room_type) for room in args['<room_name>'])

        db = DBManager('room_alloc.db')

        if db.run_many_queries("INSERT INTO rooms(name, type) VALUES (?, ?)", room_list):
            print 'New rooms succesfully created'
        else:
            return 'Duplicate entries: A room already exist with provided name'

    def room_allocations(self, args):
        """Print out a list of all room allocations"""
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

        divider = max(max([len(", ".join(i)) for i \
            in office_space_allocations.values() if i[0] is not None]),
            max([len(", ".join(i)) for i \
            in living_space_allocations.values() if i[0] is not None]))

        print '\n', '*' * divider, "\nOFFICE SPACES\n", '*' * divider, "\n"
        if len(office_space_allocations) != 0:
            for name, occupants in office_space_allocations.iteritems():
                if occupants[0] is not None:
                    members = ", ".join(occupants)
                    print name
                    print '-' * divider
                    print members
                    print ""
        else:
            print "no office spaces are occupied"

        print '\n', '*' * divider, "\nLIVING SPACES\n", '*' * divider,"\n"

        if len(living_space_allocations) != 0:
            for name, occupants in living_space_allocations.iteritems():
                if occupants[0] is not None:
                    members = ", ".join(occupants)
                    print name
                    print '-' * divider
                    print members
                    print ""
        else:
            print "no living spaces are occupied"

class OfficeSpace(Rooms):
    room_space = 6

    def __init__(self):
       self.db = DBManager('room_alloc.db')

    def office_spaces(self):
        """
        Return a list of office spaces with a vacancy
        """

        office_space = self.db.select("SELECT rooms.id, rooms.name, rooms.type, COUNT(*) AS occupants FROM rooms LEFT JOIN staff ON rooms.id = staff.room_id WHERE rooms.type='O' GROUP BY rooms.id")
        return office_space

    def office_space(self, office_id):
        """
        Get the details of an office space

        Args:
            office_id     The unique Id for the room
        Returns:
            list        The office_id, name and room_type
        """
        if isinstance(office_id, str):
            query = "SELECT * FROM rooms WHERE name = '%s' AND type='O'" % (office_id)
        elif isinstance(office_id, int):
            query = "SELECT * FROM rooms where id = %d AND type='O'" % (office_id)
        office = self.db.select_one(query)
        if office:
            return office
        return False

    def allocate_room(self, staff_id, room_id):
        update_room = "UPDATE staff SET room_id = %d WHERE id = %d" % (room_id, staff_id)

        if self.db.update(update_room):
            return True
        return False

    def office_space_occupancy(self, office_id):
        """
        Get the details of an office space

        Args:
            office_id     The unique Id for the room
        Returns:
            list
        """
        room = self.office_space(office_id)
        if room:
            return self.db.select( "SELECT * FROM staff WHERE room_id = %d" % (room[0]))
        return False

class LivingSpace(Rooms):

    room_space = 4

    def __init__(self):
       self.db = DBManager('room_alloc.db')

    def living_spaces(self):
        """View a list of rooms with at least one vacancy"""

        living_spaces = self.db.select("SELECT rooms.id, rooms.name, rooms.type, COUNT(*) AS occupants FROM rooms LEFT JOIN fellows ON rooms.id = fellows.room_id WHERE rooms.type='L' GROUP BY rooms.id")
        return living_spaces

    def living_space(self, room_id):
        """
        Get the details of a living space

        Args:
            room_id     The unique Id for the room
        Returns:
            list        The room_id, name and room_type
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

        Args:
            room_id     The unique Id for the room
        Returns:
            list
        """
        room = self.living_space(room_id)
        if room:
            return self.db.select( "SELECT * FROM fellows WHERE room_id = %d" % (room[0]))
        return False

    def allocate_room(self, fellow_id, room_id):
        update_room = "UPDATE fellows SET room_id = %d, accomodation = 'Y' WHERE id = %d" % (room_id, fellow_id)

        if self.db.update(update_room):
            return True
        return False



