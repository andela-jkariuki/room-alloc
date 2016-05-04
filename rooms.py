from pprint import pprint as pp
from db.dbManager import DBManager

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

class OfficeSpace(Rooms):
    room_space = 6

    def office_spaces(self):
        """
        Return a list of office spaces with a vacancy
        """
        db = DBManager('room_alloc.db')
        office_space = db.select("SELECT rooms.id, rooms.name, rooms.type, COUNT(*) AS occupants FROM rooms LEFT JOIN staff ON rooms.id = staff.room_id WHERE rooms.type='O' GROUP BY rooms.id")
        return office_space

class LivingSpace(Rooms):
    room_space = 4
    def __init__(self):
       self.db = DBManager('room_alloc.db')

    def living_spaces(self):
        """
        View a list of rooms with at least one vacancy
        """

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
        # rooms_occupancy = "SELECT * FROM rooms WHERE room_id = %d" % (room_id)
        # rooms_occupancy = self.db.select(rooms_occupancy)
        if isinstance(room_id, str):
            query = "SELECT * FROM rooms WHERE name = '%s'" % (room_id)
        elif isinstance(room_id, int):
            query = 'SELECT * FROM rooms where id = %d' % (room_id)
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
        update_room = "UPDATE fellows SET room_id = %d WHERE id = %d" % (room_id, fellow_id)

        if self.db.update(update_room):
            return True
        return False



