from celo_sdk.kit import Kit
import json
import datetime
import string
import call_api
from datetime import datetime as dt
from pycoingecko import CoinGeckoAPI
from web3 import Web3



cg = CoinGeckoAPI()

ray = 1000000000000000000000000000
ether = 1000000000000000000
         
DELAY_IN_SEC = 10 
INTEREST_RATE =[ 'NONE','STABLE','VARIABLE' ]

with open("./abis/LendingPoolAddressesProvider.json") as f:
    Lending_Pool_Addresses_Provider = json.load(f) 
with open("./abis/LendingPool.json") as f:
    Lending_Pool = json.load(f)
with open("./abis/IPriceOracleGetter.json") as f:
    IPrice_Oracle_Getter = json.load(f)         

unique_addresses = []

def getInEther(num):
    return num/ether

def getInRayRate(num):
    return round((num/ray)*100, 2)

def getInRay(num):
    return num/ray    

def get_block_info(block_number):
    w3 = Kit('https://forno.celo.org').w3
    w3.middleware_onion.clear()
    return w3.eth.getBlock(hex(block_number))

def get_latest_block(celo_mainnet_web3): 
    celo_mainnet_web3.middleware_onion.clear()
    blocksLatest = celo_mainnet_web3.eth.getBlock("latest")
    return int(blocksLatest["number"], 16)    

celo_mainnet_kit = Kit('https://forno.celo.org')
celo_mainnet_web3 = celo_mainnet_kit.w3
celo_mainnet_eth = celo_mainnet_web3.eth        
celo_mainnet_address_provider = celo_mainnet_eth.contract(address='0x7AAaD5a5fa74Aec83b74C2a098FBC86E17Ce4aEA', abi=Lending_Pool_Addresses_Provider) 

price_oracle_address = celo_mainnet_address_provider.functions.getPriceOracle().call()

celo_mainnet_address = celo_mainnet_address_provider.functions.getLendingPool().call() 
# print(celo_mainnet_address)
# print(price_oracle_address) 0x568547688121AA69bDEB8aEB662C321c5D7B98D0
celo_mainnet_lendingPool = celo_mainnet_eth.contract(address=celo_mainnet_address, abi= Lending_Pool)
price_oracle = celo_mainnet_eth.contract(address=price_oracle_address, abi= IPrice_Oracle_Getter)
print(price_oracle.functions.getAssetPrice("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE").call()/ether)
helper_w3 = Kit('https://forno.celo.org').w3
celo_mainnet_latest_block = get_latest_block(helper_w3)

w3 = Web3(Web3.HTTPProvider('https://celo-mainnet--rpc.datahub.figment.io/apikey/e05da80c6de7b2f8af3bae0015639f08/'))
lendingPool_contract = w3.eth.contract(address=celo_mainnet_address, abi= Lending_Pool)
print(celo_mainnet_address)
print("Latest scanned block number " + str(celo_mainnet_latest_block))

def get_all_moola_logs(from_block, to_block):
    start = from_block
    # start = 6510004
    # number_of_moola_blocks = 0
    end, moola_logs = start+10000, []
    while end<to_block:
        # print("\n" + str(start)+"-"+str(end))
        event_filter = celo_mainnet_eth.filter({"address": celo_mainnet_lendingPool.address, 'fromBlock':celo_mainnet_web3.toHex(start), 'toBlock': celo_mainnet_web3.toHex(end)})
        current_moola_logs = celo_mainnet_eth.getFilterLogs(event_filter.filter_id)
        moola_logs += current_moola_logs
        # print(len(current_moola_logs))    
        start, end = end+1, end+10000 
    event_filter = celo_mainnet_eth.filter({"address": '0xc1548F5AA1D76CDcAB7385FA6B5cEA70f941e535', 'fromBlock':celo_mainnet_web3.toHex(start), 'toBlock': celo_mainnet_web3.toHex(to_block)})
    current_moola_logs = celo_mainnet_eth.getFilterLogs(event_filter.filter_id)
    moola_logs += current_moola_logs
    print("\nFinal total logs:" + str(len(moola_logs)))
    return moola_logs

def get_coins():
    coins = [{
        'name':"celo", "reserve_address": '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    }, {
        'name':"cusd", "reserve_address": '0x765DE816845861e75A25fCA122bb6898B8B1282a'  
    }, {
        'name':"ceuro", "reserve_address": '0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73'  
    }]
    return coins

