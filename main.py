from celo_sdk.kit import Kit
import json
import datetime
import string
import call_api
from datetime import datetime as dt
from pycoingecko import CoinGeckoAPI

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
    return celo_mainnet_eth.getBlock(hex(block_number))

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
print(celo_mainnet_address)

celo_mainnet_lendingPool = celo_mainnet_eth.contract(address=celo_mainnet_address, abi= Lending_Pool)
price_oracle = celo_mainnet_eth.contract(address=price_oracle_address, abi= IPrice_Oracle_Getter)
print(price_oracle.functions.getAssetPrice("0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE").call()/ether)
celo_mainnet_latest_block = get_latest_block(Kit('https://forno.celo.org').w3)
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

def get_lending_pool_reserve_config_data(reserve_address):
    config_data = celo_mainnet_lendingPool.functions.getReserveConfigurationData(reserve_address).call()
    parsed_data = {
        "LoanToValuePercentage": config_data[0],
        "LiquidationThreshold": config_data[1],
        "LiquidationBonus": config_data[2],
        "InterestRateStrategyAddress": config_data[3],
        "UsageAsCollateralEnabled": 1 if config_data[4] else "",
        "BorrowingEnabled": 1 if config_data[5] else "",
        "StableBorrowRateEnabled": 1 if config_data[6] else "",
        "isActive": 1 if config_data[7] else ""
    }
    return parsed_data

def get_lending_pool_reserve_data(reserve_address):
    data = celo_mainnet_lendingPool.functions.getReserveData(reserve_address).call()
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
            "LastUpdate": dt.fromtimestamp(data[12]).strftime("%m-%d-%Y %H:%M:%S")
    }
    return parsed_data

def get_lending_pool_data():
    coins = get_coins()
    lending_pool_data = []
    for coin in coins:
        # print(coin['name'])
        config_data= get_lending_pool_reserve_config_data(coin['reserve_address'])
        data = get_lending_pool_reserve_data(coin['reserve_address'])
        lending_pool_data.append({
            "CoinName": coin['name'],
            "ConfigData": config_data,
            "Data": data 
            
        })
    return lending_pool_data

def get_user_account_data(unique_addresses):
    all_user_account_data = []
    for address in unique_addresses:
        try:
            user_account_data = celo_mainnet_lendingPool.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress(address)).call()
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
            "HealthFactor": getInEther(user_account_data[7])
        } 
        all_user_account_data.append({
            "UserAddress": address,
            "UserData": parsedUserAccountData 
        })
    # print("User account data: " + str(len(all_user_account_data)))
    return all_user_account_data

