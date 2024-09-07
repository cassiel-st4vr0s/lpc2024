import random

def rolar_dado():
    """Simula uma rolagem de dado, retornando um número entre 1 e 6."""
    return random.randint(1, 6)

def simular_rolagens(num_rolagens):
    """Simula um número de rolagens de dado e retorna a contagem de cada face."""
    face_counts = [0] * 7  # Lista que armazena a contagem de cada face
    
    for _ in range(num_rolagens):
        resultado = rolar_dado()
        face_counts[resultado] += 1
    
    return face_counts

def print_resultados(face_counts, num_rolagens):
    """Imprime os resultados das rolagens na tela."""
    print(f"Resultados após {num_rolagens} rolagens:")
    for face in range(1, 7):
        print(f"{face}: {face_counts[face]} vezes")

def imprimir_porcentagens(face_counts, num_rolagens):
    """Imprime as porcentagens de ocorrência de cada face."""
    print("\nPorcentagens:")
    for face in range(1, 7):
        percentage = (face_counts[face] / num_rolagens) * 100
        print(f"Face {face}: {percentage:.2f}%")

def main():
    num_rolagens = 100
    face_counts = simular_rolagens(num_rolagens)
    print_resultados(face_counts, num_rolagens)
    imprimir_porcentagens(face_counts, num_rolagens)

if __name__ == "__main__":
    main()
