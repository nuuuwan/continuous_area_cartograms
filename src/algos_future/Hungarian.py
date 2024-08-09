import numpy as np
from scipy.optimize import linear_sum_assignment


class Hungarian:
    # See https://en.wikipedia.org/wiki/Hungarian_algorithm for details

    def __init__(self, cost_matrix):
        self.cost_matrix = np.array(cost_matrix)

    def run(self):
        # Apply the Hungarian algorithm
        row_ind, col_ind = linear_sum_assignment(self.cost_matrix)

        # Optimal assignment and cost
        optimal_assignment = list(zip(row_ind, col_ind))
        self.cost_matrix[row_ind, col_ind].sum()

        return optimal_assignment


if __name__ == "__main__":
    INF = int(1e9)
    optimal_assignment = Hungarian(
        [[1, INF, INF], [INF, 1, INF], [INF, INF, 1]]
    ).run()
    print(optimal_assignment)
