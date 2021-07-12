## Workflow

The following is the workflow to extract data from celo blockchain:

* Get the latest block from alfajores network
* Ignore the latest 5 blocks and get the previous 10 blocks
* Get the lending pool reserve configuration parameter for Celo and cUSD using `getReserveConfigurationData()` method
* Get the lending pool global information of the reserve pools using `getReserveData()` method for Celo and cUSD
* You can also get blocks data of the 10 blocks [not a required step] 
* Get logs data of the 10 blocks & addresses from the logs
* Get the unique addresses
* For each unique address, you can get information specific to a user address using `getUserAccountData()` method
* Get reserve specific user for each unique address using `getUserReserveData()` method for Celo and cUSD


## Installation

```bash
pip install -r requirements.txt
```

## Methods

<details><summary><strong>getReserveConfigurationData()</strong></summary>

`function getReserveConfigurationData(address _reserve)`

Returns specific reserve's configuration parameters.

|`return` name              |Type   |Description                                             |
|---------------------------|-------|--------------------------------------------------------|
|ltv                        |uint256|Loan-to-value. Value in percentage|
|liquidationThreshold       |uint256|liquidation threshold. Value in percentage              |
|liquidationDiscount        |uint256|liquidation bonus. Value in percentage|
|interestRateStrategyAddress|address|address of the contract defining the interest rate strategy|
|usageAsCollateralEnabled   |bool   |if `true`, reserve asset can be used as collateral for borrowing|
|borrowingEnabled           |bool   |if `true`, reserve asset can be borrowed|
|stableBorrowRateEnabled    |bool   |if `true`, reserve asset can be borrowed with stable rate mode|
|isActive                   |bool   |if `true`, users can interact with reserve asset|

</details>

<details><summary><strong>getReserveData()</strong></summary>

`function getReserveData(address _reserve)`

Returns global information on any asset `reserve` pool

|`return` name              |Type   |Description                                             |
|---------------------------|-------|--------------------------------------------------------|
|totalLiquidity             |uint256|`reserve` total liquidity|
|availableLiquidity         |uint256|`reserve` available liquidity for borrowing|
|totalBorrowsStable         |uint256|total amount of outstanding borrows at Stable rate|
|totalBorrowsVariable       |uint256|total amount of outstanding borrows at Variable rate|
|liquidityRate              |uint256|current deposit APY of the `reserve` for depositors, in Ray units|
|variableBorrowRate         |uint256|current variable rate APY of the `reserve` pool, in Ray units|
|stableBorrowRate           |uint256|current stable rate APY of the `reserve` pool, in Ray units|
|averageStableBorrowRate    |uint256|current average stable borrow rate|
|utilizationRate            |uint256|expressed as total borrows/total liquidity|
|liquidityIndex             |uint256|cumulative liquidity index|
|variableBorrowIndex        |uint256|cumulative variable borrow index|
|aTokenAddress              |address|mTokens contract address for the specific `_reserve`|
|lastUpdateTimestamp        |uint40 |timestamp of the last update of `reserve` data|

</details>

<details><summary><strong>getReserveData()</strong></summary>

`function getUserAccountData(address _user)`

Returns information of a reserve exclusively related with a particular `user` address

|`return` name              |Type   |Description                                             |
|---------------------------|-------|--------------------------------------------------------|
|totalLiquidityETH          |uint256|`user` aggregated deposits across all the reserves. In Wei|
|totalCollateralETH         |uint256|`user` aggregated collateral across all the reserves. In Wei|
|totalBorrowsETH            |uint256|`user` aggregated outstanding borrows across all the reserves. In Wei|
|totalFeesETH               |uint256|`user` aggregated current outstanding fees in ETH. In Wei|
|availableBorrowsETH        |uint256|`user` available amount to borrow in ETH|
|currentLiquidationThreshold|uint256|`user` current average liquidation threshold across all the collaterals deposited|
|ltv                        |uint256|`user` average Loan-to-Value between all the collaterals|
|healthFactor               |uint256|`user` current Health Factor|

</details>


<details><summary><strong>getUserReserveData()</strong></summary>

`function getUserReserveData(address _reserve, address _user)`

Returns information related to the `user` data on a specific `reserve`


