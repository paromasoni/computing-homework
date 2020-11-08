#Paroma Soni
#Nov 1, 2020
#Homework 03 Part 1


#Documentation URL = https://pokeapi.co/docs/v2#pokemon

import requests

url = "https://pokeapi.co/api/v2/pokemon/55"
response = requests.get(url, allow_redirects=True)

data_55 = response.json()

#print (data_55.keys())
print ("The pokemon with ID 55 is named", data_55['name'])
print ("Its height is", data_55['height'], "decimeters")

print ("--------------------")

version_url = "https://pokeapi.co/api/v2/version/?offset=0&limit=34"
response = requests.get(version_url, allow_redirects=True)

version_data = response.json()

version_count = version_data['results']
print ("There are", len(version_count), "versions of Pokemon.")

print ("--------------------")

type_url = "https://pokeapi.co/api/v2/type/electric/"

response = requests.get(type_url, allow_redirects=True)
type_data = response.json()

#print (type_data.keys())
print ("The names of all electric Pokemon are:")
for pokemonnames in type_data['pokemon']:
  print (pokemonnames['pokemon']['name'])


print ("--------------------")

for pokemon_langs in type_data['names']:
  langs = pokemon_langs ['language']
  if langs['name'] == 'ko':
    print ("Electric-type pokemon are called", pokemon_langs['name'], "in Korean.")

print ("--------------------")

speedurl = "https://pokeapi.co/api/v2/pokemon/eevee/"

response = requests.get(speedurl, allow_redirects=True)

speed_eevee_data = response.json()

speedurl2 = "https://pokeapi.co/api/v2/pokemon/pikachu/"

response = requests.get(speedurl2, allow_redirects=True)

speed_pikachu_data = response.json()

#print (speed_eevee_data.keys())
#print (speed_eevee_data['name'])
for speed1 in (speed_eevee_data['stats']):
  speed2 = speed1['stat']
  if (speed2 ['name']) == 'speed':
    eevee_speed = speed1['base_stat']
    #print (eevee_speed)

for speed_a in (speed_pikachu_data['stats']):
  speed_b = speed_a['stat']
  if (speed_b ['name']) == 'speed':
    pikachu_speed = speed_a['base_stat'] 
    #print (pikachu_speed)

if eevee_speed > pikachu_speed:
  print (f'Eevee has a faster speed of {eevee_speed} compared to Pikachu who has {pikachu_speed}')
else:
  print (f'Pikachu has a faster speed of {pikachu_speed} compared to Eevee who has {eevee_speed}')
    
    #print (speed_eevee_data['name'], speed1['base_stat'], speed2['name'])
  #for speed3 in speed2['stat']:
    #print (speed3 ['name'])

#print (data.keys())
#print (data['results'])
#for pokemon_info in data['results']:
   # pokemon_name = pokemon_info ['name']
 #  pokemon_url = pokemon_info ['url']

#response = requests.get(pokemon_url, allow_redirects=True)

#pokemon_data = response.json()
#for pokemon in pokemon_data:
 #   print (pokemon[1])

#print (pokemon_data)
#for pokemon in pokemon_data:
  #  print (pokemon)
    #if 'id' == 55:
    #    print (pokemon['name'])
    #    print (pokemon['height'])