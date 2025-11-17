from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file=None, output_file=None):
        self.input_file = input_file
        self.output_file = output_file
        self.workers = workers
        print("Initialized")

    def solve(self):
        n, bs, matrix_a, matrix_b = self.read_input()
        assert n == len(matrix_a[0]), "Matrix A is not square"
        assert n == len(matrix_b), "Matrix A and B are not compatible"
        assert n == len(matrix_b[0]), "Matrix B is not square"
        assert n % bs == 0, "Matrix size isn't divisible by block size"
        mapped = []
        p = len(self.workers)
        for i in range(p):
            mapped.append(self.workers[i].compute(bs, matrix_a, matrix_b, i, p))
        result_matrix = self.reduce(mapped, n)
        self.write_output(result_matrix)
        # print("Job Finished")

    @staticmethod
    @expose
    def compute(bs, matrix_a, matrix_b, worker_id, total_workers):
        n = len(matrix_a[0])
        local_c = [[0] * n for _ in range(n)]
        nb = n // bs
        for bi in range(nb):
            for bj in range(nb):
                block_index = bi * nb + bj
                if block_index % total_workers == worker_id:
                    for bk in range(nb):
                        for i in range(bs):
                            for j in range(bs):
                                sum_val = 0
                                for k in range(bs):
                                    row_a = bi * bs + i
                                    col_a = bk * bs + k
                                    row_b = bk * bs + k
                                    col_b = bj * bs + j
                                    sum_val += matrix_a[row_a][col_a] * matrix_b[row_b][col_b]

                                row_c = bi * bs + i
                                col_c = bj * bs + j
                                local_c[row_c][col_c] += sum_val
        return local_c


    @staticmethod
    @expose
    def reduce(mapped, n):
        result_matrix = [[0] * n for _ in range(n)]
        for worker_result in mapped:
            mat = worker_result.value
            for i in range(n):
                for j in range(n):
                    result_matrix[i][j] += mat[i][j]
        return result_matrix

    def read_input(self):
        with open(self.input_file, 'r') as f:
            n = int(f.readline())
            bs = int(f.readline())
            matrix_a = [[int(x) for x in f.readline().split()] for i in range(n)]
            matrix_b = [[int(x) for x in f.readline().split()] for i in range(n)]
        return n, bs, matrix_a, matrix_b

    def write_output(self, matrix_c):
        with open(self.output_file, 'w') as f:
            n = len(matrix_c)
            for i in range(n):
                f.write(' '.join(str(matrix_c[i][j]) for j in range(n)) + '\n')
