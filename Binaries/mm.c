#include <stdio.h>

// Function to perform matrix multiplication
void matrixMultiplication(int size, int matrix1[][size], int matrix2[][size], int result[][size]) {
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            result[i][j] = 0;
            for (int k = 0; k < size; ++k) {
                result[i][j] += matrix1[i][k] * matrix2[k][j];
            }
        }
    }
}

int main() {
    int size = 10;

    int matrixA[size][size];
    int matrixB[size][size];
    int resultMatrix[size][size];

    int count = 1;
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            matrixA[i][j] = count++;
            matrixB[i][j] = count++;
        }
    }

    matrixMultiplication(size, matrixA, matrixB, resultMatrix);

    // Printing the result (commented out to avoid printing large matrices)
    /*
    printf("Result Matrix:\n");
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            printf("%d ", result[i][j]);
        }
        printf("\n");
    }
    */

    return 0;
}

