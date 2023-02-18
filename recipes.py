boodschappenlijst = []
while True:
    boodschap = input('Wat wil je hebben?\n')

    if boodschap == '':
        print("Je hebt niks ingevuld.")
        break
    elif boodschap in boodschappenlijst:
        print('Dit item heb je al op de lijst staan')
    else:
        boodschappenlijst.append(boodschap)

with open('boodschappenlijst.txt', 'w+') as file:
    for item in boodschappenlijst:
        file.write(item + '\n')