def get_lending_pool_reserve_config_data(reserve_address, block_number):
    try: 
        config_data = celo_mainnet_lendingPool.functions.getReserveConfigurationData(reserve_address).call(block_identifier=block_number)
    except:
        config_data = lendingPool_contract.functions.getReserveConfigurationData(reserve_address).call(block_identifier=block_number)
      
    parsed_data = {
        "LoanToValuePercentage": config_data[0],
        "LiquidationThreshold": config_data[1],
        "LiquidationBonus": config_data[2],
        "InterestRateStrategyAddress": config_data[3],
        "UsageAsCollateralEnabled": 1 if config_data[4] else "",
        "BorrowingEnabled": 1 if config_data[5] else "",
        "StableBorrowRateEnabled": 1 if config_data[6] else "",
        "isActive": 1 if config_data[7] else "",
        "blockNumber": block_number
    }
    return parsed_data

def get_lending_pool_reserve_data(reserve_address, block_number):
    lendingPool_contract
    try:
        data = celo_mainnet_lendingPool.functions.getReserveData(reserve_address).call(block_identifier=block_number)
    except:
        data = lendingPool_contract.functions.getReserveData(reserve_address).call(block_identifier=block_number)
    parsed_data = {
            "TotalLiquidity": getInEther(data[0]),
            "AvailableLiquidity": getInEther(data[1]),
            "TotalBorrowsStable": getInEther(data[2]),
            "TotalBorrowsVariable": getInEther(data[3]),
            "LiquidityRate": getInRayRate(data[4]),
            "VariableRate": getInRayRate(data[5]),
            "StableRate": getInRayRate(data[6]),
            "AverageStableRate": getInRayRate(data[7]),
            "UtilizationRate": getInRayRate(data[8]),# Ut
            "LiquidityIndex": getInRay(data[9]),
            "VariableBorrowIndex": getInRay(data[10]),
            "MToken": data[11],
            "LastUpdate": dt.fromtimestamp(data[12]).strftime("%m-%d-%Y %H:%M:%S"),
            "blockNumber": block_number
    }
    return parsed_data

def get_lending_pool_data(block_number):
    coins = get_coins()
    lending_pool_data = []
    for coin in coins:
        # print(coin['name'])
        config_data= get_lending_pool_reserve_config_data(coin['reserve_address'], block_number)
        data = get_lending_pool_reserve_data(coin['reserve_address'], block_number)
        lending_pool_data.append({
            "CoinName": coin['name'],
            "ConfigData": config_data,
            "Data": data 
            
        })
    return lending_pool_data

def get_user_account_data(unique_addresses, block_number):
    all_user_account_data = []
    for address in unique_addresses:
        try:
            user_account_data = celo_mainnet_lendingPool.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress(address)).call(block_identifier=block_number)
        except Exception as e:
            print(e)
            print("Exception for address: " + str(address))
            try:
                user_account_data = lendingPool_contract.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress(address)).call    (block_identifier=block_number)
            except Exception as e:
                print(e)
                print("Exception for address: " + str(address))
                continue
        parsedUserAccountData = {
            "TotalLiquidityETH": getInEther(user_account_data[0]),
            "TotalCollateralETH": getInEther(user_account_data[1]),
            "TotalBorrowsETH": getInEther(user_account_data[2]),
            "TotalFeesETH": getInEther(user_account_data[3]),
            "AvailableBorrowsETH": getInEther(user_account_data[4]),
            "CurrentLiquidationThreshold": user_account_data[5],
            "LoanToValuePercentage": user_account_data[6],
            "HealthFactor": getInEther(user_account_data[7]),
            "blockNumber": block_number
        } 
        all_user_account_data.append({
            "UserAddress": address,
            "UserData": parsedUserAccountData 
        })
    # print("User account data: " + str(len(all_user_account_data)))
    return all_user_account_data

