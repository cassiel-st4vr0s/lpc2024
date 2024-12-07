def pegar_numero ():
  need_integer = True
  while need_integer:
    try:
      number_of_choice = int(input("Número inteiro de 0 a 99: "))
      break
    except ValueError:
      need_integer = True
  return number_of_choice


def pegar_unidade (number):
  unidades = [" ","um","dois","três","quatro","cinco","seis","sete","oito","nove","dez"]
  return unidades[number]


def pegar_dezenas (number):
  if (number <10):
    return pegar_unidade(number)
  if (number < 20):
    dez_especial = ["","onze","doze","treze","quatorze","qunze","dezesseis","dezessete","dezoito","dezenove"]
    return dez_especial[number-10]
  else:
    dezenas = ["","vinte","trinta","quarenta","cinquenta","sessenta","setenta","oitenta","noventa"]
    return dezenas[(number//10)-1]
  

number = pegar_numero()
if (number == 0):
  print("Número por extenso: zero")

elif (number > 10):
  if (number < 20):
    print(f'Número por extenso: {pegar_dezenas(number)} ')
  elif (number >20):
    print(f'Número por extenso: {pegar_dezenas(number)} e {pegar_unidade(number%10)}')

else:
  print(f'Número por extenso: {pegar_unidade(number)}')
