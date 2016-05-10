from rooms import Rooms
from people import Fellow, Staff
from db.dbManager import DBManager


class Data:
    db_name = 'test.db'

    def __init__(self):
        """Create a test database"""
        self.db = DBManager()

    def create_living_spaces(self, room_names):
        rooms = Rooms()
        arguments = {'<room_name>': room_names,
                     'living': True,
                     'office': False}

        return rooms.create_rooms(arguments)

    def create_office_spaces(self, room_names):
        rooms = Rooms()
        arguments = {'<room_name>': room_names,
                     'living': False,
                     'office': True}

        return rooms.create_rooms(arguments)

    def fetch_data(self, table_name, single_record=True):
        if single_record:
            return self.db.select_one("SELECT * FROM %s" % (table_name))
        else:
            return self.db.select("SELECT * FROM  %s" % (table_name))

    def create_fellow(self, first_name, last_name, accomodation):
        arguments = {'<first_name>': first_name,
                     '<last_name>': last_name,
                     '--a': accomodation}
        fellow = Fellow()
        return fellow.add_fellow(arguments)

    def create_staff(self, first_name, last_name):
        arguments = {'<first_name>': first_name,
                     '<last_name>': last_name}
        staff = Staff()
        return staff.add_staff(arguments)
