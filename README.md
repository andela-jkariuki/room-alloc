# room-alloc

```
room-alloc is Room allocation system for Amity, an Andela facility in Nigeria.
```

Room-alloc enables a user to manage the living and office spaces by allocating the fellows and staff members respectively.

Amity works under the following constraints

1. An office can occupy a maximum of 6 people.
2. A living space can inhabit a maximum of 4 people.
3. A person to be allocated could be a fellow or staff.
4. Staff cannot be allocated living spaces.
5. Fellows have a choice to choose a living space or not.

## Installation

To set up room-alloc, make sure that you have python and pip installed on your workstation.

I highly recommend that you use [Virtualenvwrapper](http://virtualenvwrapper.readthedocs.io/en/latest/) for an isolated working environment.

Proceed to clone the repo into your projects folder

```bash
$ git@github.com:andela-jkariuki/room-alloc.git

$ cd room-alloc
```

Create a virtual environment to work from using the Virtualenvwrapper's `mkvirtualenv` command

```bash
$ mkvirtualenv room-alloc
```

This will automagically activate the virtual env. You can now proceed to install our modules from the `requirements.txt` file

```bash
 $ pip install -r requirements.txt
```

Confirm your installed packages
```bash
$ pip list
```

## Usage

**1. Create Rooms**

To create a living or office space, follow the following docopt pattern
```bash
Usage: create_rooms (living|office) <room_name>...
```

Creating living spaces
```bash
create_rooms living woodwing bluewing redwing
```

Creating office spaces
```bash
create_rooms office camelot midgar
```

**2. Add Person**

You can either add a staff member or a fellow with the `add_person` command.
A fellow can either opt in or out of the Amity accomodation plan.
The docopt patter is as follows
```bash
Usage: add_person <first_name> <last_name> (fellow|staff) [--a=n]
```

Add a staff member
```bash
add_person Joshua Mwaniki staff
```

Add a fellow that opts in to the andela accommodation
```bash
add_person Amos Omondi fellow --a=y
```

Add a fellow that opts out of the andela accommodation
```bash
add_person Amos Omondi fellow
```

**3. Reallocate a person**

You can reallocate a person from one space (living or office) to another using the following pattern
```bash
reallocate_person (fellow|staff) <person_identifier> <new_room_name>
```

Reallocate a fellow with id 1 from woodwing to bluewing

```bash
reallocate_person fellow 1 bluewing
```
Reallocate a staff with id 10 from midgar to camelot

```bash
reallocate_person staff 10 camelot
```

**4. Print Stuff**

The print methods allow you to print out room allocations for all rooms, one room or list of unallocated people.
You can also specify an optional `--o` parameter to write the data to a file.

**Print room allocations**

Print out a list of all room allocations at amity
```bash
print_allocations --o=y
```
**Print unallocated**

Print out a list of all unallocated people (staff members and fellows)
```bash
print_unallocated --o=y
```

**Print out room details**

Print out a list of the allocations of a particular room at amity
```bash
print_room camelot --o=y
```

## Contributing

Contributions are **welcome** and will be fully **credited**.

We accept contributions via Pull Requests on [Github](https://github.com/andela-jkariuki/room-alloc).

## Security

If you discover any security related issues, please email me at [John Kariuki](mailto:john.kariuki@andela.com) or create an issue.

## Credits

[John kariuki](https://github.com/andela-jkariuki)

## License

### The MIT License (MIT)

Copyright (c) 2016 John kariuki <john.kariuki@andela.com>

> Permission is hereby granted, free of charge, to any person obtaining a copy
> of this software and associated documentation files (the "Software"), to deal
> in the Software without restriction, including without limitation the rights
> to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
> copies of the Software, and to permit persons to whom the Software is
> furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in
> all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
> IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
> FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
> AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
> LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
> OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
> THE SOFTWARE.
