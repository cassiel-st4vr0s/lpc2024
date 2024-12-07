import random

rolls = []
count_1 = count_2 = count_3 = count_4 = count_5 = count_6 = 0

for i in range(100):
  this_roll = random.randint(1,6)
  rolls.append(this_roll)

for i in range(1,7,1):
  for j in range(len(rolls)):
    if (i==rolls[j] and i==1):
      count_1 +=1
    elif (i==rolls[j] and i==2):
      count_2 +=1
    elif (i==rolls[j] and i==3):
      count_3 +=1
    elif (i==rolls[j] and i==4):
      count_4 +=1
    elif (i==rolls[j] and i==5):
      count_5 +=1
    elif (i==rolls[j] and i==6):
      count_6+=1

    
count = [
         count_1,count_2,count_3,
         count_4,count_5,count_6,
        ]

print(f'Número de vezes que cada lado caiu pra cima:\n')

for i in range(len(count)):
  print(f'{i+1}: {count[i]} vezes\n')
