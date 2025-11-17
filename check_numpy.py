import time
import numpy as np


def read_input(input_file):
    print(f"Зчитування матриць з файлу: '{input_file}'...")
    with open(input_file, 'r') as f:
        num = int(f.readline()) # 1024, 512
        block = int(f.readline()) # 16
        matrix_a = [[int(x) for x in f.readline().split()] for _ in range(num)]
        matrix_b = [[int(x) for x in f.readline().split()] for _ in range(num)]
    print("Матриці успішно зчитано.\n")
    return num, block, matrix_a, matrix_b


def write_output(matrix_c, output_file):
    print(f"Запис результату у файл '{output_file}'...")
    with open(output_file, 'w') as f:
        for row in matrix_c:
            f.write(' '.join(map(str, row)) + '\n')
    print("Результат успішно записано.")


if __name__ == "__main__":
    input_path = "input.txt"
    output_path = "output.txt"

    n, bs, A, B = read_input(input_path) # зчитуємо файл: розміри і матриці

    # просте множення матриць за допомогою бібліотеки numpy для перевірки результатів множення
    A_np = np.array(A)
    B_np = np.array(B)
    C_np = A_np @ B_np
    C = C_np.tolist()

    write_output(C, output_path)