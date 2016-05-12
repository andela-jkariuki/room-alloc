#!/usr/bin/env python
"""
RoomLoc

This provides guidance on how to handle room allocations for office and living
spaces in Amity

Usage:
    room_loc create_rooms (living|office) <room_name>...
    room_loc add_person <first_name> <last_name> (fellow|staff) [--a=n]
    room_loc reallocate_person (fellow|staff) <person_identifier> <new_room_name>
    room_loc print_allocations [--o=allocations.txt]
    room_loc print_room <room_name> [--o=y]
    room_loc load_people
    room_loc (-i | --interactive)
    room_loc (-h | --help | --version)
Options:
    -i, --interactive  Interactive Mode
    -h, --help  Show this screen and exit.
"""

import sys
import cmd
from docopt import docopt, DocoptExit
from rooms import Rooms
from people import Person, Staff, Fellow


def pass_opt(func):
    """
    This decorator is used to simplify the try/except block and pass the result
    of the docopt parsing to the called action.
    """
    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as e:
            # The DocoptExit is thrown when the args do not match.
            # We print a message to the user and the usage block.

            print('Invalid Command!')
            print(e)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here.

            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Amity (cmd.Cmd):
    intro = """Welcome to my Amity!
    (type help for a list of commands.)"""

    prompt = '(room_loc) '
    file = None

    @pass_opt
    def do_create_rooms(self, args):
        """Usage: create_rooms (living|office) <room_name>..."""
        print(Rooms().create_rooms(args))

    @pass_opt
    def do_add_person(self, args):
        """Usage: add_person <first_name> <last_name> (fellow|staff) [--a=n]"""
        if args['fellow']:
            fellow = Fellow()
            print(fellow.add_fellow(args))
        else:
            staff = Staff()
            print(staff.add_staff(args))

    @pass_opt
    def do_reallocate_person(self, args):
        """Usage: reallocate_person (fellow|staff) <person_identifier> <new_room_name>"""
        if args['fellow']:
            print(Fellow().reallocate(args))
        else:
            print(Staff().reallocate(args))

    @pass_opt
    def do_print_allocations(self, args):
        """Usage: print_allocations [--o=allocations.txt]"""
        rooms = Rooms()
        print(rooms.room_allocations(args))

    @pass_opt
    def do_print_room(self, args):
        """Usage: print_room <room_name> [--o=y]"""
        rooms = Rooms()
        print(rooms.room_allocation(args))

    @pass_opt
    def do_print_unallocated(self, args):
        """Usage: print_unallocated [--o=y]"""
        person = Person()
        person.unallocated(args)

    @pass_opt
    def do_load_people(self, args):
        """Usage: load_people"""
        people = Person()
        people.allocate_from_file(args)

    def do_quit(self, arg):
        """Quits out of Interactive Mode."""
        print('Good Bye!')
        exit()

opt = docopt(__doc__, sys.argv[1:])

if opt['--interactive']:
    Amity().cmdloop()

print(opt)