def get_user_reserve_data(unique_addresses, block_number):
    coins = get_coins()
    all_user_reserve_data = []
    for coin in coins:
        reserve_specific_user_reserve_data = {"Coin": coin["name"], "Data":[]}
        for address in unique_addresses:
            try:
                user_reserve_data = celo_mainnet_lendingPool.functions.getUserReserveData(coin['reserve_address'], celo_mainnet_web3.toChecksumAddress(address)).call(block_identifier=block_number)
            except Exception as e:
                print(e)
                print("Exception for address: " + str(address))
                try:
                    user_reserve_data = lendingPool_contract.functions.getUserReserveData(coin['reserve_address'], celo_mainnet_web3.toChecksumAddress(address)).call(block_identifier=block_number)
                except Exception as e:
                    print(e)
                    print("Exception for address: " + str(address))
                    continue
           
            parsed_data = {
                "Deposited": getInEther(user_reserve_data[0]),
                "Borrowed": getInEther(user_reserve_data[1]),
                "Debt": getInEther(user_reserve_data[2]),
                "RateMode": INTEREST_RATE[user_reserve_data[3]],
                "BorrowRate": getInRayRate(user_reserve_data[4]),
                "LiquidityRate": getInRayRate(user_reserve_data[5]),
                "OriginationFee": getInEther(user_reserve_data[6]),
                "BorrowIndex": getInRay(user_reserve_data[7]),
                "LastUpdate": dt.fromtimestamp(user_reserve_data[8]).strftime("%m-%d-%Y %H:%M:%S"),
                "IsCollateral": 1 if user_reserve_data[9] else "", 
                "blockNumber": block_number
            }
            reserve_specific_user_reserve_data["Data"].append({
                "UserAddress": address,
                "UserReserveData": parsed_data
            })
        # print(coin["name"] + " user reserve data: " + str(len(reserve_specific_user_reserve_data["Data"])))   
        all_user_reserve_data.append(reserve_specific_user_reserve_data)
    return all_user_reserve_data

def is_address(address):
    return address.startswith('0x') and len(address) == 42

def get_addresses(from_block, to_block):
    logs = get_all_moola_logs(from_block, to_block)
    all_addresses = []
    tx_hashes = [log['transactionHash'] for log in logs] 
    for tx_hash in tx_hashes:
        receipt = celo_mainnet_eth.getTransactionReceipt(tx_hash)
        if is_address(receipt['from']):
            all_addresses.append(receipt['from'])    
        if is_address(receipt['to']):
            all_addresses.append(receipt['to'])
        current_logs = receipt['logs']
        current_addresses = [log['address'] for log in current_logs]
        all_addresses += current_addresses 
    unique_addresses = list(set(all_addresses))
    return unique_addresses

def store_addresses(log_unique_addresses, fromto_unique_addresses, unique_addresses):
    print("Number of From to unique addresses: " + str(len(fromto_unique_addresses)))    
    print("Number of log unique addresses: " + str(len(log_unique_addresses)))    
    print("Number of unique addresses: " + str(len(unique_addresses)))    
    # file = open("addresses1.txt", "w")
    # file.write("From to:\n")
    # for address in fromto_unique_addresses:
    #     file.write(address+"\n")
    # file.write("\nLog:\n")
    # for address in log_unique_addresses:
    #     file.write(address+"\n")
    # file.close()
    file = open("uniqueAddresses.txt", "w")
    print(len(unique_addresses))
    for address in unique_addresses:
        file.write(address+"\n")
    file.close()
    # addresses = [log['address'] for log in logs] 
    # print(addresses)
    # unique_addresses = list(set(addresses)) 
    # print("Number of unique addresses: " + str(len(unique_addresses)))

def get_adderesses_from_file():
    unique_addresses = [] 
    with open('uniqueAddresses.txt') as f:
        unique_addresses = list(f)
    return [unique_address.strip() for unique_address in unique_addresses]

def store_addresses_with_no_value(addresses_with_no_value):
    with open('addressesWithNoValue.txt', 'w') as file: 
        for address in addresses_with_no_value:
            file.write(address+"\n")

def call_apis_for_lending_pool(all_lending_pool_data):
    # number_of_call = 0
    for lending_pool_data in all_lending_pool_data:
        coin_name = lending_pool_data["CoinName"]
        call_api.dump_reserve_config_data(coin_name, lending_pool_data["ConfigData"]["LoanToValuePercentage"], lending_pool_data["ConfigData"]["LiquidationThreshold"], lending_pool_data["ConfigData"]["LiquidationBonus"], lending_pool_data["ConfigData"]["InterestRateStrategyAddress"], lending_pool_data["ConfigData"]["UsageAsCollateralEnabled"], lending_pool_data["ConfigData"]["BorrowingEnabled"], lending_pool_data["ConfigData"]["StableBorrowRateEnabled"], lending_pool_data["ConfigData"]["isActive"], lending_pool_data["ConfigData"]["blockNumber"]) 
       
        call_api.dump_reserve_data(coin_name, lending_pool_data["Data"]["TotalLiquidity"], lending_pool_data["Data"]["AvailableLiquidity"], lending_pool_data["Data"]["TotalBorrowsStable"], lending_pool_data["Data"]["TotalBorrowsVariable"], lending_pool_data["Data"]["LiquidityRate"], lending_pool_data["Data"]["VariableRate"], lending_pool_data["Data"]["StableRate"], lending_pool_data["Data"]["AverageStableRate"], lending_pool_data["Data"]["UtilizationRate"], lending_pool_data["Data"]["LiquidityIndex"], lending_pool_data["Data"]["VariableBorrowIndex"], lending_pool_data["Data"]["MToken"], lending_pool_data["Data"]["LastUpdate"], lending_pool_data["Data"]["blockNumber"])
        # number_of_call += 2
    # return number_of_call
      

