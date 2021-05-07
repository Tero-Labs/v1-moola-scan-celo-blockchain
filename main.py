from celo_sdk.kit import Kit
import json
import time, datetime
import string, time
import call_api
from datetime import datetime as dt
import collections

ray = 1000000000000000000000000000
ether = 1000000000000000000
DELAY_IN_SEC = 10 
INTEREST_RATE =[ 'NONE','STABLE','VARIABLE' ]

with open("./abis/LendingPoolAddressesProvider.json") as f:
    Lending_Pool_Addresses_Provider = json.load(f) 
with open("./abis/LendingPool.json") as f:
    Lending_Pool = json.load(f)
with open("./abis/AToken.json") as f:
    CELO_Token = json.load(f)
with open("./abis/AToken.json") as f:
    CUSD = json.load(f)
with open("./abis/AToken.json") as f:
    CEUR = json.load(f)        
# with open("./abis/LendingPoolCore.json") as f:
#     Lending_Pool_Core = json.load(f)  
# with open("./abis/LendingPoolDataProvider.json") as f:
#     Lending_Pool_Data_Provider = json.load(f)      


def getInEther(num):
    return num/ether

def getInRayRate(num):
    return str(round((num/ray)*100, 2))+'%'

def getInRay(num):
    return num/ray    

def get_latest_block(celo_mainnet_web3): 
    celo_mainnet_web3.middleware_onion.clear()
    blocksLatest = celo_mainnet_web3.eth.getBlock("latest")
    return int(blocksLatest["number"], 16)    

alfajores_kit = Kit('https://alfajores-forno.celo-testnet.org')
celo_mainnet_kit = Kit('https://forno.celo.org')
alfajores_web3 = alfajores_kit.w3
alfajores_eth = alfajores_web3.eth
celo_mainnet_web3 = celo_mainnet_kit.w3
celo_mainnet_eth = celo_mainnet_web3.eth        

alfajores_address_provider = alfajores_eth.contract(address='0x6EAE47ccEFF3c3Ac94971704ccd25C7820121483', abi=Lending_Pool_Addresses_Provider) 
celo_mainnet_address_provider = celo_mainnet_eth.contract(address='0x7AAaD5a5fa74Aec83b74C2a098FBC86E17Ce4aEA', abi=Lending_Pool_Addresses_Provider) 
alfajores_cEUR = alfajores_eth.contract(address=alfajores_web3.toChecksumAddress('0x10c892a6ec43a53e45d0b916b4b7d383b1b78c0f'), abi=CEUR)
alfajores_cUSD = alfajores_eth.contract(address=alfajores_web3.toChecksumAddress('0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1'), abi=CUSD)
alfajores_CELO = alfajores_eth.contract(address=alfajores_web3.toChecksumAddress('0xF194afDf50B03e69Bd7D057c1Aa9e10c9954E4C9'), abi=CELO_Token)
celo_mainnet_cEUR = celo_mainnet_eth.contract(address='0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73', abi=CEUR)
celo_mainnet_cUSD = celo_mainnet_eth.contract(address='0x765DE816845861e75A25fCA122bb6898B8B1282a', abi=CUSD)
celo_mainnet_CELO = celo_mainnet_eth.contract(address='0x471EcE3750Da237f93B8E339c536989b8978a438', abi=CELO_Token)
alfajores_address = alfajores_address_provider.functions.getLendingPool().call()
celo_mainnet_address = celo_mainnet_address_provider.functions.getLendingPool().call() 
alfajores_lendingPool = celo_mainnet_eth.contract(address= alfajores_address, abi= Lending_Pool) 
celo_mainnet_lendingPool = celo_mainnet_eth.contract(address= celo_mainnet_address, abi= Lending_Pool)
celo_mainnet_latest_block = get_latest_block(celo_mainnet_web3)
# print("Celo mainnet latest block: " + str(celo_mainnet_latest_block))
# print(celo_mainnet_lendingPool.address)
# print(alfajores_lendingPool.address)6450002-6460001


