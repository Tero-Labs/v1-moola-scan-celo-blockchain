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
    CUSD = json.load(f)    
    CEUR = json.load(f)

alfajores_kit = Kit('https://alfajores-forno.celo-testnet.org')
celo_mainnet_kit = Kit('https://forno.celo.org')
alfajores_web3 = alfajores_kit.w3
alfajores_eth = alfajores_web3.eth
celo_mainnet_web3 = celo_mainnet_kit.w3
celo_mainnet_eth = celo_mainnet_web3.eth        

alfajores_address_provider = alfajores_eth.contract(address='0x6EAE47ccEFF3c3Ac94971704ccd25C7820121483', abi=Lending_Pool_Addresses_Provider) 
celo_mainnet_address_provider = celo_mainnet_eth.contract(address='0x7AAaD5a5fa74Aec83b74C2a098FBC86E17Ce4aEA', abi=Lending_Pool_Addresses_Provider) 
alfajores_cEUR = alfajores_eth.contract(address='0x10c892a6ec43a53e45d0b916b4b7d383b1b78c0f', abi=CEUR)
alfajores_cUSD = alfajores_eth.contract(address='0x874069Fa1Eb16D44d622F2e0Ca25eeA172369bC1', abi=CUSD)
alfajores_CELO = alfajores_eth.contract(address='0xF194afDf50B03e69Bd7D057c1Aa9e10c9954E4C9', abi=CELO_Token)
celo_mainnet_cEUR = celo_mainnet_eth.contract(address='0xD8763CBa276a3738E6DE85b4b3bF5FDed6D6cA73', abi=CEUR)
celo_mainnet_cUSD = celo_mainnet_eth.contract(address='0x765DE816845861e75A25fCA122bb6898B8B1282a', abi=CUSD)
celo_mainnet_CELO = celo_mainnet_eth.contract(address='0x471EcE3750Da237f93B8E339c536989b8978a438', abi=CELO_Token)
alfajores_address = alfajores_address_provider.functions.getLendingPool().call()
celo_mainnet_address = celo_mainnet_address_provider.functions.getLendingPool().call() 
alfajores_lendingPool = eth.contract(address= alfajores_address, abi= Lending_Pool) 
celo_mainnet_lendingPool = eth.contract(address= celo_mainnet_address, abi= Lending_Pool)

def getInEther(num):
    return num/ether

def getInRayRate(num):
    return str(round((num/ray)*100, 2))+'%'

def getInRay(num):
    return num/ray    