def get_user_reserve_data(unique_addresses):
    coins = get_coins()
    all_user_reserve_data = []
    for coin in coins:
        reserve_specific_user_reserve_data = {"Coin": coin["name"], "Data":[]}
        for address in unique_addresses:
            try:
                user_reserve_data = celo_mainnet_lendingPool.functions.getUserReserveData(coin['reserve_address'], celo_mainnet_web3.toChecksumAddress(address)).call()
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
    # print(logs[0])
    # print(celo_mainnet_lendingPool.events.LiquidationCall().getLogs())
    fromto_addresses = []
    log_addresses = []
    tx_hashes = [log['transactionHash'] for log in logs] 
    for tx_hash in tx_hashes:
        receipt = celo_mainnet_eth.getTransactionReceipt(tx_hash)
        if is_address(receipt['from']):
            fromto_addresses.append(receipt['from'])    
        if is_address(receipt['to']):
            fromto_addresses.append(receipt['to'])
        current_logs = receipt['logs']
        current_addresses = [log['address'] for log in current_logs]
        log_addresses += current_addresses
    log_unique_addresses = list(set(log_addresses))    
    fromto_unique_addresses = list(set(fromto_addresses))    
    unique_addresses = list(set(fromto_addresses+log_addresses))
    store_addresses(log_unique_addresses, fromto_unique_addresses, unique_addresses)
    return (log_unique_addresses, fromto_unique_addresses, unique_addresses)

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
    total_calls = 0
    for lending_pool_data in all_lending_pool_data:
        coin_name = lending_pool_data["CoinName"]
        call_api.dump_reserve_config_data(coin_name, lending_pool_data["ConfigData"]["LoanToValuePercentage"], lending_pool_data["ConfigData"]["LiquidationThreshold"], lending_pool_data["ConfigData"]["LiquidationBonus"], lending_pool_data["ConfigData"]["InterestRateStrategyAddress"], lending_pool_data["ConfigData"]["UsageAsCollateralEnabled"], lending_pool_data["ConfigData"]["BorrowingEnabled"], lending_pool_data["ConfigData"]["StableBorrowRateEnabled"], lending_pool_data["ConfigData"]["isActive"]) 
       
        call_api.dump_reserve_data(coin_name, lending_pool_data["Data"]["TotalLiquidity"], lending_pool_data["Data"]["AvailableLiquidity"], lending_pool_data["Data"]["TotalBorrowsStable"], lending_pool_data["Data"]["TotalBorrowsVariable"], lending_pool_data["Data"]["LiquidityRate"], lending_pool_data["Data"]["VariableRate"], lending_pool_data["Data"]["StableRate"], lending_pool_data["Data"]["AverageStableRate"], lending_pool_data["Data"]["UtilizationRate"], lending_pool_data["Data"]["LiquidityIndex"], lending_pool_data["Data"]["VariableBorrowIndex"], lending_pool_data["Data"]["MToken"], lending_pool_data["Data"]["LastUpdate"])
        total_calls+=2
    return total_calls

def cal_apis_for_user_account_data(all_user_data):
    for user_data in  all_user_data:
        call_api.dump_user_account_data(user_data["UserAddress"], user_data["UserData"]["TotalLiquidityETH"], user_data["UserData"]["TotalCollateralETH"], user_data["UserData"]["TotalBorrowsETH"], user_data["UserData"]["TotalFeesETH"], user_data["UserData"]["AvailableBorrowsETH"], user_data["UserData"]["CurrentLiquidationThreshold"], user_data["UserData"]["LoanToValuePercentage"], user_data["UserData"]["HealthFactor"])

def cal_apis_for_user_reserve_data(all_user_reserve_data):
    total_calls = 0
    for user_reserve_data in  all_user_reserve_data:
        coin_name = user_reserve_data["Coin"]
        all_data = user_reserve_data["Data"]
        for data in all_data:
            total_calls += 1
            call_api.dump_user_reserve_data(coin_name, data["UserAddress"], data["UserReserveData"]["Deposited"], data["UserReserveData"]["Borrowed"], data["UserReserveData"]["Debt"], data["UserReserveData"]["RateMode"], data["UserReserveData"]["BorrowRate"], data["UserReserveData"]["LiquidityRate"], data["UserReserveData"]["OriginationFee"], data["UserReserveData"]["BorrowIndex"], data["UserReserveData"]["LastUpdate"], data["UserReserveData"]["IsCollateral"])
    return total_calls

def call_apis_for_useractivity_data(user_activities):
    for user_activity in user_activities:
        call_api.dump_user_activity_data(user_activity['address'], user_activity['coinType'], user_activity['activityType'], user_activity['amount'])

def call_apis_for_exchange_rate():
    coins = get_coins()
    for coin in coins:
        call_api.dump_coin_exchange_rate(coin["name"], 'celo mainnet', get_exchange_rate_in_usd(coin["name"], coin["reserve_address"] ))


