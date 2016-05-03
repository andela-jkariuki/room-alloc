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

    def living_spaces(self):
        """
        View a list of rooms with at least one vacancy
        """
        db = DBManager('room_alloc.db')
        living_spaces = db.select("SELECT rooms.id, rooms.name, rooms.type, COUNT(*) AS occupants FROM rooms LEFT JOIN fellows ON rooms.id = fellows.room_id WHERE rooms.type='L' GROUP BY rooms.id")
        return living_spaces


