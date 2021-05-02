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
print("Celo mainnet latest block: " + str(celo_mainnet_latest_block))
print(celo_mainnet_lendingPool.address)
print(alfajores_lendingPool.address)
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

def getInEther(num):
    return num/ether

def getInRayRate(num):
    return str(round((num/ray)*100, 2))+'%'

def getInRay(num):
    return num/ray    