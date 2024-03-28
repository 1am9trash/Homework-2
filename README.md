# 2024-Spring-HW2

Please complete the report problem below:

## Problem 1
Provide your profitable path, the amountIn, amountOut value for each swap, and your final reward (your tokenB balance).

#### Profitable Path
- Path: `tokenB->tokenA->tokenD->tokenC->tokenB`
- Final TokenB Balance: 20.129889
- `tokenB -> tokenA`: 5.000000 to 5.655322
- `tokenA -> tokenD`: 5.655322 to 2.458781
- `tokenD -> tokenC`: 2.458781 to 5.088927
- `tokenC -> tokenB`: 5.088927 to 20.129889

## Problem 2
What is slippage in AMM, and how does Uniswap V2 address this issue? Please illustrate with a function as an example.

#### Slippage
在提交交易跟真正執行之間存在時間差，而這中間預期價格跟執行價格的差異就是 Slippage ，在高度波動的市場或交易額極大，影響 Liquidity 更為顯著。
#### Uniswap V2 Solution
- Slippage Tolerance: 交易時可以設置對 slippage 的容忍範圍，如果價值變動過大，則回退交易，如 `swapTokensForExactTokens()` 中的 `amountInMax` 。
  ```solidity
  function swapTokensForExactTokens(
      uint256 amountOut,
      uint256 amountInMax,
      address[] calldata path,
      address to,
      uint256 deadline
  ) external returns (uint256[] memory amounts);
  ```
- Price Oracles: 透過引入 TWAP ，幫助做出合理的決策並設置 slippage tolerance 。

## Problem 3
Please examine the mint function in the UniswapV2Pair contract. Upon initial liquidity minting, a minimum liquidity is subtracted. What is the rationale behind this design?

#### mint function
在 LP 往 pool 中投入 token 時，給予 pool 所有權份額的 function 。
#### Minimum Liquidity
- 說明: Uniswap V2 在首次提供 liquidity 時，會鑄造一定數量的 token ，但會扣除 MINIMUM_LIQUIDITY (一般是 1000 單位)，這部分 liquidity 會被永久鎖定在 pool 中。
  ```solidity
  if (_totalSupply == 0) {
      liquidity = Math.sqrt(amount0.mul(amount1)).sub(MINIMUM_LIQUIDITY);
      _mint(address(0), MINIMUM_LIQUIDITY); 
  }
  ```
- 初始化: 避免 pool 中的 x 、 y 太少，使新建立的 pool 是可以支持交易的狀態。
- 確保所有權表示: 透過設定最小 liquidity ，避免 LP 可以輕易地透過極小的投入獲取 100% 所有權。
- 防止單 wei 攻擊: 單 wei 攻擊中，攻擊者可以透過及小的金額重複添加或移除 liquidity ，從 pool 剝削價值。透過鎖定最小 liquidity ，可避免 pool 被抽乾。

## Problem 4
Investigate the minting function in the UniswapV2Pair contract. When depositing tokens (not for the first time), liquidity can only be obtained using a specific formula. What is the intention behind this?

#### Liquidity Formula
在首次操作之後，往 pool 添加 token 會依據以下公式計算分配到的 liquidity，其目的如下。
- 維持公平避免稀釋所有權: 獲取價值與現有規模成正比。
- 維持乘積: 取 `min()` 維持比例。
```solidity
liquidity = Math.min(amount0.mul(_totalSupply) / _reserve0, amount1.mul(_totalSupply) / _reserve1);
```

## Problem 5
What is a sandwich attack, and how might it impact you when initiating a swap?

#### Sandwich Attack
- 觀察市場，在有人送出交易但尚未執行時，先進行交易 (透過 gas 取得優先權) 抬高 token 價格，但不超過原交易者限制的 slippage tolerance。
- 等待原交易進行。
- 出售買入的 token ，因原交易會拉高價格，因此有利可圖。