def cal_apis_for_user_account_data(all_user_data):
    # number_of_calls = 0
    for user_data in  all_user_data:
        call_api.dump_user_account_data(user_data["UserAddress"], user_data["UserData"]["TotalLiquidityETH"], user_data["UserData"]["TotalCollateralETH"], user_data["UserData"]["TotalBorrowsETH"], user_data["UserData"]["TotalFeesETH"], user_data["UserData"]["AvailableBorrowsETH"], user_data["UserData"]["CurrentLiquidationThreshold"], user_data["UserData"]["LoanToValuePercentage"], user_data["UserData"]["HealthFactor"], user_data["UserData"]["blockNumber"])
        # number_of_calls += 1
    # return number_of_calls

def cal_apis_for_user_reserve_data(all_user_reserve_data):
    # number_of_calls = 0
    for user_reserve_data in  all_user_reserve_data:
        coin_name = user_reserve_data["Coin"]
        all_data = user_reserve_data["Data"]
        for data in all_data:
            call_api.dump_user_reserve_data(coin_name, data["UserAddress"], data["UserReserveData"]["Deposited"], data["UserReserveData"]["Borrowed"], data["UserReserveData"]["Debt"], data["UserReserveData"]["RateMode"], data["UserReserveData"]["BorrowRate"], data["UserReserveData"]["LiquidityRate"], data["UserReserveData"]["OriginationFee"], data["UserReserveData"]["BorrowIndex"], data["UserReserveData"]["LastUpdate"], data["UserReserveData"]["IsCollateral"], data["UserReserveData"]["blockNumber"])
            # number_of_calls += 1
    # return number_of_calls

def call_apis_for_useractivity_data(user_activities):
    for user_activity in user_activities:
        call_api.dump_user_activity_data(user_activity['address'], user_activity['coinType'], user_activity['activityType'], user_activity['amount'], user_activity['amountOfDebtRepaid'], user_activity["healthFactor"], user_activity['Liquidation_price_same_currency'], user_activity['tx_hash'], user_activity['timestamp'], user_activity['block_number'])
        #  call_api.dump_user_activity_data(user_activity['address'], user_activity['coinType'], user_activity['activityType'], user_activity['amount'], user_activity['amountOfDebtRepaid'], user_activity['Liquidation_price_same_currency'], user_activity['Liquidation_price_celo_in_cusd'], user_activity['Liquidation_price_celo_in_ceuro'], user_activity['Liquidation_price_cusd_in_celo'], user_activity['Liquidation_price_cusd_in_ceuro'], user_activity['Liquidation_price_ceuro_in_celo'], user_activity['Liquidation_price_ceuro_in_cusd'], user_activity['tx_hash'], user_activity['timestamp'], user_activity['block_number'])

def call_apis_for_exchange_rate(block_number):
    coins = get_coins()
    for coin in coins:
        call_api.dump_coin_exchange_rate(coin["name"], 'celo mainnet', get_exchange_rate_in_usd(coin["name"], coin["reserve_address"]), block_number)


