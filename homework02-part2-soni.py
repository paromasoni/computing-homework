#Paroma Soni
#October 28, 2020
#Homework 2, Part 2

#Part 2: Lists
countries = ['India', 'Mexico', 'Latvia', 'Jordan', 'Egypt', 'Zambia', 'Peru']
for country in countries:
    print (country)

countries.sort()
print (countries) #Just to check if it sorted correctly

print (countries[0])
print (countries[-2])

countries.remove('Latvia')

for country in countries:
    print (country.upper())

#Part 2: Dicitionaries
tree = {
    'name': 'Treaty Tree',
    'species': 'White milkwood',
    'age': 500,
    'location_name': 'Cape Town, South Africa',
    'latitude': -33.93,
    'longitude': 18.45
}

print (tree['name'], "is a", tree ['age'], "year-old tree that is in", tree['location_name'])

if tree ['latitude'] < 40.72:
    print ("The", tree['name'], "in", tree ['location_name'], "is south of NYC.")
else:
    print ("The", tree['name'], "in", tree ['location_name'], "is north of NYC.")

age = input("How old are you?")
age = int(age)

if age > tree ['age']:
    diff = age - tree['age']
    print ("You are", diff, "years older than", tree['name'])
else:
    diff = tree['age'] - age
    print ("You are", diff, "years younger than", tree['name'])

#Part 2: Lists of dictionaries

places = [ 
    {'city_name': 'Moscow', 'latitude': 55.76, 'longitude': 37.62},
    {'city_name': 'Tehran', 'latitude': 35.79, 'longitude': 51.39},
    {'city_name': 'Falkland Islands', 'latitude': -51.79, 'longitude': -59.54},
    {'city_name': 'Seoul', 'latitude': 37.57, 'longitude': 126.97},
    {'city_name': 'Santiago', 'latitude': -33.45, 'longitude': -70.67}
]

for place in places:
    print (place['city_name'])
    if place['latitude'] > 0:
        print ("It's above the equator!")
    elif place['latitude'] < 0: 
        print ("It's below the equator!")
    elif place['latitude'] == 0:
        print ("It's exactly on the equator!")
    if place['city_name'] == 'Falkland Islands':
        print ("The Falkland Islands are a biogeographical part of the mild Antarctic zone.")

for place in places:
    if place['latitude'] > tree['latitude']:
        print (place['city_name'], "is north of the", tree['name'])
    else:
        print (place['city_name'], "is south of the", tree['name'])

