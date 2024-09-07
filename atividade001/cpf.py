import re #Fornece funcões para buscar e manipular padrões em strings


def validate_cpf(cpf: str) -> bool:
    """
    Valida o n° de CPF recebido.

    cpf (str): CPF deve estar no formato xxx.xxx.xxx-xx

    Retorna(bool): True se o CPF é valido, False se não for
    """
    # Usa o Regex para verificar se está no formato xxx.xxx.xxx-xx
    if not re.match(r'^\d{3}\.\d{3}\.\d{3}-\d{2}$', cpf):
        return False

    # Remove os "." e o "-"
    numbers = [int(digit) for digit in cpf if digit.isdigit()]

    # Verifica se todos os caracteres não são iguais
    if len(set(numbers)) == 1:
        return False

    # Valida o primeiro dígito
    sum_of_products = sum(a*b for a, b in zip(numbers[0:9], range(10, 1, -1)))
    """
    zip:  Combina os primeiros nove dígitos do CPF com os pesos decrescentes de 10 a 2.
    sum:  Calcula a soma dos produtos dos dígitos com os pesos.
    """
    expected_digit = (sum_of_products * 10 % 11) % 10 # Calcula o primeiro dígito verificador
    if numbers[9] != expected_digit: # Compara o nono dígito com o dígito esperado.
        return False

    # Valida o segundo dígito
    sum_of_products = sum(a*b for a, b in zip(numbers[0:10], range(11, 1, -1)))
    '''Combina os primeiros dez dígitos do CPF com os pesos decrescentes de 11 a 2.'''
    expected_digit = (sum_of_products * 10 % 11) % 10
    if numbers[10] != expected_digit:
        return False

    return True


def main():
    """Main function"""
    print("Dgite um CPF no formato xxx.xxx.xxx-xx")

    while True:
        cpf = input("Dgitar CPF (Digite s para sair): ")
        
        if cpf.lower() == 's':
            print("Operação encerrada")
            break

        if validate_cpf(cpf):
            print("CPF válido")
        else:
            print("CPF inválido")


if __name__ == "__main__":
    main()