def bootstrap():
    # from_block, to_block, number_of_calls = 3410001, celo_mainnet_latest_block, 0   
    # from_block, to_block, number_of_calls = 3410001, 6876412, 0  
    # Last updated: 6876412, 6994224 -> 6994225, 6997440 -> 6997442 -> 7015737 -> 7022115 -> 7040955
    from_block, to_block = 7022131, 7040955
    # celo_mainnet_latest_block = get_latest_block(helper_w3)
    unique_addresses = get_addresses(from_block, to_block)
    print("Number of unique addresses: " +  str(len(unique_addresses)))
    celo_mainnet_latest_block = get_latest_block(helper_w3)  
    if len(unique_addresses) == 0:
        # call_apis_for_exchange_rate(celo_mainnet_latest_block)
        call_api.dump_latest_scanned_block_number(to_block)
        return 
    # unique_addresses = get_adderesses_from_file()
    all_lending_pool_data = get_lending_pool_data(celo_mainnet_latest_block)
    all_user_account_data = get_user_account_data(unique_addresses, celo_mainnet_latest_block)
    all_user_reserve_data = get_user_reserve_data(unique_addresses, celo_mainnet_latest_block)  
    # call_apis_for_exchange_rate(celo_mainnet_latest_block)
    # number_of_calls += 3
    # log_unique_addresses, fromto_unique_addresses, unique_addresses = get_addresses(from_block, to_block)
  
    call_apis_for_lending_pool(all_lending_pool_data)
    # print(all_lending_pool_data[0])
    cal_apis_for_user_account_data(all_user_account_data)
    # print(all_user_account_data[0])
    cal_apis_for_user_reserve_data(all_user_reserve_data)
    # print(all_user_reserve_data[0])
    
    # user_activities = get_user_activity(from_block, to_block)
    # # print(user_activities[0])  
    # # number_of_calls += len(user_activities) 
    # call_apis_for_useractivity_data(user_activities)
    # print("Number of user activities:" + str(len(user_activities)))
    call_api.dump_latest_scanned_block_number(to_block)
    # print("Number of calls: " + str(number_of_calls))

def call_all_apis_for_reserve_and_user_data(from_block, to_block, unique_addresses):
    print("Number of addresses: " + str(len(unique_addresses)))
    all_lending_pool_data = get_lending_pool_data(to_block)
    
    all_user_account_data = get_user_account_data(unique_addresses, to_block)
    all_user_reserve_data = get_user_reserve_data(unique_addresses, to_block)
    call_apis_for_lending_pool(all_lending_pool_data)
    cal_apis_for_user_account_data(all_user_account_data)
    cal_apis_for_user_reserve_data(all_user_reserve_data)
    call_api.dump_latest_scanned_block_number(to_block)
   
def get_latest_block_from_db():
    latest_block = "err"
    try_number = 0
    while latest_block == "err":
        latest_block = call_api.getLastestBlock()
        try_number+=1
        if try_number > 1000:
            raise Exception("Can not retrive the lastest block")
    return latest_block  


def update(latest_block):    
    from_block, to_block = latest_block, latest_block 
    # from_block, to_block = 3410001, celo_mainnet_latest_block
    current_latest_block = get_latest_block(helper_w3)
    while latest_block > current_latest_block:
        # print("Ahead of the celo blockchain")
        # print(latest_block, current_latest_block)
        current_latest_block = get_latest_block(helper_w3)
    unique_addresses = get_addresses(from_block, to_block)
    print("Number of unique addresses " + str(len(unique_addresses)))
    if len(unique_addresses) > 0:
        call_all_apis_for_reserve_and_user_data(from_block, to_block, unique_addresses)
        user_activities = get_user_activity(from_block, to_block)  
        call_apis_for_useractivity_data(user_activities)
        call_api.dump_latest_scanned_block_number(to_block)
    else:
        call_api.dump_latest_scanned_block_number(to_block)

celo_to_usd = cg.get_price(ids='celo', vs_currencies='usd')['celo']['usd']

def get_exchange_rate_in_usd(coin_name, coin_address):
    price_in_celo = (price_oracle.functions.getAssetPrice(coin_address).call()/ether)
    return price_in_celo*celo_to_usd

def get_exchange_rate(coin):
    celo_in_usd = cg.get_price(ids='celo', vs_currencies='usd')['celo']['usd']
    cusd_in_usd = cg.get_price(ids='celo-dollar', vs_currencies='usd')['celo-dollar']['usd']
    ceuro_in_usd = cg.get_price(ids='universal-euro', vs_currencies='usd')['universal-euro']['usd']
    
    if coin.lower() == 'celo':
        return {
            'USD': celo_in_usd,
            'cUSD': celo_in_usd/cusd_in_usd,
            'cEUR': celo_in_usd/ceuro_in_usd
        }
        
    elif coin.lower() == 'cusd':
        return {
            'USD': cusd_in_usd,
            'Celo': cusd_in_usd/celo_in_usd,
            'cEUR': cusd_in_usd/ceuro_in_usd
        }
    elif coin.lower() == 'ceuro':
        return {
            'USD': ceuro_in_usd,
            'cUSD': ceuro_in_usd/cusd_in_usd,
            'Celo': ceuro_in_usd/celo_in_usd
        }
    else:
        return "Unknown coin"


