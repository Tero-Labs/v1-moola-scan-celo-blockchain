from celo_sdk.kit import Kit
import json

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

def getInEther(num):
    return num/ether

def getInRayRate(num):
    return str(round((num/ray)*100, 2))+'%'

def getInRay(num):
    return num/ray    

def get_latest_block(web3): 
    web3.middleware_onion.clear()
    blocksLatest = web3.eth.getBlock("latest")
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
# print(alfajores_lendingPool.address)
def get_all_moola_logs():
    start = 3410001
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
        'name':"cEUR", "reserve_address": cusd_reserve_address  
    }]
    return coins

def get_lending_pool_reserve_data(reserve_address, lending_pool):
    config_data = lending_pool.functions.getReserveConfigurationData(reserve_address).call()
    data = lending_pool.functions.getReserveData(reserve_address).call()
    parsed_data = {
        "reserveConfigParameter":{
            "LoanToValuePercentage": config_data[0],
            "LiquidationThreshold": config_data[1],
            "LiquidationBonus": config_data[2],
            "InterestRateStrategyAddress": config_data[3],
            "UsageAsCollateralEnabled": config_data[4],
            "BorrowingEnabled": config_data[5],
            "StableBorrowRateEnabled": config_data[6],
            "isActive": config_data[7]
        }, 
        "reservePoolGlobalInfo":{
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
            "LastUpdate": datetime.fromtimestamp(data[12]).strftime("%m/%d/%Y, %H:%M:%S")
        } 
    }
    return parsed_data

def get_lending_pool_data(lending_pool):
    coins = get_coins()
    lending_pool_data = []
    for coin in coins:
        # print(coin['name'])
        data = get_lending_pool_reserve_data(coin['reserve_address'], lending_pool)
        lending_pool_data.append({
            "CoinName": coin['name'],
            "Data": data 
        })
    return lending_pool_data

def get_user_account_data(lending_pool, unique_addresses):
    all_user_account_data = []
    for address in unique_addresses:
        user_account_data = lending_pool.functions.getUserAccountData(web3.toChecksumAddress(address)).call()
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
    return all_user_account_data

def get_user_reserve_data(lending_pool, unique_addresses):
    coins = get_coins()
    all_user_reserve_data = []
    for coin in coins:
        reserve_specific_user_reserve_data = {"Coin": coin["name"], "Data":[]}
        for address in unique_addresses:
            user_reserve_data = lending_pool.functions.getUserReserveData(coin['reserve_address'], web3.toChecksumAddress(address)).call()
            
            parsed_data = {
                "Deposited": getInEther(user_reserve_data[0]),
                "Borrowed": getInEther(user_reserve_data[1]),
                "Debt": getInEther(user_reserve_data[2]),
                "RateMode": INTEREST_RATE[user_reserve_data[3]],
                "BorrowRate": getInRayRate(user_reserve_data[4]),
                "LiquidityRate": getInRayRate(user_reserve_data[5]),
                "OriginationFee": getInEther(user_reserve_data[6]),
                "BorrowIndex": getInRay(user_reserve_data[7]),
                "LastUpdate": datetime.fromtimestamp(user_reserve_data[8]).strftime("%m/%d/%Y, %H:%M:%S"),
                "IsCollateral": user_reserve_data[9], 
            }
           
            reserve_specific_user_reserve_data["Data"].append({
                "UserAddress": address,
                "UserReserveData": parsed_data
            })
        all_user_reserve_data.append(reserve_specific_user_reserve_data)
    return all_user_reserve_data

def main():
    print(celo_mainnet_CELO.address)
    print()
    print()
    print()
    reserves = celo_mainnet_lendingPool.functions.getReserves().call()
    for reserve_address in reserves:
        # print(lending_pool_reserves[reserve_address])
        print(reserve_address)

if __name__=="__main__": 
    main()