import numpy as np
N = 3
start_column = 7
board = np.array([[1, 1, 1, 5, 5, 5, 5, 1, 4, 4, 4, 2, 5, 5, 1],
                         [2, 1, 5, 1, 5, 5, 2, 2, 3, 4, 4, 2, 2, 1, 1],
                         [4, 1, 3, 1, 1, 1, 1, 3, 3, 3, 5, 5, 2, 1, 1],
                         [4, 3, 3, 2, 2, 2, 4, 4, 1, 1, 5, 5, 2, 3, 4],
                         [3, 1, 2, 2, 2, 4, 4, 4, 4, 2, 2, 3, 3, 3, 3],
                         [3, 4, 4, 3, 3, 3, 3, 5, 5, 2, 3, 4, 4, 4, 2],
                         [5, 5, 4, 4, 4, 4, 3, 5, 5, 1, 1, 1, 1, 2, 2]], dtype=np.int8)
value = 4
flat_board = board.reshape(-1) #(105)
w,h = board.shape
index_grid = np.arange(w * h).reshape(w, h)

up    = np.pad(index_grid[:-1,],  ((1,0),(0,0)), constant_values=-1).flatten()
right = np.pad(index_grid[:,1:],  ((0,0),(0,1)), constant_values=-1).flatten()
down  = np.pad(index_grid[1:,:],  ((0,1),(0,0)), constant_values=-1).flatten()
left  = np.pad(index_grid[:,:-1], ((0,0),(1,0)), constant_values=-1).flatten()

nearby = np.column_stack((up,right,down,left))
flat_board_pad = np.append(flat_board, -1)
nearby[flat_board_pad[nearby]!=board.reshape(-1,1)] = -1
valid_starts = index_grid[board[:,start_column] == value, start_column] #start from central column


search = valid_starts[:, np.newaxis]
for i in range(N-1):
    head = search[:,-1]
    candidates = nearby[head].flatten()
    mask_invalid = candidates != -1
    search = np.repeat(search,4,axis=0)
    mask_wrong = ~np.any(candidates.reshape(-1,1) == search, axis=1)
    mask = mask_invalid & mask_wrong
    search = np.column_stack((search[mask],candidates[mask]))
search = np.unique(np.sort(search, axis=1), axis=0)

coordinates = np.stack((search // w, search % w), axis=2)

print(coordinates)


