cpf_number = input("Insira um número de CPF válido: ")

if (len(cpf_number)<14 or len(cpf_number)>14):
  print("Número de CPF em formato inválido!")
elif (cpf_number[3] !='.' or cpf_number[7] !='.'):
  print("Número de CPF em formato inválido!")
elif (cpf_number[11] !='-'):
  print("Número de CPF em formato inválido!")
else:
  count_numbers = 0
  for i in range(14):
    if ((i !=3 and i !=7) and i != 11):
      try:
        int(cpf_number[i])
        count_numbers +=1
      except ValueError:
        print("Número de CPF Inválido!")
  if (count_numbers==11):
    print("CPF Válido!!")
    