# events = ['Borrow', 'Deposit', 'FlashLoan', 'LiquidationCall', 'OriginationFeeLiquidated', 'RebalanceStableBorrowRate', 'RedeemUnderlying', 'Repay', 'ReserveUsedAsCollateralDisabled', 'ReserveUsedAsCollateralEnabled', 'Swap']
# 
events = {
 'Borrow': 'borrow', 'Deposit': 'deposit', 'LiquidationCall': 'liquidate', 'RedeemUnderlying': 'withdraw', 'Repay': 'repay'
}

# events = { 
#  'Borrow': 'borrow', 'Deposit': 'deposit', 'LiquidationCall': 'liquidate', 'RedeemUnderlying': 'withdraw', 'Repay': 'repay', 'Swap':'swap', 'FlashLoan':'flashLoan', 'OriginationFeeLiquidated':'OriginationFeeLiquidated', 'RebalanceStableBorrowRate': 'RebalanceStableBorrowRate', 'ReserveUsedAsCollateralDisabled': 'ReserveUsedAsCollateralDisabled' , 'ReserveUsedAsCollateralEnabled': 'ReserveUsedAsCollateralEnabled'
# }
coins = {
    '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE': 'celo',
    '0x765DE816845861e75A25fCA122bb6898B8B1282a': 'cusd',
    '0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73': 'ceuro'
}

def get_health_factor(user_pub_key, block):
    try:
        user_account_data = lendingPool_contract.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress(user_pub_key)).call(block_identifier=block)
        total_in_eth = getInEther(user_account_data[1])
        total_in_debt = getInEther(user_account_data[2])
        total_fee =  getInEther(user_account_data[3])
    except Exception as e:
        print("Error:  " + str(e))
        return 0.0
    
    if total_in_eth != 0.0 and total_in_debt+total_fee != 0.0:
        return (total_in_eth*0.8)/(total_in_debt+total_fee)
    if total_in_eth != 0.0 and total_in_debt+total_fee == 0.0:
        return 100.0
    return 0.0

def get_user_activity(from_block, to_block):
    all_event_data, user_activities = {}, []
    number_of_event = 0
    for event in events.keys():
        # start = 3410001
        start = from_block
        specific_event_data = []
        end = start+10000
        while end<to_block:
            event_filter = celo_mainnet_lendingPool.events[event].createFilter(fromBlock=celo_mainnet_web3.toHex(start), toBlock=celo_mainnet_web3.toHex(end))
            specific_event_data += event_filter.get_all_entries()    
            start, end = end+1, end+10000 
        event_filter = celo_mainnet_lendingPool.events[event].createFilter(fromBlock=celo_mainnet_web3.toHex(start), toBlock=celo_mainnet_web3.toHex(to_block))
        specific_event_data += event_filter.get_all_entries()
        Liquidation_price_same_currency = 0.0
        number_of_event += len(specific_event_data)
        if len(specific_event_data) > 0:
            for e in specific_event_data:
                amount =''
                amountOfDebtRepaid = 0
                liquidation_price = 0
                health_factor = 0
                if event == 'LiquidationCall':
                    amount = e['args']['_liquidatedCollateralAmount']
                    amountOfDebtRepaid = e['args']['_purchaseAmount']
                    Liquidation_price_same_currency = get_liquidation_price(e["blockNumber"], e['args']['_user'])
                    # print("liquidation_price: " + str(liquidation_price))
                    health_factor = get_health_factor(e['args']['_user'], e["blockNumber"]-1)
                elif event == 'Repay':
                    amount = e['args']['_amountMinusFees'] + e['args']['_fees']
                    Liquidation_price_same_currency = get_liquidation_price(e["blockNumber"], e['args']['_user'])
                    # print("liquidation_price: " + str(liquidation_price))
                    health_factor = get_health_factor(e['args']['_user'], e["blockNumber"])
                elif event == "Borrow":
                    amount = e['args']['_amount']
                    Liquidation_price_same_currency = get_liquidation_price(e["blockNumber"], e['args']['_user'])
                    # print("liquidation_price: " + str(liquidation_price))
                    health_factor = get_health_factor(e['args']['_user'], e["blockNumber"])
                else:
                    amount = e['args']['_amount']
                    health_factor = get_health_factor(e['args']['_user'], e["blockNumber"])
        
                user_activities.append({
                    'activityType': events[event],
                    'address': e['args']['_user'], 
                    'timestamp': dt.fromtimestamp(e['args']['_timestamp']).strftime("%m-%d-%Y %H:%M:%S"),
                    'coinType': coins[e['args']['_reserve']],
                    'amount': amount/ether,
                    'healthFactor': health_factor,
                    'amountOfDebtRepaid': amountOfDebtRepaid/ether,
                    'Liquidation_price_same_currency': Liquidation_price_same_currency,
                    # 'Liquidation_price_celo_in_cusd': Liquidation_price_celo_in_cusd,
                    # 'Liquidation_price_celo_in_ceuro': Liquidation_price_celo_in_ceuro,
                    # 'Liquidation_price_cusd_in_celo': Liquidation_price_cusd_in_celo,
                    # 'Liquidation_price_cusd_in_ceuro': Liquidation_price_cusd_in_ceuro,
                    # 'Liquidation_price_ceuro_in_celo': Liquidation_price_ceuro_in_celo,
                    # 'Liquidation_price_ceuro_in_cusd': Liquidation_price_ceuro_in_cusd,
                    'tx_hash': str(e['transactionHash'].hex())[2:],
                    "block_number": e['blockNumber']
                })
        # all_event_data[event] = specific_event_data
    # for e in all_event_data:
    #     for data in all_event_data[e]:
    #         print()
    #         print(data)
    return user_activities

