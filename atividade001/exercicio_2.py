word = input("Digite uma sequência de caracteres: ")
word_cleaned= word.replace(" ","")
count = 0
word_reversed = word_cleaned[::-1]

for i in range(len(word_cleaned)):
  if (word_cleaned[i]==word_reversed[i]):
    count +=1

if count == len(word_cleaned):
  print(f'{word} é palíndromo!')
else:
  print(f'{word} não é palíndromo!')

