#  follow this manual to set up python environement:
#  https://web3py.readthedocs.io/en/stable/quickstart.html

#  Switch to working directory and activate your new virtual environment:
#$ cd /ethereum-network-analysis/web3py/
#$ source ~/.venv-py3/bin/activate

import json
import time
import random as rand

from solc import compile_standard
from web3 import Web3

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



w3 = Web3(Web3.EthereumTesterProvider())


if w3.isConnected():
    print('\n \n web3.py instance is connected to EthereumTesterProvider \n' 
    + 'client version: ' + w3.clientVersion + '\n'
    )
    
else:
    print('no connection')
      

working_account = w3.eth.accounts[0]
# check address, balance and current transaction count (=nonce)
print("" + str(working_account) + " balance: "+ str(w3.eth.getBalance(working_account)) + "\n"
+"metamask_account transaction count: " + str(w3.eth.getTransactionCount(working_account))+ '\n')

# set account as default account.
w3.eth.defaultAccount = str(working_account)

# get bytecode
bytecode = compiled_sol['contracts']['Test_contract.sol']['collectionTester']['evm']['bytecode']['object']

# get abi
abi = json.loads(compiled_sol['contracts']['Test_contract.sol']['collectionTester']['metadata'])['output']['abi']

Tester_preDeployment = w3.eth.contract(abi=abi, bytecode=bytecode)

tx_hash = Tester_preDeployment.constructor().transact()

# Wait for the transaction to be mined, and get the transaction receipt
tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)

tester_postDeployment = w3.eth.contract(
     address=tx_receipt.contractAddress,
     abi=abi
)

transRange = 1000000
hexNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
for x in range(transRange):
    # addNumberToArray Method
    addNumberTx_hash = tester_postDeployment.functions.addNumberToArray(x).transact()
    # deactivate for excessive testing
    #tx_receipt = w3.eth.waitForTransactionReceipt(addNumberTx_hash)
    #print("Number of Numbers: " + str(tester_postDeployment.functions.howManyNumbers().call()))    
     

    # addAddress Method
    amount = rand.randint(0, 10)
    address = '0x'
    for y in range(40):
        address = address + rand.choice(hexNumbers)
    print("random Address: " + address + ", random amount: " + str(amount) +", current loop: " + str(x))
    address = Web3.toChecksumAddress(address)  
    addAddressTx_hash = tester_postDeployment.functions.addAddress(address, amount).transact()
    # deactivate for excessive testing
    #tx_receipt = w3.eth.waitForTransactionReceipt(addAddressTx_hash)
    #print("Number of Addresses: " + str(tester_postDeployment.functions.howManyAddresses().call()) + '\n')