coins_reserve_address = {
         "celo": '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE',
         "cusd": '0x765DE816845861e75A25fCA122bb6898B8B1282a' , 
         "ceuro": '0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73'  
}

def get_liquidation_price(block_number, user_pub_key):
    total_in_debt, total_in_eth, total_fee = 0.0, 0.0, 0.0
    print(block_number)
    # try:
    #     data_celo = lendingPool_contract.functions.getUserReserveData('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', w3.toChecksumAddress(user_pub_key)).call(block_identifier=block_number)[0]
    # except Exception as e:
    #     print("celo:  " + str(e))
    # try:
    #     data_cusd = lendingPool_contract.functions.getUserReserveData('0x765DE816845861e75A25fCA122bb6898B8B1282a', w3.toChecksumAddress(user_pub_key)).call(block_identifier=block_number)[0]
    # except Exception as e:
    #     print("cusd:  " + str(e))
    # try:
    #     data_ceuro = lendingPool_contract.functions.getUserReserveData('0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73', w3.toChecksumAddress(user_pub_key)).call(block_identifier=block_number)[0]
    # except Exception as e:
    #     print("ceuro:  " + str(e))
    try:
        user_account_data = lendingPool_contract.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress(user_pub_key)).call(block_identifier=block_number)
        total_in_eth = getInEther(user_account_data[1])
        total_in_debt = getInEther(user_account_data[2])
        total_fee =  getInEther(user_account_data[3])
    except Exception as e:
        print("Error:  " + str(e))
        return 0.0
    
    if total_in_eth == 0.0 or total_in_debt == 0.0:
        return 0.0
    
    # celo_usd, cusd_usd, ceuro_usd = get_exchange_rate_in_usd("celo", coins_reserve_address["celo"]), get_exchange_rate_in_usd("cusd", coins_reserve_address["cusd"]),get_exchange_rate_in_usd("ceuro", coins_reserve_address["ceuro"])
            
    Liquidation_price_celo_in_celo = (total_in_debt+total_fee)/(0.8*total_in_eth)
    # Liquidation_price_celo_in_cusd = Liquidation_price_celo_in_celo * celo_usd / cusd_usd
    # Liquidation_price_celo_in_ceuro = Liquidation_price_celo_in_celo * celo_usd / ceuro_usd
    # Liquidation_price_cusd_in_celo = Liquidation_price_celo_in_celo * cusd_usd / celo_usd
    # Liquidation_price_cusd_in_cusd =
    # Liquidation_price_cusd_in_ceuro = Liquidation_price_celo_in_celo * cusd_usd / ceuro_usd
    # Liquidation_price_ceuro_in_celo = Liquidation_price_celo_in_celo * ceuro_usd / celo_usd
    # Liquidation_price_ceuro_in_cusd = Liquidation_price_celo_in_celo * ceuro_usd / cusd_usd
    # Liquidation_price_ceuro_in_ceuro =
# , Liquidation_price_celo_in_cusd, Liquidation_price_celo_in_ceuro, Liquidation_price_cusd_in_celo, Liquidation_price_cusd_in_ceuro, Liquidation_price_ceuro_in_celo, Liquidation_price_ceuro_in_cusd
    return Liquidation_price_celo_in_celo

def dump_user_data():
    pass

