from rooms import Rooms
from db.dbManager import DBManager


class Data:
    def __init__(self):
        """Create a test database"""
        self.db = DBManager('test.db')

    def create_living_spaces(self):
        rooms = Rooms('test.db')
        arguments = {'<room_name>': ['woodwing', 'westwing', 'eastwing'],
                     'living': True,
                     'office': False}

        return rooms.create_rooms(arguments)

    def fetch_data(self, table_name, single_record=True):
        if single_record:
            return self.db.select_one("SELECT * FROM %s" % (table_name))
        else:
            return self.db.select("SELECT * FROM  %s" % (table_name))
