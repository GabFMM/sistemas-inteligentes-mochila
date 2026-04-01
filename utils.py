import random

def generate_items(n):
    items = []
    for _ in range(n):
        weight = random.randint(1, 100)
        
        if random.random() < 0.2:
            value = random.randint(1, 20) 
        else:
            value = random.randint(100, 200)
        
        items.append((weight, value))
    
    return tuple(items)

def fractional_knapsack_bound(items, capacity):
    dp = [[0 for _ in range(capacity + 1)] for _ in range(len(items) + 1)]

    for i in range(len(items) + 1):
        for w in range(capacity + 1):
            if i == 0 or w == 0:
                dp[i][w] = 0
            elif items[i-1][0] <= w:
                dp[i][w] = max(items[i-1][1] + dp[i-1][w-items[i-1][0]], 
                               dp[i-1][w])
            else:
                dp[i][w] = dp[i-1][w]

    return dp[len(items)][capacity]