import random


def carregar_palavras(nome_arquivo):
    """Carrega palavras de um arquivo de texto."""
    try:
        with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
            return [palavra.strip().upper() for palavra in arquivo] 
            '''Cria uma lista de palavras, remove espaços em branco nas extremidades 
               e converte as palavras para maiúsculas'''
    except FileNotFoundError:
        print(f"Erro: O arquivo '{nome_arquivo}' não foi encontrado.")
        return [] # Retorna uma lista vazia para indicar que não há palavras disponíveis


def escolher_palavra(palavras):
    """Escolhe uma palavra aleatória da lista."""
    return random.choice(palavras)


def exibir_palavra(palavra, letras_corretas):
    """Exibe a palavra com as letras adivinhadas."""
    return ' '.join(letra if letra in letras_corretas else '_' for letra in palavra)
    '''
    Para cada letra em palavra, verifica se a letra está em letras_corretas.
    Se sim, exibe a letra; Se não, exibe ('_').
    As letras ou sublinhados são unidos e separados por espaços (' '.join(...))).
    '''

def jogar_forca():
    """Função principal"""
    palavras = carregar_palavras('palavras.txt')
    if not palavras: #  Verifica se a lista está vazia. Se sim, o arquivo não foi encontrado ou estava vazio.
        print("Não foi possível iniciar, Verifique o arquivo de palavras.")
        return

    palavra = escolher_palavra(palavras) # Escolhe uma palavra aleatória da lista
    letras_corretas = set() # Armazena as letras que o jogador adivinhou corretamente.
    letras_erradas = set() #  Armazena as letras que o jogador adivinhou incorretamente.
    tentativas_restantes = 6

    print("Jogo da Forca")
    print("Adivinhe a palavra:")

    while tentativas_restantes > 0:
        print("\nA palavra é:", exibir_palavra(palavra, letras_corretas))
        print(f"Tentativas restantes: {tentativas_restantes}")
        
        letra = input("Digite uma letra: ").upper()
        
        if len(letra) != 1 or not letra.isalpha(): # Verifica se a entrada do jogador é válida
            print("Por favor, digite apenas uma letra.")
            continue
        
        if letra in letras_corretas or letra in letras_erradas: #  Verifica se o jogador já tentou a letra anteriormente
            print("Você já tentou essa letra. Tente outra.")
            continue
        
        if letra in palavra: # Verifica se a letra digitada está na palavra
            letras_corretas.add(letra)
            if set(palavra) == letras_corretas:
                print(f"\nParabéns! A palavra era: {palavra}")
                return
        else:
            letras_erradas.add(letra)
            tentativas_restantes -= 1
            print(f"-> Você errou pela {7 - tentativas_restantes}ª vez. ", end="")
            if tentativas_restantes > 0:
                print("Tente de novo!")
            else:
                print(f"\nFim de jogo! A palavra era: {palavra}")
                return


if __name__ == "__main__":
    jogar_forca()