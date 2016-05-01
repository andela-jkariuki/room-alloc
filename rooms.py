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


