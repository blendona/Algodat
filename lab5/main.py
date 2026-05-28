import sys



def main():
    data = sys.stdin.read().split('\n')
    idx = 0

    chars = data[idx].split()
    idx += 1
    k = len(chars)

    # Build cost lookup: alpha[(a, b)] = gain of aligning character a with b
    alpha = {}
    for i in range(k):
        row = list(map(int, data[idx].split()))
        idx += 1
        for j in range(k):
            alpha[(chars[i], chars[j])] = row[j]

    gap_cost = -4  # cost of inserting a '*' gap

    Q = int(data[idx])
    idx += 1

    results = []

    for _ in range(Q):
        parts = data[idx].split()
        idx += 1
        X, Y = parts[0], parts[1]
        m, n = len(X), len(Y)

        # A[i][j] = max gain aligning X[:i] with Y[:j]
        A = [[0] * (n + 1) for _ in range(m + 1)]
        for i in range(m + 1):
            A[i][0] = i * gap_cost
        for j in range(n + 1):
            A[0][j] = j * gap_cost

        for i in range(1, m + 1):
            xi = X[i - 1]
            row_i = A[i]
            row_prev = A[i - 1]
            for j in range(1, n + 1):
                match = alpha[(xi, Y[j - 1])] + row_prev[j - 1]
                gap_in_x = gap_cost + row_i[j - 1]   # '*' in X, Y keeps Y[j-1]
                gap_in_y = gap_cost + row_prev[j]     # X keeps X[i-1], '*' in Y
                row_i[j] = match if match >= gap_in_x and match >= gap_in_y \
                    else (gap_in_x if gap_in_x >= gap_in_y else gap_in_y)
                

        # Traceback from (m, n) to reconstruct the aligned strings
        aligned_x, aligned_y = [], []
        i, j = m, n
        while i > 0 or j > 0:
            if i > 0 and j > 0 and A[i][j] == alpha[(X[i - 1], Y[j - 1])] + A[i - 1][j - 1]:
                aligned_x.append(X[i - 1])
                aligned_y.append(Y[j - 1])
                i -= 1
                j -= 1
            elif j > 0 and A[i][j] == gap_cost + A[i][j - 1]:
                aligned_x.append('*')
                aligned_y.append(Y[j - 1])
                j -= 1
            else:
                aligned_x.append(X[i - 1])
                aligned_y.append('*')
                i -= 1

        aligned_x.reverse()
        aligned_y.reverse()
        results.append(''.join(aligned_x) + ' ' + ''.join(aligned_y))

    print('\n'.join(results))


main()
