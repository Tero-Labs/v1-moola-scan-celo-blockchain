import requests, time

URL = "https://mooapi.herokuapp.com/"

def dump_data(api_url, params, method):
    time.sleep(1)
    # try:
    #     response = ''
    #     if method == 'GET':
    #         response = requests.get(
    #             URL+api_url,
    #             params = params    
    #         ) 
    #     elif method == 'POST': 
    #         response = requests.post(
    #             URL+api_url,
    #             data = params    
    #         )
    #     if (response.status_code == 200):
    #         print("The request was a success!")
    #     response.raise_for_status()
    # # Additional code will only run if the request is successful
    # except requests.exceptions.HTTPError as error:
    #     print(error)

def dump_reserve_config_data(CoinType, LoanToValuePercentage, LiquidationThreshold, LiquidationBonus, InterestRateStrategyAddress, UsageAsCollateralEnabled, BorrowingEnabled, StableBorrowRateEnabled, isActive):
    dump_data('set/DB_CeloMainnet/Tbl_ReserveConfigurationData', {'coin_name': CoinType,'ltv': LoanToValuePercentage, 'liquidation_threshold': LiquidationThreshold, 'liquidation_discount': LiquidationBonus, 'interest_rate_strategy_address': InterestRateStrategyAddress, 'usage_as_collateral_enabled': UsageAsCollateralEnabled, 'borrowing_enabled': BorrowingEnabled, 'stable_borrow_rate_enabled': StableBorrowRateEnabled, 'enabled': isActive, 'agent_id':"Test"}, 'GET')


def dump_reserve_data(CoinType, TotalLiquidity, AvailableLiquidity, TotalBorrowsStable, TotalBorrowsVariable, LiquidityRate, VariableRate, StableRate, AverageStableRate, UtilizationRate, LiquidityIndex, VariableBorrowIndex, MToken, LastUpdate):
    dump_data('set/DB_CeloMainnet/Tbl_Reserve_data', {'coin_name': CoinType, 'total_liquidity': TotalLiquidity, 'available_liquidity': AvailableLiquidity, 'total_borrows_stable': TotalBorrowsStable, 'total_borrows_variable': TotalBorrowsVariable, 'liquidity_rate': LiquidityRate, 'variable_borrow_rate': VariableRate, 'stable_borrow_rate': StableRate, 'average_stable_borrow_rate': AverageStableRate, 'utilization_rate': UtilizationRate, 'liquidity_index': LiquidityIndex, 'variable_borrow_index': VariableBorrowIndex, 'atoken_address': MToken, 'last_update': LastUpdate, 'agent_id':"Test"}, 'GET')


def dump_user_addresses(addresses):
    dump_data('set/DB_CeloMainnet/Tbl_User/add_addresses', {'addresses': addresses, 'agent_id':"Test"}, 'GET')

def dump_user_account_data(address, TotalLiquidityETH, TotalCollateralETH, TotalBorrowsETH, TotalFeesETH, AvailableBorrowsETH, CurrentLiquidationThreshold, LoanToValuePercentage, HealthFactor):
    dump_data('set/DB_CeloMainnet/Tbl_UserAccountData', {'address': address, 'total_liquidity_eth': TotalLiquidityETH, 'total_collateral_eth': TotalCollateralETH, 'total_borrows_eth': TotalBorrowsETH, 'total_fees_eth': TotalFeesETH, 'available_borrows_eth': AvailableBorrowsETH, 'current_liquidation_threshold': CurrentLiquidationThreshold, 'ltv': LoanToValuePercentage, 'health_factor': HealthFactor, 'agent_id':"Test"}, 'GET')

def dump_user_reserve_data(coinType, address, Deposited, Borrowed, Debt, RateMode, BorrowRate, LiquidityRate, OriginationFee, BorrowIndex, LastUpdate, IsCollateral):
    dump_data('set/DB_CeloMainnet/Tbl_UserReserveData', {'coin_name': coinType, 'address': address, 'deposited': Deposited, 'borrowed': Borrowed, 'debt': Debt, 'rate_mode': RateMode, 'borrow_rate': BorrowRate, 'liquidity_rate': LiquidityRate, 'origination_fee': OriginationFee, 'borrow_index': BorrowIndex, 'last_update': LastUpdate, 'is_collateral': IsCollateral, 'agent_id':"Test"}, 'GET')

def dump_user_activity_data(address, coinType, activityType, amount):
    dump_data('set/DB_CeloMainnet/Tbl_User_Activity', {'address': address, 'coin_name': coinType, 'activity_type': activityType, 'amount': amount, 'agent_id':"Test"}, 'GET')

def dump_latest_scanned_block_number(blockNumber):
    dump_data('/set/block_number', {'blockNumber': blockNumber}, 'GET')