def get_all_moola_logs():
    # start = 3410001
    start = 6490004
    end, moola_logs = start+10000, []
    while end<celo_mainnet_latest_block:
        print("\n" + str(start)+"-"+str(end))
        event_filter = celo_mainnet_eth.filter({"address": celo_mainnet_lendingPool.address, 'fromBlock':celo_mainnet_web3.toHex(start), 'toBlock': celo_mainnet_web3.toHex(end)})
        current_moola_logs = celo_mainnet_eth.getFilterLogs(event_filter.filter_id)
        moola_logs += current_moola_logs
        print(len(current_moola_logs))    
        start, end = end+1, end+10000 
    event_filter = celo_mainnet_eth.filter({"address": celo_mainnet_lendingPool.address, 'fromBlock':celo_mainnet_web3.toHex(start), 'toBlock': celo_mainnet_web3.toHex(celo_mainnet_latest_block)})
    current_moola_logs = celo_mainnet_eth.getFilterLogs(event_filter.filter_id)
    moola_logs += current_moola_logs
    print("\nFinal total logs:" + str(len(moola_logs)))
    return moola_logs

def get_coins():
    celo_reserve_address = '0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeEEeE'
    cusd_reserve_address = celo_mainnet_cUSD.address
    ceur_reserve_address = celo_mainnet_cEUR.address
    coins = [{
        'name':"Celo", "reserve_address": celo_reserve_address
    }, {
        'name':"cUSD", "reserve_address": cusd_reserve_address  
    }, {
        'name':"cEUR", "reserve_address": ceur_reserve_address  
    }]
    return coins

def get_lending_pool_reserve_config_data(reserve_address):
    config_data = celo_mainnet_lendingPool.functions.getReserveConfigurationData(reserve_address).call()
    parsed_data = {
        "LoanToValuePercentage": config_data[0],
        "LiquidationThreshold": config_data[1],
        "LiquidationBonus": config_data[2],
        "InterestRateStrategyAddress": config_data[3],
        "UsageAsCollateralEnabled": config_data[4],
        "BorrowingEnabled": config_data[5],
        "StableBorrowRateEnabled": config_data[6],
        "isActive": config_data[7]
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
            "LastUpdate": dt.fromtimestamp(data[12]).strftime("%m/%d/%Y, %H:%M:%S")
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
    no_value_addresses = []
    for address in unique_addresses:
        try:
            user_account_data = celo_mainnet_lendingPool.functions.getUserAccountData(celo_mainnet_web3.toChecksumAddress(address)).call()
        except Exception as e:
            print(e)
            print("Exception for address: " + address)
            continue
        parsedUserAccountData = {
            "TotalLiquidityETH": getInEther(user_account_data[0]),
            "TotalCollateralETH": getInEther(user_account_data[1]),
            "TotalBorrowsETH": getInEther(user_account_data[2]),
            "TotalFeesETH": getInEther(user_account_data[3]),
            "AvailableBorrowsETH": getInEther(user_account_data[4]),
            "CurrentLiquidationThreshold": str(user_account_data[5]) +'%',
            "LoanToValuePercentage": str(user_account_data[6])+'%',
            "HealthFactor": getInEther(user_account_data[7])
        }
        if parsedUserAccountData["TotalLiquidityETH"] == 0.0 and parsedUserAccountData["TotalCollateralETH"] == 0.0 and parsedUserAccountData["TotalBorrowsETH"] == 0.0 and parsedUserAccountData["TotalFeesETH"] == 0.0 and parsedUserAccountData["CurrentLiquidationThreshold"] == '0%' and parsedUserAccountData["LoanToValuePercentage"] == '0%':
            no_value_addresses.append(address)
        all_user_account_data.append({
            "UserAddress": address,
            "UserData": parsedUserAccountData 
        })
    print("User account data: " + str(len(all_user_account_data)))
    print("No value addresses: ")
    print(len(no_value_addresses))
    # print(no_value_addresses)
    return all_user_account_data, no_value_addresses

def get_user_reserve_data(unique_addresses):
    coins = get_coins()
    all_user_reserve_data = []
    all_no_value_addresses = []
    for coin in coins:
        reserve_specific_user_reserve_data = {"Coin": coin["name"], "Data":[]}
        no_value_addresses = []
        for address in unique_addresses:
            try:
                user_reserve_data = celo_mainnet_lendingPool.functions.getUserReserveData(coin['reserve_address'], celo_mainnet_web3.toChecksumAddress(address)).call()
            except Exception as e:
                print(e)
                print("Exception for address: " + address)
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
                "LastUpdate": dt.fromtimestamp(user_reserve_data[8]).strftime("%m/%d/%Y, %H:%M:%S"),
                "IsCollateral": user_reserve_data[9], 
            }
            if parsed_data["Deposited"] == 0.0 and parsed_data["Borrowed"] == 0.0 and parsed_data["Debt"] == 0.0 and parsed_data["OriginationFee"] == 0.0 and parsed_data["BorrowIndex"] == 0.0 and parsed_data["BorrowRate"] == '0.0%':
                no_value_addresses.append(address)
                
            reserve_specific_user_reserve_data["Data"].append({
                "UserAddress": address,
                "UserReserveData": parsed_data
            })
        print(coin["name"] + " user reserve data: " + str(len(reserve_specific_user_reserve_data["Data"])))
        print(coin["name"] +  " no value addresses: ")
        print(len(no_value_addresses))
        all_no_value_addresses.append(no_value_addresses)
        # print(no_value_addresses)
        all_user_reserve_data.append(reserve_specific_user_reserve_data)
    common_no_value_addresses =list(set(all_no_value_addresses[0]) & set(all_no_value_addresses[1]) & set(all_no_value_addresses[2]))
   
    print("All no value addresses: ")    
    print(len(common_no_value_addresses))
    # print(common_no_value_addresses)
    return (all_user_reserve_data, common_no_value_addresses)

