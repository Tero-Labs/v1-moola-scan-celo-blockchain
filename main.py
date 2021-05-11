from celo_sdk.kit import Kit
import json
import time, datetime
import string, time
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
unique_addresses = []

def getInEther(num):
    return num/ether

def getInRayRate(num):
    return str(round((num/ray)*100, 2))+'%'

def getInRay(num):
    return num/ray    

def get_block_info(block_number):
    return celo_mainnet_eth.getBlock(hex(block_number))

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
celo_mainnet_lendingPool = celo_mainnet_eth.contract(address=celo_mainnet_address, abi= Lending_Pool)
celo_mainnet_latest_block = get_latest_block(celo_mainnet_web3)
call_api.dump_latest_scanned_block_number(celo_mainnet_latest_block)
print("Latest scanned block number " + str(celo_mainnet_latest_block))
# print("Celo mainnet latest block: " + str(celo_mainnet_latest_block))
print(celo_mainnet_address)
# print(alfajores_lendingPool.address)6450002-6460001
gas_contract = celo_mainnet_kit.base_wrapper.create_and_get_contract_by_name('GasPriceMinimum')


def get_all_moola_logs():
    start = 3410001
    # start = 6510004

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
            "CurrentLiquidationThreshold": str(user_account_data[5]) +'%',
            "LoanToValuePercentage": str(user_account_data[6])+'%',
            "HealthFactor": getInEther(user_account_data[7])
        }
        
        all_user_account_data.append({
            "UserAddress": address,
            "UserData": parsedUserAccountData 
        })
    print("User account data: " + str(len(all_user_account_data)))
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
                "LastUpdate": dt.fromtimestamp(user_reserve_data[8]).strftime("%m/%d/%Y, %H:%M:%S"),
                "IsCollateral": user_reserve_data[9], 
            }
            reserve_specific_user_reserve_data["Data"].append({
                "UserAddress": address,
                "UserReserveData": parsed_data
            })
        print(coin["name"] + " user reserve data: " + str(len(reserve_specific_user_reserve_data["Data"])))   
        all_user_reserve_data.append(reserve_specific_user_reserve_data)
    return all_user_reserve_data

def is_address(address):
    return address.startswith('0x') and len(address) == 42

def get_addresses():
    logs = get_all_moola_logs()
    # print(logs[0])
    # print(celo_mainnet_lendingPool.events.LiquidationCall().getLogs())
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

def call_apis_for_lending_pool(all_lending_pool_data):
    for lending_pool_data in all_lending_pool_data:
        call_api.dump_reserve_config_data(lending_pool_data["CoinName"], lending_pool_data["ConfigData"]["LoanToValuePercentage"], lending_pool_data["ConfigData"]["LiquidationThreshold"], lending_pool_data["ConfigData"]["LiquidationBonus"], lending_pool_data["ConfigData"]["InterestRateStrategyAddress"], lending_pool_data["ConfigData"]["UsageAsCollateralEnabled"], lending_pool_data["ConfigData"]["BorrowingEnabled"], lending_pool_data["ConfigData"]["StableBorrowRateEnabled"], lending_pool_data["ConfigData"]["isActive"]) 
        call_api.dump_reserve_data(lending_pool_data["CoinName"], lending_pool_data["Data"]["TotalLiquidity"], lending_pool_data["Data"]["AvailableLiquidity"], lending_pool_data["Data"]["TotalBorrowsStable"], lending_pool_data["Data"]["TotalBorrowsVariable"], lending_pool_data["Data"]["LiquidityRate"], lending_pool_data["Data"]["VariableRate"], lending_pool_data["Data"]["AverageStableRate"], lending_pool_data["Data"]["UtilizationRate"], lending_pool_data["Data"]["LiquidityIndex"], lending_pool_data["Data"]["VariableBorrowIndex"], lending_pool_data["Data"]["MToken"], lending_pool_data["Data"]["LastUpdate"])

def cal_apis_for_user_account_data(all_user_data):
    for user_data in  all_user_data:
        call_api.dump_user_account_data(user_data["UserAddress"], user_data["UserData"]["TotalLiquidityETH"], user_data["UserData"]["TotalCollateralETH"], user_data["UserData"]["TotalBorrowsETH"], user_data["UserData"]["TotalFeesETH"], user_data["UserData"]["AvailableBorrowsETH"], user_data["UserData"]["CurrentLiquidationThreshold"], user_data["UserData"]["LoanToValuePercentage"], user_data["UserData"]["HealthFactor"])

def cal_apis_for_user_reserve_data(all_user_reserve_data):
    for user_reserve_data in  all_user_reserve_data:
        coin_name = user_reserve_data["Coin"]
        all_data = user_reserve_data["Data"]
        for data in all_data:
            call_api.dump_user_reserve_data(coin_name, data["UserAddress"], data["UserReserveData"]["Deposited"], data["UserReserveData"]["Borrowed"], data["UserReserveData"]["Debt"], data["UserReserveData"]["RateMode"], data["UserReserveData"]["BorrowRate"], data["UserReserveData"]["LiquidityRate"], data["UserReserveData"]["OriginationFee"], data["UserReserveData"]["BorrowIndex"], data["UserReserveData"]["LastUpdate"], data["UserReserveData"]["IsCollateral"])

def call_apis_for_useractivity_data():
    pass