|`return` name              |Type   |Description                                             |
|---------------------------|-------|--------------------------------------------------------|
|currentATokenBalance       |uint256|current `reserve` mToken balance|
|currentBorrowBalance       |uint256|`user` current `reserve` outstanding borrow balance|
|principalBorrowBalance     |uint256|`user` balance of borrowed asset|
|borrowRateMode             |uint256|`user` borrow rate mode either Stable or Variable|
|borrowRate                 |uint256|`user` current borrow rate APY|
|liquidityRate              |uint256|`user` current earn rate on `_reserve`|
|originationFee             |uint256|`user` outstanding loan origination fee|
|variableBorrowIndex        |uint256|`user` variable cumulative index|
|lastUpdateTimestamp        |uint256|Timestamp of the last data update|
|usageAsCollateralEnabled   |bool   |Whether the user's current reserve is enabled as a collateral|

</details>

<details><summary><strong>getReserves()</strong></summary>

`function getReserves()`

Returns an array of all the active reserves addresses.
</details>

## Emitted Events
The `LendingPool` contract produces events that can be monitored on the Ethereum blockchain. For more information on emitted events and filters, refer to [the official solidity documentation.](https://solidity.readthedocs.io/en/latest/contracts.html#events)

In Moola protocol, `reserve` is defined by the smart-contract of the asset used for the method interaction. 

- A list of all smart-contract addresses is available in here. 
- To avoid the usage of a CELO wrapper throughout the protocol (such as CELO duality token), a mock address is used for the CELO reserve: `0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE`

<details><summary><strong>Deposit</strong></summary>

|`return` name    |Type   |Description                                             |
|-----------------|-------|--------------------------------------------------------|
|_reserve         |address|address of the underlying asset|
|_user            |address|address of the `user`|
|_amount          |uint256|amount deposited, in Wei|
|_referral        |uint16 |`ReferralCode` for referral programs|
|_timestamp       |uint256|timestamp of the transaction, in Unix time|

</details>

<details><summary><strong>RedeemUnderlying</strong></summary>

|`return` name    |Type   |Description                                             |
|-----------------|-------|--------------------------------------------------------|
|_reserve         |address|address of the underlying asset|
|_user            |address|address of the `user`|
|_amount          |uint256|amount redeemed, in Wei|
|_timestamp       |uint256|timestamp of the transaction, in Unix time|

</details>

<details><summary><strong>Borrow</strong></summary>

|`return` name         |Type   |Description                                             |
|----------------------|-------|--------------------------------------------------------|
|_reserve              |address|address of the underlying asset|
|_user                 |address|address of the `user`|
|_amount               |uint256|amount borrowed, in Wei|
|_borrowRateMode       |uint16 |interest rate mode `0` for None, `1` for stable and `2` for variable|
|_borrowRate           |uint256|APY of the loan at the time of the `borrow()` call. in Wei|
|_originationFee       |uint256|amount of the `originationFee` of the loan, in Ray units|
|_borrowBalanceIncrease|uint256|amount of debt increased since the last update by the user, in Wei|
|_referral             |uint16 |`ReferralCode` for referral programs|
|_timestamp            |uint256|timestamp of the transaction, in Unix time|

</details>

<details><summary><strong>Repay</strong></summary>

|`return` name         |Type   |Description                                             |
|----------------------|-------|--------------------------------------------------------|
|_reserve              |address|address of the underlying asset|
|_user                 |address|address of the `user`|
|_repayer              |address|address of the `repayer`|
|_amountMinusFees      |uint256|amount repayed, without fees|
|_fees                 |uint256|fees paid|
|_borrowBalanceIncrease|uint256|amount of debt increased since the last update by the user, in Wei|
|_timestamp            |uint256|timestamp of the transaction, in Unix time|

</details>

<details><summary><strong>LiquidationCall</strong></summary>

|`return` name              |Type   |Description                                             |
|---------------------------|-------|--------------------------------------------------------|
|_collateral                |address|address of the contract of collateral asset being liquidated|
|_reserve                   |address|address of the underlying asset|
|_user                      |address|address of the `user` being liquidated|
|_purchaseAmount            |uint256|amount of the liquidation, in Wei|
|_liquidatedCollateralAmount|uint256|amount of collateral being liquidated|
|_accruedBorrowInterest     |uint256|amount of debt increased since the last update by the user, in Wei|
|_liquidator                |address|address of the liquidator|
|_receiveAToken             |bool   |`true` if the liquidator wants to receive mTokens, `false` otherwise|
|_timestamp                 |uint256|timestamp of the transaction, in Unix time|

</details>