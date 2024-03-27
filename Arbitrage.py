liquidity = {
    ("tokenA", "tokenB"): (17, 10),
    ("tokenA", "tokenC"): (11, 7),
    ("tokenA", "tokenD"): (15, 9),
    ("tokenA", "tokenE"): (21, 5),
    ("tokenB", "tokenC"): (36, 4),
    ("tokenB", "tokenD"): (13, 6),
    ("tokenB", "tokenE"): (25, 3),
    ("tokenC", "tokenD"): (30, 12),
    ("tokenC", "tokenE"): (10, 8),
    ("tokenD", "tokenE"): (60, 25),
}

# x * y = (x + 0.997 * x_in) * (y - y_out)
def getAmountOut(amountIn, reserveIn, reserveOut):
    amountInWithFee = amountIn * 997
    return (amountInWithFee * reserveOut) / (1000 * reserveIn + amountInWithFee)

def getAmountOutWithToken(tokenIn, tokenOut, amountIn):
    if tokenIn < tokenOut:
        reserveIn, reserveOut = liquidity[(tokenIn, tokenOut)]
    else:
        reserveOut, reserveIn = liquidity[(tokenOut, tokenIn)]
    return getAmountOut(amountIn, reserveIn, reserveOut)

# turn back to targetToken at end
def check_path(path, amount, targetToken):
    for i in range(1, len(path)):
        amount = getAmountOutWithToken(path[i - 1], path[i], amount)
    if path[-1] != targetToken:
        amount = getAmountOutWithToken(path[-1], targetToken, amount)
    return amount

def dfs_path(tokenUsed, token, amount, targetToken):
    if token != targetToken:
        max_amount = getAmountOutWithToken(token, targetToken, amount)
        max_path = [token, targetToken]
    else:
        max_amount = amount
        max_path = [token]
    
    for key in tokenUsed.keys():
        if tokenUsed[key] or key == token:
            continue
        tokenUsed[key] = True
        next_amount = getAmountOutWithToken(token, key, amount)
        best_amount, best_path = dfs_path(tokenUsed, key, next_amount, targetToken)
        if best_amount > max_amount:
            max_amount = best_amount
            max_path = [token] + best_path
        tokenUsed[key] = False
    
    return max_amount, max_path

def find_best_path(token, balance):
    tokenUsed = {"tokenA": False, "tokenB": False, "tokenC": False, "tokenD": False, "tokenE": False}
    tokenUsed[token] = True

    best_amount, best_path = dfs_path(tokenUsed, "tokenB", 5, "tokenB")
    check_amount = check_path(best_path, balance, token)

    return best_amount, best_path


if __name__ == "__main__":
    balance, path = find_best_path("tokenB", 5)
    print(f"path: {path}, balance: {balance:.6f}.")