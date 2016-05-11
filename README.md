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

##Installation

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

