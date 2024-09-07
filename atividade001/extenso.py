def num_extenso(numero):
    """Converte um número de 0 a 99 em sua representação por extenso."""
    unidades = [
        "zero", "um", "dois", "três", "quatro", "cinco",
        "seis", "sete", "oito", "nove"
    ]
    especiais = [
        "dez", "onze", "doze", "treze", "quatorze", "quinze",
        "dezesseis", "dezessete", "dezoito", "dezenove"
    ]
    dezenas = [
        "", "", "vinte", "trinta", "quarenta", "cinquenta",
        "sessenta", "setenta", "oitenta", "noventa"
    ]

    if 0 <= numero < 10: # Verifica se o número está entre 0 e 9. Se sim, retorna a representação correspondente da lista unidades
        return unidades[numero]
    elif 10 <= numero < 20: # Verifica se o número está entre 10 e 19. Se sim, retorna a representação correspondente da lista
        return especiais[numero - 10]
    else: # Trata os números de 20 a 99
        dezena = numero // 10
        unidade = numero % 10
        if unidade == 0: # Se a unidade for 0, retorna apenas a dezena, como "vinte", "trinta", etc.
            return dezenas[dezena]
        else:
            return f"{dezenas[dezena]} e {unidades[unidade]}"


def main():
    """main function"""
    while True:
        entrada = input("Digite um número entre 0 e 99 (ou 's' para sair): ")
        
        if entrada.lower() == 's':
            print("Operação encerrada")
            break
        
        try:
            numero = int(entrada) # Tenta converter a entrada do usuário para um número inteiro.
            if 0 <= numero <= 99:
                print(f"{num_extenso(numero).capitalize()}.")
                ''' 
                Se o número estiver no intervalo, chama num_extenso para convertê-lo em texto,
                capitaliza a primeira letra e exibe a string
                '''
            else:
                print("Número > 99, digite um número entre 0 e 99.")
        except ValueError:
            print("Entrada inválida. Digite um número válido.")
            '''
            Se a conversão para inteiro falhar, captura a exceção 
            e exibe mensagem indicando que a entrada foi inválida.
            '''


if __name__ == "__main__":
    main()