def main():
    # call_api.dump_latest_scanned_block_number(7274594)
    # print(get_block_info(6839625))
    # event_filter = celo_mainnet_eth.filter({"address": celo_mainnet_lendingPool.address, 'fromBlock':celo_mainnet_web3.toHex(6839625), 'toBlock': celo_mainnet_web3.toHex(6839625)})
    # log = celo_mainnet_eth.getFilterLogs(event_filter.filter_id)
    # print(str(log[0]['transactionHash']))
    # receipt = celo_mainnet_eth.getTransactionReceipt("0xbe6077af8b3c57360cff6064046cd344f868476251414c1b5c3aeb24c8e2ba5f")
    # logs = celo_mainnet_lendingPool.events.LiquidationCall().processReceipt(receipt)
    # print(logs)
    # store_addresses()    
    # print(unique_addresses)
    # print(len(unique_addresses))
    # pass
    from_block, to_block = 3410001, celo_mainnet_latest_block
    print(celo_mainnet_latest_block)
    # from_block, to_block = celo_mainnet_latest_block-100000, celo_mainnet_latest_block
    user_activities = get_user_activity(from_block, to_block)  
    call_apis_for_useractivity_data(user_activities)
    
    print(celo_mainnet_latest_block)
    print("Finished...")
    # bootstrap()

    # print(get_user_account_data(["0x5083043abfceadd736a97ce32a71ac7a1386e449"], 7104903))
    # current_block = get_latest_block_from_db()+1
    # print(current_block)
    # # current_block = 7040956
    # while True:
    #     update(current_block)
    #     current_block+=1


    # user_reserve_data_c = celo_mainnet_lendingPool.functions.getUserReserveData('0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE', celo_mainnet_web3.toChecksumAddress('0xFf447b6b29Cc2000afB7125c560E18F4DC109993')).call(block_identifier=6936112)
    # print(user_reserve_data_c[0])
    # user_reserve_data_u = celo_mainnet_lendingPool.functions.getUserReserveData('0x765DE816845861e75A25fCA122bb6898B8B1282a', celo_mainnet_web3.toChecksumAddress('0xFf447b6b29Cc2000afB7125c560E18F4DC109993')).call()
    # print(user_reserve_data_u[0])
    # '0x86dba69d06f87F3FDEef5eDaE2ce63835187FD59 0xc1548F5AA1D76CDcAB7385FA6B5cEA70f941e535
    # 'https://celo-mainnet--rpc.datahub.figment.io/apikey/e05da80c6de7b2f8af3bae0015639f08/'
   
    # lp =get_liquidation_price(6806115, '0x86dba69d06f87F3FDEef5eDaE2ce63835187FD59')
    # print(lp)
    # print((total_in_eth*0.8)/(total_in_eth))
    # user_reserve_data_e = celo_mainnet_lendingPool.functions.getUserReserveData('0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73', celo_mainnet_web3.toChecksumAddress('0xFf447b6b29Cc2000afB7125c560E18F4DC109993')).call()
    # print(user_reserve_data_e[0])
  
    
    # user_data = celo_mainnet_lendingPool.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress('0x851b85aA13193fD3A2987662eeC5dF7e89F25912')).call(block_identifier=celo_mainnet_latest_block)
    # call_api.dump_user_account_data('0x851b85aA13193fD3A2987662eeC5dF7e89F25912', user_data["TotalLiquidityETH"], user_data["TotalCollateralETH"], user_data["TotalBorrowsETH"], user_data["TotalFeesETH"], user_data["AvailableBorrowsETH"], user_data["CurrentLiquidationThreshold"], user_data["LoanToValuePercentage"], user_data["HealthFactor"], user_data["blockNumber"])
    # user_activities = get_user_activity(6842227, 6842227, False)
    # print(celo_mainnet_lendingPool.functions.getReserves().call())
    # block_info = get_block_info(celo_mainnet_latest_block)
    # print(celo_mainnet_latest_block)
    # print(block_info)
    # transactions = block_info["transactions"]
    # number_of_transaction, latest_timestamp, index_latest_tx = len(transactions), 99999999, 0
    # for i in range(number_of_transaction):
    #     latest_timestamp < transactions[i].timeStamp


if __name__=="__main__": 
    start = dt.now()
    print("Start time: "+ start.strftime('"%Y-%m-%d %H:%M:%S"'))
    main()
    end = dt.now()
    print("End time: "+ end.strftime("%Y-%m-%d %H:%M:%S"))
    difference = end - start
    hours, remainder = divmod(difference.seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    print('Time: ' + '{:02}:{:02}:{:02}'.format(int(hours), int(minutes), int(seconds)))


