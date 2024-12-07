import random

dir = "./words.txt"


def open_text(dir):
  
  file = open(dir,'r',encoding='UTF-8')
  content = file.readlines()

  return content


def get_word(content):
  word_number= random.randint(0,len(content))
  word = content[word_number].strip()


  return word


count_hit = count_miss = 0
conteudo = open_text(dir)
palavra = get_word(conteudo)
palavra = palavra.upper()
index = ["_"]*len(palavra)
letters_used = []

print("Jogo da Forca!!!")
print(''.join(index))

while count_miss < 6:
  dont_hit = True
  letter_of_choice = input("Digite uma letra: ").upper()
  for i in range (len(palavra)):
    if ((letter_of_choice == palavra[i]) and(letter_of_choice not in letters_used)):
      count_hit +=1
      dont_hit = False
      index[i] = letter_of_choice
      
  if (count_hit ==len(palavra)):
    print("Parabéns!! Acertou!!")
    print(f"A palavra era: {palavra}")
    break
  print(''.join(index))
  if dont_hit:
    count_miss +=1
  if dont_hit and(count_miss <= 5):
    print(f'Você errou pela {count_miss}a vez. Tente de novo!')
  elif dont_hit and (count_miss==6):
    print(f'Acabaram as chances!! A palavra era {palavra}!')
    break
  
  letters_used.append(letter_of_choice)




    