def bootstrap():
    number_of_calls = 0
    # # from_block, to_block = 3410001, celo_mainnet_latest_block   
    from_block, to_block = celo_mainnet_latest_block-1000, celo_mainnet_latest_block
    call_apis_for_exchange_rate()
    # log_unique_addresses, fromto_unique_addresses, unique_addresses = get_addresses(from_block, to_block)
    # # unique_addresses = get_adderesses_from_file()
    # # print(len(unique_addresses))
    # all_lending_pool_data = get_lending_pool_data()
    # number_of_calls += call_apis_for_lending_pool(all_lending_pool_data)
    # # print(all_lending_pool_data[0])
    # number_of_calls += len(unique_addresses)
    # call_api.dump_user_addresses(unique_addresses, from_block, to_block)
    # all_user_account_data = get_user_account_data(unique_addresses)
    # number_of_calls += len(all_user_account_data)
    # cal_apis_for_user_account_data(all_user_account_data)
    # # print(all_user_account_data[0])
    # all_user_reserve_data = get_user_reserve_data(unique_addresses)
    # number_of_calls += cal_apis_for_user_reserve_data(all_user_reserve_data)
    # # print(all_user_reserve_data[0])
    # user_activities = get_user_activity(from_block, to_block)
    # # print(user_activities[0])   
    # number_of_calls += len(user_activities)
    # call_apis_for_useractivity_data(user_activities)
    # call_api.dump_latest_scanned_block_number(to_block)
    # print("Number of calls: " + str(number_of_calls+1))

def update():
    number_of_calls = 0
    # from_block, to_block = 6721328, celo_mainnet_latest_block
    from_block, to_block = 3410001, celo_mainnet_latest_block
    log_unique_addresses, fromto_unique_addresses, unique_addresses = get_addresses(from_block, to_block)
    all_lending_pool_data = get_lending_pool_data()
    number_of_calls += call_apis_for_lending_pool(all_lending_pool_data)
    number_of_calls += len(unique_addresses)
    call_api.dump_user_addresses(unique_addresses, from_block, to_block)
    all_user_account_data = get_user_account_data(unique_addresses)
    number_of_calls += len(all_user_account_data)
    cal_apis_for_user_account_data(all_user_account_data)
    all_user_reserve_data = get_user_reserve_data(unique_addresses)
    number_of_calls += cal_apis_for_user_reserve_data(all_user_reserve_data)
    user_activities = get_user_activity(from_block, to_block) 
    number_of_calls += len(user_activities)
    call_apis_for_useractivity_data(user_activities)
    call_api.dump_latest_scanned_block_number(to_block)

def get_exchange_rate_in_usd(coin_name, coin_address):
    price_in_celo = (price_oracle.functions.getAssetPrice(coin_address).call()/ether)
    return price_in_celo*cg.get_price(ids='celo', vs_currencies='usd')['celo']['usd']

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
coins = {
    '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE': 'celo',
    '0x765DE816845861e75A25fCA122bb6898B8B1282a': 'cusd',
    '0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73': 'ceuro'
}

def get_user_activity(from_block, to_block):
    all_event_data, user_activities = {}, []
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
        # print(events[event] + " event:")
        # print(len(specific_event_data))
        if len(specific_event_data) > 0:
            for e in specific_event_data:
                amount =''
                if event == 'LiquidationCall':
                    amount = e['args']['_liquidatedCollateralAmount']
                elif event == 'Repay':
                    amount = e['args']['_amountMinusFees'] + e['args']['_fees']
                else:
                    amount = e['args']['_amount']
                user_activities.append({
                    'activityType': events[event],
                    'address': e['args']['_user'],
                    'coinType': coins[e['args']['_reserve']],
                    'amount': amount,
                })
        all_event_data[event] = specific_event_data
    # for e in all_event_data:
    #     for data in all_event_data[e]:
    #         print()
    #         print(data)
    return user_activities

def main():
    # store_addresses()    
    # print(unique_addresses)
    # print(len(unique_addresses))
    bootstrap()
    # block_info = get_block_info(celo_mainnet_latest_block)
    # print(celo_mainnet_latest_block)
    # print(block_info)
  
    # print(get_gas_price('celo'))
    # print(get_gas_price('cusd'))
    # print(get_gas_price('ceuro'))
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