def bootstrap():
    log_unique_addresses, fromto_unique_addresses, unique_addresses = get_addresses()
    all_lending_pool_data = get_lending_pool_data()
    call_apis_for_lending_pool(all_lending_pool_data)
    # print(lending_pool_data)
    call_api.dump_user_addresses(unique_addresses)
    all_user_account_data = get_user_account_data(unique_addresses)
    cal_apis_for_user_account_data(all_user_account_data)
    # print(user_account_data)
    all_user_reserve_data = get_user_reserve_data(unique_addresses)
    cal_apis_for_user_reserve_data(all_user_reserve_data)

def update():
    pass

def get_exchange_rate(coin):
    print("Coin name: " + coin)
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
    elif coin.lower() == 'ceur':
        return {
            'USD': ceuro_in_usd,
            'cUSD': ceuro_in_usd/cusd_in_usd,
            'Celo': ceuro_in_usd/celo_in_usd
        }
    else:
        return "Unknown coin"

w3 = Web3(Web3.HTTPProvider('https://forno.celo.org'))
lnd_contract = w3.eth.contract(address=celo_mainnet_address, abi=Lending_Pool)
events = ['Borrow', 'Deposit', 'FlashLoan', 'LiquidationCall', 'OriginationFeeLiquidated', 'RebalanceStableBorrowRate', 'RedeemUnderlying', 'Repay', 'ReserveUsedAsCollateralDisabled', 'ReserveUsedAsCollateralEnabled', 'Swap']

def get_user_activity():
    all_event_data = {}
    for event in events:
        start = 3410001
        specific_event_data = []
        end = start+10000
        while end<celo_mainnet_latest_block:
            event_filter = lnd_contract.events[event].createFilter(fromBlock=celo_mainnet_web3.toHex(start), toBlock=celo_mainnet_web3.toHex(end))
            specific_event_data += event_filter.get_all_entries()
            start, end = end+1, end+10000 
        event_filter = lnd_contract.events[event].createFilter(fromBlock=celo_mainnet_web3.toHex(start), toBlock=celo_mainnet_web3.toHex(celo_mainnet_latest_block))
        specific_event_data += event_filter.get_all_entries()
        print(event + " event:")
        print(len(specific_event_data))
        if len(specific_event_data) >0:
            print(specific_event_data[0])
        all_event_data[event] = specific_event_data
    return all_event_data

def get_gas_price(coin_name):
    coin_reserve_address = {
        "celo": "0x471EcE3750Da237f93B8E339c536989b8978a438",
        "cusd": celo_mainnet_cUSD.address,
        "ceur": celo_mainnet_cEUR.address
    }
    return gas_contract.get_gas_price_minimum(coin_reserve_address[coin_name.lower()])

def estimate_gas_amount(activity, amount):
    if activity == 'deposit':
        return int(alfajores_lendingPool.functions.deposit(celo_mainnet_cUSD.address, amount, 0).estimateGas({
            'from': '0x011ce5bd73a744b2b5d12265be37250defb5b590', 
        }), 16)
    elif activity == 'borrow':
        return int(alfajores_lendingPool.functions.borrow(celo_mainnet_cUSD.address, amount, 1, 0).estimateGas({
            'from': '0x011ce5bd73a744b2b5d12265be37250defb5b590', 
        }), 16)
    elif activity == 'repay':
        return int(alfajores_lendingPool.functions.repay(celo_mainnet_cEUR.address, amount, alfajores_web3.toChecksumAddress('0x011ce5bd73a744b2b5d12265be37250defb5b590')).estimateGas({
            'from': '0x011ce5bd73a744b2b5d12265be37250defb5b590', 
        }), 16)
    elif activity == 'withdraw':
        return int(alfajores_lendingPool.functions.redeemUnderlying(celo_mainnet_cUSD.address, alfajores_web3.toChecksumAddress('0x011ce5bd73a744b2b5d12265be37250defb5b590'), amount, 0).estimateGas({
            'from': '0x011ce5bd73a744b2b5d12265be37250defb5b590', 
        }), 16)
    
def wei_to_celo(price_in_wei):
    return ((price_in_wei/ether)*cg.get_price(ids='ethereum', vs_currencies='usd')['ethereum']['usd'])/cg.get_price(ids='celo', vs_currencies='usd')['celo']['usd']

def get_fee(activity, amount, coin_name):
    return estimate_gas_amount(activity, amount) * (wei_to_celo(get_gas_price(coin_name)))

def main():
    # store_addresses()    
    # print(unique_addresses)
    # print(len(unique_addresses))
    # bootstrap()
    # block_info = get_block_info(celo_mainnet_latest_block)
    # print(celo_mainnet_latest_block)
    # print(block_info)
    # print(get_fee("deposit", 150, 'celo'))
    # print(get_fee("deposit", 150, 'cusd'))
    # print(get_fee("deposit", 150, 'ceur'))
    # print(get_exchange_rate('Celo'))
    # print(get_exchange_rate('Cusd'))
    # print(get_exchange_rate('Ceur'))
    get_user_activity()   
    # print(get_gas_price('celo'))
    # print(get_gas_price('cusd'))
    # print(get_gas_price('ceur'))
    # transactions = block_info["transactions"]
    # number_of_transaction, latest_timestamp, index_latest_tx = len(transactions), 99999999, 0
    # for i in range(number_of_transaction):
    #     latest_timestamp < transactions[i].timeStamp


if __name__=="__main__": 
    start = time.time()
    main()
    end = time.time()
    print("time: " + str(datetime.timedelta(seconds = end-start)))