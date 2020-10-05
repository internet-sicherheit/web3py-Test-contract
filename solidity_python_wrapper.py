#  follow this manual to set up python environement:
#  https://web3py.readthedocs.io/en/stable/quickstart.html

#  Switch to working directory and activate your new virtual environment:
#$ cd /ethereum-network-analysis/web3py/
#$ source ~/.venv-py3/bin/activate
import json

from web3 import Web3
from solc import compile_standard
import random as rand

# importing solidity source code
sol_string = open('Test_contract.sol', "r").read()
# print contract
#print(sol_string)
# compiling source code
compiled_sol = compile_standard(
{
    "language": "Solidity",
    "sources": {
        "Test_contract.sol": {
            "content": 
                # solidity Test crontract
                sol_string
            
        }
    },
    "settings": {
        
            "outputSelection": {
                "*": {
                    "*": [
                        "metadata", "evm.bytecode"
                        , "evm.bytecode.sourceMap"
                    ]
                }
            }
        
    }
})



# HTTPProvider
httpUrl = 'https://core.bloxberg.org'
w3 = Web3(Web3.EthereumTesterProvider())
#w3 = Web3(Web3.HTTPProvider(httpUrl))    
if w3.isConnected():
    print('web3.py instance is connected to the EthereumTesterProvider. Test environment should'
    + ' be changed to bloxberg asap.')
    #print(f'web3.py instance is connected to {httpUrl} (not really atm, but will be after update.)')
else:
    print('no connection')
      



# set pre-funded accout as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# get bytecode
bytecode = compiled_sol['contracts']['Test_contract.sol']['collectionTester']['evm']['bytecode']['object']

# get abi
abi = json.loads(compiled_sol['contracts']['Test_contract.sol']['collectionTester']['metadata'])['output']['abi']

Tester = w3.eth.contract(abi=abi, bytecode=bytecode)
      



        
# Submit the transaction that deploys the contract
tx_hash = Tester.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tester = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)
# check initial number of numbers (not used atm)
#print(tester.functions.howManyNumbers().call())
transRange = 1
hexNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
for x in range(transRange):
    tx_hash = tester.functions.addNumberToArray(x).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Number of Numbers: " + str(tester.functions.howManyNumbers().call()))


for x in range(transRange):
    amount = rand.randint(0, 10)
    address = '0x'
    for x in range(40):
        address = address + rand.choice(hexNumbers)
    print("random Address: " + address)
    address = Web3.toChecksumAddress(address)    
    tx_hash = tester.functions.addAddress(address, amount).transact()
    tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
    print("Number of Addresses: " + str(tester.functions.howManyAddresses().call()))        
    