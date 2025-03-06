seasons = ['Spring  ', 'Summer ', 'Fall', 'Winter', ' ', '','\nalo']
strippedSeasons = [x.strip() for x in seasons if x.strip()]

#test
print(strippedSeasons)
listStuff = list(enumerate(strippedSeasons))

for index,line in listStuff:
    print(f"Line Number: {index}, Line String: {line}")
