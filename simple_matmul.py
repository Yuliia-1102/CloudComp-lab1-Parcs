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


def block_matrix_multiply(matrix_a, matrix_b, block_size):
    """
    Виконує послідовне блочне множення матриць. Цей код є аналогом логіки з PARCS, але виконується на одному процесорі.
    """
    size = len(matrix_a)
    if size % block_size != 0:
        raise ValueError("Розмір матриці має ділитися на розмір блоку без остачі.")

    result_matrix = [[0] * size for _ in range(size)] # cтворюємо результуючу матрицю, заповнену нулями

    nb = size // block_size  # к-ть блоків в одному вимірі

    # Ітерація по всіх блоках результуючої матриці
    for bi in range(nb):
        for bj in range(nb):
            # Обчислення одного блоку C[bi][bj]
            for bk in range(nb):
                # Множення блоків A[bi][bk] та B[bk][bj] і додавання до результату
                for i in range(block_size):
                    for j in range(block_size):
                        sum_val = 0
                        for k in range(block_size):
                            row_a = bi * block_size + i
                            col_a = bk * block_size + k
                            row_b = bk * block_size + k
                            col_b = bj * block_size + j
                            sum_val += matrix_a[row_a][col_a] * matrix_b[row_b][col_b]

                        row_c = bi * block_size + i
                        col_c = bj * block_size + j
                        result_matrix[row_c][col_c] += sum_val

    return result_matrix


if __name__ == "__main__":
    input_path = "input.txt"
    output_path = "output.txt"

    # print(f"\nПочаток блочного множення...\n")
    # start_time = time.perf_counter()

    n, bs, A, B = read_input(input_path) # зчитуємо файл: розміри і матриці

    # просте множення матриць за допомогою бібліотеки numpy
    A_np = np.array(A)
    B_np = np.array(B)
    C_np = A_np @ B_np
    C = C_np.tolist()

    # C = block_matrix_multiply(A, B, bs)

    # end_time = time.perf_counter()
    # elapsed_time = end_time - start_time
    #
    # print(f"Множення завершено.\n")
    # print(f"Час виконання: {elapsed_time:.4f} секунд.")

    write_output(C, output_path)