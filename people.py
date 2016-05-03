from db.dbManager import DBManager

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

        fellow_id = self.db.run_single_query(new_fellow_query)

        if fellow_id :
            print("New fellow succesfully added. Fellow ID is %d" % (fellow_id))
            if self.accomodation == 'Y':
                print('Searching for accomodation for the fellow...')
                self.accomodate_fellow(fellow_id)
            else:
                print('accomodation not provided for fellow.')
        else:
            print("Error adding new fellow. Please try again")

    def accomodate_fellow(self, fellow_id):
        print('we be up in here accomodating the fellow')


