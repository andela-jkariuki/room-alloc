from db.dbManager import DBManager
import sqlite3 as lite

class Person:
    def __init__(self, first_name, last_name):
        self.name = first_name + ' ' + last_name

class Fellow(Person):
    def __init__(self, args):
        self.person = Person(args['<first_name>'], args['<last_name>'])
        self.accomodation  = 'Y' if args['--wants_accomodation'].lower() == 'y' else 'N'

        self.db = DBManager('room_alloc.db')
        self.add_fellow()

    def add_fellow(self):
        new_fellow_query = "INSERT INTO fellows(name, accomodation) VALUES('{name}', '{accomodation}')".format(name = self.person.name, accomodation =  self.accomodation)
        print(new_fellow_query)
        try:
            with self.db.connection
                new_fellow = self.db.cursor.execute(new_fellow_query)
                print("New fellow succesfully added to the system")
        except lite.IntegrityError:
            print("Error adding new fellow. Please try again")

