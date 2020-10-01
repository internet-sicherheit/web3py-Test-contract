#  follow this manual to set up python environement:
#  https://web3py.readthedocs.io/en/stable/quickstart.html

#  Switch to working directory and activate your new virtual environment:
#$ cd /ethereum-network-analysis/web3py/
#$ source ~/.venv-py3/bin/activate
import json

from web3 import Web3
from solc import compile_standard

# importing solidity source code
sol_string = open('Test_contract.sol', "r").read()
print(sol_string)
# compiling source code
compiled_sol = compile_standard(
{
    "language": "Solidity",
    "sources": {
        "Greeter.sol": {
            "content": 
                # solidity
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
#w3 = Web3(Web3.HTTPProvider(httpUrl))
w3 = Web3(Web3.EthereumTesterProvider())
if w3.isConnected():
    print(f'web3.py instance is connected to {httpUrl} (not really atm, but will be after update.)')
else:
    print('no connection')

# set pre-funded accout as sender
w3.eth.defaultAccount = w3.eth.accounts[0]

# get bytecode
bytecode = compiled_sol['contracts']['Greeter.sol']['Greeter']['evm']['bytecode']['object']

# get abi
abi = json.loads(compiled_sol['contracts']['Greeter.sol']['Greeter']['metadata'])['output']['abi']

Greeter = w3.eth.contract(abi=abi, bytecode=bytecode)

# Submit the transaction that deploys the contract
tx_hash = Greeter.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

greeter = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)
print(greeter.functions.greet().call())

tx_hash = greeter.functions.setGreeting('Nihao').transact()
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

print(greeter.functions.greet().call())