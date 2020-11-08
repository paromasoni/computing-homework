#Paroma Soni
#October 28, 2020
#Homework 2, Part 1

#Part 1: Lists
numbers = [22,90,0,-10,3,22,48]
print (len(numbers))
print (numbers[3])
print (numbers[1] + numbers [3])
print (numbers[-2])
print (numbers[6])
print (sum (numbers)/2)
sorted (numbers)
median = (numbers[3])
mean = (sum(numbers)/len(numbers))

if mean > median:
    print ("The mean is higher than the median")
else:
    print ("The median is higher than the mean")

#Part 2: Dictionaries
movie = {
    'title': 'Jaws',
    'year': '1975',
    'director': 'Steven Spielberg'
}
print("My favorite movie is", movie['title'], "which was released in", movie['year'], "and was directed by", movie['director'])

movie['budget'] = 9000000
movie ['revenue'] = 472000000
print (movie ['revenue'] - movie ['budget'])

if movie ['budget'] > movie ['revenue']:
    print ("That was a bad investment!")
elif movie ['revenue'] >= (movie ['budget'] * 5):
    print ("That was a great investment!")
else:
    print ("That was an okay investment.")

boroughs = {
'Manhattan': 1.6,
'Brooklyn': 2.6,
'Queens': 2.3,
'Bronx': 1.4,
'Staten Island': 0.47
}

print ("The population of Brooklyn is", boroughs['Brooklyn'], "million.")

boroughs_total = round (sum (boroughs.values()),3)
print ("The combined population of all boroughs is", boroughs_total, "million")

Manhattan_percent = (boroughs['Manhattan']/boroughs_total) * 100
print (round(Manhattan_percent, 2), "% of NYC lives in Manhattan.")