def is_address(address):
    return address.startswith('0x') and len(address) == 42

def get_addresses():
    logs = get_all_moola_logs()
    print(logs[0])
    print(celo_mainnet_lendingPool.events.LiquidationCall().getLogs())
    fromto_addresses = []
    log_addresses = []
    tx_hashes = [log['transactionHash'] for log in logs] 
    # print(tx_hashes)
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
    return (log_unique_addresses, fromto_unique_addresses, unique_addresses)

def store_addresses():
    log_unique_addresses, fromto_unique_addresses, unique_addresses = get_addresses()
    print("Number of From to unique addresses: " + str(len(fromto_unique_addresses)))    
    print("Number of log unique addresses: " + str(len(log_unique_addresses)))    
    print("Number of log unique addresses: " + str(len(unique_addresses)))    

    file = open("addresses1.txt", "w")
    file.write("From to:\n")
    for address in fromto_unique_addresses:
        file.write(address+"\n")
    file.write("\nLog:\n")
    for address in log_unique_addresses:
        file.write(address+"\n")
    file.close()

    file = open("uniqueAddresses1.txt", "w")
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

def bootstrap(unique_addresses):
    # lending_pool_data = get_lending_pool_data()
    # print(lending_pool_data)
    user_account_data, user_account_no_value_addresses = get_user_account_data(unique_addresses)
    # print(user_account_data)
    user_reserve_data, user_reserve_no_value_addresses = get_user_reserve_data(unique_addresses)
    print("___")
    print(len(user_account_no_value_addresses))
    print(len(user_reserve_no_value_addresses))
    print(collections.Counter(user_account_no_value_addresses) == collections.Counter(user_reserve_no_value_addresses))
    store_addresses_with_no_value(user_account_no_value_addresses)
    # common_no_value_address = list(set(user_account_no_value_addresses).intersection(set(user_reserve_no_value_addresses)))
    # all_no_value_address = list(set(user_account_no_value_addresses).union(set(user_reserve_no_value_addresses)))
    # print(len(all_no_value_address))
    # print(len(common_no_value_address))
    # print(user_reserve_data)

def update():
    pass

def main():
    # store_addresses()
    unique_addresses = get_adderesses_from_file()
    # print(unique_addresses)
    print(len(unique_addresses))
    # call_api.hello()
    bootstrap(unique_addresses)

if __name__=="__main__": 
    start = time.time()
    main()
    end = time.time()
    print("time: " + str(datetime.timedelta(seconds = end-start)))