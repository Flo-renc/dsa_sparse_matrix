import os

class SparseMatrix:
    def __init__(self):
        self.elements = {}  # Dictionary to hold non-zero elements with (row, col) as key

    def insert(self, row, col, value):
        if value != 0:
            self.elements[(row, col)] = value

    @staticmethod
    def load_from_file(file_path):
        matrix = SparseMatrix()
        try:
            with open(file_path, 'r') as f:
                row_line = f.readline().strip()
                if not row_line.startswith('rows='):
                    raise ValueError(f"Missing 'rows=' declaration in {file_path}")

                rows = int(row_line.split('=')[1])

                col_line = f.readline().strip()
                if not col_line.startswith('cols='):
                    raise ValueError(f"Missing 'cols=' declaration in {file_path}")

                cols = int(col_line.split('=')[1])

                for line_number, line in enumerate(f, start=3):  # Start tracking from line 3 (entries)
                    if line.strip():  # Ignore empty lines
                        if not (line.startswith('(') and line.endswith(')')):
                            raise ValueError(f"Invalid matrix entry format at line {line_number} in {file_path}: {line.strip()}")
                        parts = line.strip()[1:-1].split(', ')
                        if len(parts) != 3:
                            raise ValueError(f"Expected 3 values, got {len(parts)} in line {line_number} of {file_path}")
                        row, col, value = map(int, parts)
                        matrix.insert(row, col, value)

        except Exception as e:
            raise ValueError(f"Error in file {file_path}: {str(e)}")

        return matrix

    def add(self, other):
        result = SparseMatrix()
        all_keys = set(self.elements.keys()).union(set(other.elements.keys()))
        
        for key in all_keys:
            value = self.elements.get(key, 0) + other.elements.get(key, 0)
            result.insert(key[0], key[1], value)
        
        return result

    def subtract(self, other):
        result = SparseMatrix()
        all_keys = set(self.elements.keys()).union(set(other.elements.keys()))
        
        for key in all_keys:
            value = self.elements.get(key, 0) - other.elements.get(key, 0)
            result.insert(key[0], key[1], value)
        
        return result

    def multiply(self, other):
        result = SparseMatrix()

        for (row_a, col_a), value_a in self.elements.items():
            for (row_b, col_b), value_b in other.elements.items():
                if col_a == row_b:
                    current_value = result.elements.get((row_a, col_b), 0)
                    result.insert(row_a, col_b, current_value + value_a * value_b)
                    
        return result


def write_matrix_to_file(matrix, file_path):
    with open(file_path, 'w') as f:
        for (row, col), value in matrix.elements.items():
            f.write(f"({row}, {col}, {value})\n")


def process_sparse_matrices(input_dir, output_dir):
    input_files = os.listdir(input_dir)
    os.makedirs(output_dir, exist_ok=True)
    error_log = []

    for i, file_name in enumerate(input_files):
        input_path = os.path.join(input_dir, file_name)
        output_path_add = os.path.join(output_dir, f"{file_name}_addition.txt")
        output_path_sub = os.path.join(output_dir, f"{file_name}_subtraction.txt")
        output_path_mul = os.path.join(output_dir, f"{file_name}_multiplication.txt")

        try:
            # Load the first matrix
            matrix_a = SparseMatrix.load_from_file(input_path)
            # Load the second matrix (if needed, use different file or same)
            matrix_b = SparseMatrix.load_from_file(input_path)  # Modify to load another matrix as needed

            # Perform addition, subtraction, and multiplication
            result_add = matrix_a.add(matrix_b)
            result_sub = matrix_a.subtract(matrix_b)
            result_mul = matrix_a.multiply(matrix_b)

            # Write the results to output files
            write_matrix_to_file(result_add, output_path_add)
            write_matrix_to_file(result_sub, output_path_sub)
            write_matrix_to_file(result_mul, output_path_mul)

        except ValueError as e:
            # Skip invalid matrices and log the error
            error_log.append(f"Skipping {file_name}: {e}")
            continue

    # Write the error log to a file
    with open(os.path.join(output_dir, "error_log.txt"), 'w') as f:
        for error in error_log:
            f.write(error + "\n")


if __name__ == "__main__":
    input_dir = 'sample_inputs'  # Directory where input files are stored
    output_dir = 'sample_results'  # Directory where results will be stored
    process_sparse_matrices(input_dir, output_dir)