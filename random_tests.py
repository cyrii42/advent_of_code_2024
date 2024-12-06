from itertools import permutations, product, chain, pairwise, combinations, combinations_with_replacement
from pprint import pprint

# num_columns = 5
# num_rows = 3

# columns = range(num_columns)
# rows = range(num_rows)

# num_diagonals = (num_rows + num_columns) - 1

# combos = list(product(rows, columns))

# output_list = []
# for x in reversed(rows):
#     diagonal_row = [(row, col) for row, col in combos 
#                     if row >= x
#                     and (row - col == x)]
#     print(f"Row {x}: {diagonal_row}")
#     for combo in diagonal_row:
#         combos.remove(combo)
        
#     output_list.append(diagonal_row)

# for x in range(1, num_columns):
#     diagonal_row = [(row, col) for row, col in combos 
#                     if col >= x
#                     and (col - row == x)]
#     print(f"Column {x}: {diagonal_row}")
#     for combo in diagonal_row:
#         combos.remove(combo)
        
#     output_list.append(diagonal_row)

# pprint(output_list)

# import pandas as pd
# import numpy as np

# num_columns = 5
# num_rows = 3

# num_diagonals = (num_rows + num_columns) - 1

# rows = [x.split() for x in ['A B C D', 'E F G H', 'I J K L', 'M N O P']]

# df = pd.DataFrame(rows)

# print(df)

# for x in range(0-num_rows, num_columns-1):
#     print(np.diag(df, k=x))

# df2 = df.iloc[::-1].reset_index(drop=True)
# print(df2)

# for x in range(0-num_rows, num_columns-1):
#     print(np.diag(df2, k=x))


# asdf = [1, 2, 3, 4, 5, 6, 7, 8]
# print(asdf[4:])

print(5 // 2 + 1)