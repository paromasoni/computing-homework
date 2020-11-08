# Paroma Soni
# October 26, 2020
# Homework 1

birthyear = input ("What year were you born?")
birthyear = int(birthyear)
if birthyear > 2020:
    print ("The world is not yet ready for time travel!")
    birthyear = input("What year were you really born?")
    birthyear = int(birthyear)
age = (2020 - birthyear)

print ("You are approximately", age, "years old")

# The human heart beats about 100,000 times in one day and about 35 million times in a year.
heartbeat = (age * 35000000)
heartbeat = (round(heartbeat / 1000000))
print ("Your heart has beaten", heartbeat, "million times")

# The average heart rate of a 220-ton blue whale is 11 beats per minute.
whale_heartbeat = (age * 11 * 60 * 24 * 365)
whale_heartbeat = (round(whale_heartbeat / 1000000))
print ("A blue whale's heart has beaten", whale_heartbeat, "million times during your lifetime.")

# A rabbit's heart beats between 140-180 times per minute. (Average is 160 bpm)
rabbit_heartbeat = (age * 160 * 60 * 24 * 365)
rabbit_heartbeat = (round(rabbit_heartbeat / 1000000))
print ("A rabbit's heart has beaten", rabbit_heartbeat, "million times during your lifetime.")

# 1 Earth year = 0.6152 Venus years
# 1 Neptune year = 164.8 Earth years

venus_age = (round(age * 0.6152, 1))
print ("You are around", venus_age, "years old on Venus.")

neptune_age = (round(age / 164.8, 1 ))
print ("You are around", neptune_age, "years old on Neptune.")

if age == 25:
    print ("We're the same age!")
if age > 25: 
    diff = (age - 25)
    print ("You are older than me by", diff, "years!")
elif age < 25:
    diff = (25 - age)
    print ("You are younger than me by", diff, "years!")

if (age % 2) == 0:
    print ("You were born in an even year.")
else:
    print ("You were born in an odd year.")

democrats = 0
if birthyear == 1960:
    democrats = democrats + 5
    print ("Eisenhower was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
# range has to be written as in range (1,5) but the last mumber is not included. this would be 1,2,3,4 only in the list.
if birthyear in range(1961,1963):
    democrats = democrats + 5
    print ("John. F. Kennedy was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1963 and birthyear <= 1968:
    democrats = democrats + 4
    print ("Lyndon B. Johnson was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1969 and birthyear <= 1973:
    democrats = democrats + 3
    print ("Richard M. Nixon was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1974 and birthyear <= 1976:
    democrats = democrats + 3
    print ("Gerald Ford was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1977 and birthyear <= 1980:
    democrats = democrats + 3
    print ("Jimmy Carter was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1981 and birthyear <= 1988:
    democrats = democrats + 2
    print ("Ronald Reagan was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1989 and birthyear <= 1992:
    democrats = democrats + 2
    print ("George Bush was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 1993 and birthyear <= 2000:
    democrats = democrats + 2
    print ("Bill Clinton was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 2001 and birthyear <= 2008:
    democrats = democrats + 1
    print ("George W. Bush was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 2009 and birthyear <= 2016:
    democrats = democrats + 1
    print ("Barack Obama was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")
if birthyear >= 2017 and birthyear <= 2020:
    democrats = democrats + 0
    print ("Donald Trump was in office when you were born.")
    print ("There has been a Democrat in office", democrats, "times since you were born.")