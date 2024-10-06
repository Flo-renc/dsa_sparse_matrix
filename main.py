import os
from sparse_matrix import SparseMatrix

def main():
    # Specify the folder where the input files are located
    input_folder = "sample_inputs"
    
    # Ensure the folder exists
    if not os.path.exists(input_folder):
        print(f"Error: The folder '{input_folder}' does not exist.")
        return

    # Get all file paths from the input folder
    input_files = [os.path.join(input_folder, file) for file in os.listdir(input_folder) if file.endswith(".txt")]

    if len(input_files) < 2:
        print("Error: Not enough matrix files to perform operations.")
        return

    # Load the first two matrices (for demonstration purposes)
    matrix_file1 = input_files[0]
    matrix_file2 = input_files[1]

    print(f"Loading matrices from {matrix_file1} and {matrix_file2}...")

    # Create SparseMatrix objects from the files
    matrix1 = SparseMatrix.from_file(matrix_file1)
    matrix2 = SparseMatrix.from_file(matrix_file2)

    # Perform addition and multiplication
    print("\nMatrix 1:")
    print(matrix1)

    print("\nMatrix 2:")
    print(matrix2)

    # Adding two sparse matrices
    try:
        result_add = matrix1.add(matrix2)
        print("\nResult of Addition:")
        print(result_add)
    except ValueError as e:
        print(f"Addition error: {e}")

    # Multiplying two sparse matrices
    try:
        result_mul = matrix1.multiply(matrix2)
        print("\nResult of Multiplication:")
        print(result_mul)
    except ValueError as e:
        print(f"Multiplication error: {e}")

if __name__ == "__main__":
    main()
