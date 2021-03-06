import time
import aiohttp
import asyncio
from urllib.request import urlretrieve
from urllib.parse import urlencode
from aiohttp import ClientSession
import requests


URL = "http://moola-downstream-api.herokuapp.com/"

coin_dict = {
"cusd": "cUSD",
"celo": "Celo",
"ceuro": "cEUR"
}

async def fetch(url, params, method):
    async with aiohttp.ClientSession() as session:
        async with session.get(url, params=params) as response:
            resp = await response.json()
            print(resp)
            if (resp["status"] == "OK"):
                print("The request was a success!")
            # else:
            #     response.raise_for_status()
            return resp

def getLastestBlock():
    try:
        response = ''
        params = {"agent_id": 0}
        response = requests.get(
                "https://moola-downstream-api.herokuapp.com/get/agent_last_block",
                params = params    
        ) 
        res = response.json()
        print(res)
        if (res["status"] == "OK"):
            print("The request was a success!")
            return int(res["block_number"])
        else:
            return "err"
    # response.raise_for_status()
    # Additional code will only run if the request is successful
    except requests.exceptions.HTTPError as error:
        print(error)
        return "err"

def dump_data(api_url, params, method):
    asyncio.run(fetch(URL+api_url, params, method))
    print(URL+api_url+"?"+urlencode(params))
#     # time.sleep(1)
#     # print(URL+api_url+"?"+urlencode(params))
#     # print("", end="")
#     # for k, v in params.items():
#     #     print(k + ": " + str(v))
#     #     print(type(v))
#     pass
#     # try:
#     #     response = ''
#     #     if method == 'GET':
#     #         response = requests.get(
#     #             URL+api_url,
#     #             params = params    
#     #         ) 
#     #     elif method == 'POST': 
#     #         response = requests.post(
#     #             URL+api_url,
#     #             data = params    
#     #         )
#     #     res = response.json()
#     #     print(res)
#     #     if (res["status"] == "OK"):
#     #         print("The request was a success!")
#     #     response.raise_for_status()
#     # # Additional code will only run if the request is successful
#     # except requests.exceptions.HTTPError as error:
#     #     print(error)

def dump_reserve_config_data(CoinType, LoanToValuePercentage, LiquidationThreshold, LiquidationBonus, InterestRateStrategyAddress, UsageAsCollateralEnabled, BorrowingEnabled, StableBorrowRateEnabled, isActive, block_number):
    dump_data('set/insert/db_celo_mainnet/tbl_reserve_configuration', {'coin_name': coin_dict[CoinType],'ltv': LoanToValuePercentage, 'liquidation_threshold': LiquidationThreshold, 'liquidation_discount': LiquidationBonus, 'interest_rate_strategy_address': InterestRateStrategyAddress[2:], 'usage_as_collateral_enabled': UsageAsCollateralEnabled, 'usage_as_collateral_enabled__Type': 'bool', 'borrowing_enabled': BorrowingEnabled, 'borrowing_enabled__Type': 'bool', 'stable_borrow_rate_enabled': StableBorrowRateEnabled, 'stable_borrow_rate_enabled__Type': 'bool', 'enabled': isActive, 'enabled__Type': 'bool', 'block_number': block_number, "block_number__Type": "int", 'agent_id':0}, 'GET')
# is_collateral__Type=bool

def dump_reserve_data(CoinType, TotalLiquidity, AvailableLiquidity, TotalBorrowsStable, TotalBorrowsVariable, LiquidityRate, VariableRate, StableRate, AverageStableRate, UtilizationRate, LiquidityIndex, VariableBorrowIndex, MToken, LastUpdate, block_number):
    dump_data('set/insert/db_celo_mainnet/tbl_reserve', {'coin_name': coin_dict[CoinType], 'total_liquidity': TotalLiquidity, 'available_liquidity': AvailableLiquidity, 'total_borrows_stable': TotalBorrowsStable, 'total_borrows_variable': TotalBorrowsVariable, 'liquidity_rate': LiquidityRate, 'variable_borrow_rate': VariableRate, 'stable_borrow_rate': StableRate, 'average_stable_borrow_rate': AverageStableRate, 'utilization_rate': UtilizationRate, 'liquidity_index': LiquidityIndex, 'variable_borrow_index': VariableBorrowIndex, 'atoken_address': MToken[2:],  'agent_id':0, 'last_update': LastUpdate, 'last_update__Type': 'datetime', 'block_number': block_number, "block_number__Type": "int"}, 'GET')
# , 'last_update': LastUpdate,  'last_update__Type': 'datetime'

def dump_user_addresses(addresses, from_block, to_block):
    for address in addresses:
        dump_data('set/insert/db_celo_mainnet/tbl_user', {'address': address[2:].lower(), 'block_from': from_block, 'block_to': to_block, 'agent_id':0}, 'GET')

def dump_user_account_data(address, TotalLiquidityETH, TotalCollateralETH, TotalBorrowsETH, TotalFeesETH, AvailableBorrowsETH, CurrentLiquidationThreshold, LoanToValuePercentage, HealthFactor, block_number):
    dump_data('set/insert/db_celo_mainnet/tbl_user_account', {'address': address[2:].lower(), 'total_liquidity_eth': TotalLiquidityETH, 'total_collateral_eth': TotalCollateralETH, 'total_borrows_eth': TotalBorrowsETH, 'total_fees_eth': TotalFeesETH, 'available_borrows_eth': AvailableBorrowsETH, 'current_liquidation_threshold': CurrentLiquidationThreshold, 'ltv': LoanToValuePercentage, 'health_factor': HealthFactor, 'block_number': block_number, "block_number__Type": "int",'agent_id':0}, 'GET')

