def eh_palindromo(str):
    """Verifica se a string é um palindromo"""
    str = str.replace(" ", "").lower() # Remove os espaços
    return str == str[::-1] # Compara com a string invertida

def main():
    string = input("Digite uma palavra ou frase para verificar se é um palindromo: ")
    if eh_palindromo(string):
        print("É um palindromo.")
    else:
        print("Não é um palindromo.")

if __name__ == "__main__":
    main()
