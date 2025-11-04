import random

def generate_and_save_matrices(matrix_size, block, output_file):
    print(f"Генерація двох матриць розміром: {matrix_size}x{matrix_size}...")
    try:
        with open(output_file, 'w') as f:
            f.write(str(matrix_size) + '\n') # 1024
            f.write(str(block) + '\n') # 16

            for _ in range(matrix_size): # Генеруємо матрицю A
                row = [random.randint(0, 9) for _ in range(matrix_size)]
                f.write(' '.join(map(str, row)) + '\n')

            for _ in range(matrix_size): # Генеруємо матрицю B
                row = [random.randint(0, 9) for _ in range(matrix_size)]
                f.write(' '.join(map(str, row)) + '\n')

        print(f"Матриці успішно згенеровані у файл '{output_file}'.")

    except IOError as e:
        print(f"Помилка під час запису у файл '{output_file}'. {e}.")


if __name__ == "__main__":
    size = 8
    block_size = 4
    output = "input.txt"
    generate_and_save_matrices(size, block_size, output)