def dump_user_reserve_data(coinType, address, Deposited, Borrowed, Debt, RateMode, BorrowRate, LiquidityRate, OriginationFee, BorrowIndex, LastUpdate, IsCollateral, block_number):
    dump_data('set/insert/db_celo_mainnet/tbl_user_reserve', {'coin_name': coin_dict[coinType], 'address': address[2:].lower(), 'deposited': Deposited, 'borrowed': Borrowed, 'debt': Debt, 'rate_mode': RateMode, 'borrow_rate': BorrowRate, 'liquidity_rate': LiquidityRate, 'origination_fee': OriginationFee, 'borrow_index': BorrowIndex, 'is_collateral': IsCollateral, 'is_collateral__Type': 'bool', 'agent_id':0, 'last_update': LastUpdate, 'last_update__Type': 'datetime', 'block_number': block_number, "block_number__Type": "int"}, 'GET')
# , 'last_update': LastUpdate,  'last_update__Type': 'datetime' __Type': 'bool', 
# Past
# def dump_user_activity_data(address, coinType, activityType, amount, amountOfDebtRepaid, liquidation_price_same_currency, liquidation_price_celo_in_cusd, liquidation_price_celo_in_ceuro, liquidation_price_cusd_in_celo, liquidation_price_cusd_in_ceuro, liquidation_price_ceuro_in_celo, liquidation_price_ceuro_in_cusd, tx_hash, timestamp, block_number):
#     dump_data('set/insert/db_celo_mainnet/tbl_user_activity', {'address': address[2:].lower(), 'coin_name': coin_dict[coinType], 'activity_type': activityType, 'amount': amount, 'amount_of_debt_repaid': amountOfDebtRepaid , 'liquidation_price_base': liquidation_price_same_currency, "liquidation_price_celo_in_cusd": liquidation_price_celo_in_cusd, "liquidation_price_celo_in_ceuro": liquidation_price_celo_in_ceuro,"liquidation_price_cusd_in_celo": liquidation_price_cusd_in_celo,"liquidation_price_cusd_in_ceuro": liquidation_price_cusd_in_ceuro,"liquidation_price_ceuro_in_celo": liquidation_price_ceuro_in_celo,"liquidation_price_ceuro_in_cusd": liquidation_price_ceuro_in_cusd, 'tx_hash':tx_hash, 'block_number': block_number, "block_number__Type": "int", 'tx_timestamp': timestamp,  "tx_timestamp__Type": "datetime",  'agent_id':0}, 'GET')

def dump_user_activity_data(address, coinType, claimedCurrency, activityType, amount, amountOfDebtRepaid, healthFactor, liquidation_price_same_currency, tx_hash, timestamp, block_number, origination_fee_in_celo, origination_fee_in_cusd, origination_fee_in_ceur):
    if claimedCurrency == 0:
        dump_data('set/insert/db_celo_mainnet/tbl_user_activity', {'address': address[2:].lower(), 'coin_name': coin_dict[coinType], 'activity_type': activityType, 'amount': amount, 'amount_of_debt_repaid': amountOfDebtRepaid , 'health_factor': healthFactor, 'liquidation_price_base': liquidation_price_same_currency,'tx_hash':tx_hash, 'block_number': block_number, "block_number__Type": "int", 'tx_timestamp': timestamp,  "tx_timestamp__Type": "datetime",  'agent_id':0}, 'GET')
    else:
        dump_data('set/insert/db_celo_mainnet/tbl_user_activity', {'address': address[2:].lower(), 'coin_name': coin_dict[coinType], 'claimed_currency': coin_dict[claimedCurrency], 'activity_type': activityType, 'amount': amount, 'amount_of_debt_repaid': amountOfDebtRepaid , 'health_factor': healthFactor, 'liquidation_price_base': liquidation_price_same_currency,'tx_hash':tx_hash, 'block_number': block_number, "block_number__Type": "int", 'tx_timestamp': timestamp,  "tx_timestamp__Type": "datetime",  'agent_id':0}, 'GET')
    if activityType == 'repay' or activityType == "borrow":
        dump_data('set/insert/db_celo_mainnet/tbl_user_activity_ext_origin_fee', {'activity_type': activityType, 'tx_hash':tx_hash, "origination_fee_in_celo": origination_fee_in_celo , "origination_fee_in_cusd": origination_fee_in_cusd, "origination_fee_in_ceur": origination_fee_in_ceur,'block_number': block_number, "block_number__Type": "int", 'agent_id':0}, 'GET' )

def dump_latest_scanned_block_number(blockNumber):
    dump_data('set/insert/db_celo_mainnet/tbl_block_number', {'block_number': blockNumber, 'agent_id':0}, 'GET')

def dump_coin_exchange_rate(coinName, network, usdExchangeRate, block_number):
    print(coinName, network, usdExchangeRate)
    dump_data('set/insert/db_celo_mainnet/tbl_coin_exchange_rate', {'coin_name': coin_dict[coinName], 'network_name': network, 'usd_exchange_rate':usdExchangeRate,  'agent_id':0, 'block_number': block_number, "block_number__Type": "int"}, 'GET')
