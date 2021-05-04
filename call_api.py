import requests

URL = "https://mooapi.herokuapp.com/"

def dump_data(api_url, params, methpd):
    try:
        response = ''
        if method == 'GET':
            response = requests.get(
                URL+api_url,
                params = params    
            ) 
        elif method == 'POST': 
            response = requests.post(
                URL+api_url,
                data = params    
            )
        if (response.status_code == 200):
            print("The request was a success!")
        response.raise_for_status()
    # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        print(error)

def dump_reserve_config_data(CoinType, LoanToValuePercentage, LiquidationThreshold, LiquidationBonus, InterestRateStrategyAddress, UsageAsCollateralEnabled, BorrowingEnabled, StableBorrowRateEnabled, isActive):
    dump_data('set/DB_CeloMainnet/Tbl_ReserveConfigurationData', {'CoinType': CoinType,'LoanToValuePercentage': LoanToValuePercentage, 'LiquidationThreshold': LiquidationThreshold, 'LiquidationBonus': LiquidationBonus, 'InterestRateStrategyAddress': InterestRateStrategyAddress, 'UsageAsCollateralEnabled': UsageAsCollateralEnabled, 'BorrowingEnabled': BorrowingEnabled, 'StableBorrowRateEnabled': StableBorrowRateEnabled, 'isActive': isActive}, 'GET')

def dump_reserve_data(CoinType, TotalLiquidity, AvailableLiquidity, TotalBorrowsStable, TotalBorrowsVariable, LiquidityRate, VariableRate, AverageStableRate, UtilizationRate, LiquidityIndex, VariableBorrowIndex, MToken, LastUpdate):
    dump_data('set/DB_CeloMainnet/Tbl_Reserve_data', {'CoinType': CoinType, 'TotalLiquidity': TotalLiquidity, 'AvailableLiquidity': AvailableLiquidity, 'TotalBorrowsStable': TotalBorrowsStable, 'TotalBorrowsVariable': TotalBorrowsVariable, 'LiquidityRate': LiquidityRate, 'VariableRate': VariableRate, 'AverageStableRate': AverageStableRate, 'UtilizationRate': UtilizationRate, 'LiquidityIndex': LiquidityIndex, 'VariableBorrowIndex': VariableBorrowIndex, 'MToken': MToken, 'LastUpdate': LastUpdate}, 'GET')

def dump_user_addresses(addresses):
    dump_data('set/DB_CeloMainnet/Tbl_User/add_addresses', {'addresses': addresses}, 'POST')

def dump_user_account_data(address, TotalLiquidityETH, TotalCollateralETH, TotalBorrowsETH, TotalFeesETH, AvailableBorrowsETH, CurrentLiquidationThreshold, LoanToValuePercentage, HealthFactor):
    dump_data('set/DB_CeloMainnet/Tbl_UserAccountData', {'address': address, 'TotalLiquidityETH': TotalLiquidityETH, 'TotalCollateralETH': TotalCollateralETH, 'TotalBorrowsETH': TotalBorrowsETH, 'TotalFeesETH': TotalFeesETH, 'AvailableBorrowsETH': AvailableBorrowsETH, 'CurrentLiquidationThreshold': CurrentLiquidationThreshold, 'LoanToValuePercentage': LoanToValuePercentage, 'HealthFactor': HealthFactor}, 'GET')

def dump_user_reserve_data(coinType, address, Deposited, Borrowed, Debt, RateMode, BorrowRate, LiquidityRate, OriginationFee, BorrowIndex, LastUpdate, IsCollateral):
    dump_data('set/DB_CeloMainnet/Tbl_UserReserveData', {'coinType': coinType, 'address': address, 'Deposited': Deposited, 'Borrowed': Borrowed, 'Debt': Debt, 'RateMode': RateMode, 'BorrowRate': BorrowRate, 'LiquidityRate': LiquidityRate, 'OriginationFee': OriginationFee, 'BorrowIndex': BorrowIndex, 'LastUpdate': LastUpdate, 'IsCollateral': IsCollateral}, 'GET')

def dump_user_activity_data(coinType, activityType, amount, apr):
    dump_data('set/DB_CeloMainnet/Tbl_User_Activity', {'coinType': coinType, 'activityType': activityType, 'amount': amount, 'apr': apr}, 'GET')

def dump_latest_scanned_block_number(blockNumber):
    dump_data('/set/block_number', {'blockNumber': blockNumber}, 'GET')