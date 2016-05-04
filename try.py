from itertools import groupby

offices = [(5, u'oculus', u'O', None),
 (6, u'valhala', u'O', u'Biggie Smallz'),
 (6, u'valhala', u'O', u'Gibss Softskills'),
 (6, u'valhala', u'O', u'Herbert M'),
 (7, u'horgwats', u'O', u'Clarine Muthoni'),
 (8, u'midgar', u'O', u'Nyambura Kihoro'),
 (8, u'midgar', u'O', u'Tupac Shakur'),
 (9, u'narnia', u'O', None)
 ]

office_space_allocations = {}

for key, group in groupby(offices, lambda x: x[0]):
    staff_occupancy = list(group)
    room_name = str(staff_occupancy[0][1])
    office_space_allocations[room_name] = []
    for staff in staff_occupancy:
        office_space_allocations[room_name].append(staff[-1])

print(office_space_allocations)
