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



# HTTPProvider

# TO DO: figure out why this doesnt seem to work on bloxberg
# (probably because of messed up nonces. avoid sending transaction with both 
# metamask and python before previous transactions have been confirmed)
bloxbergUrl = 'https://core.bloxberg.org/'
# 'https://ropsten.infura.io/v3/[infura_project_id]'
ropsten = 'https://ropsten.infura.io/v3/adc98d1ef9ee4662a8f72e3a971a3152'

#w3 = Web3(Web3.EthereumTesterProvider())
w3 = Web3(Web3.HTTPProvider(ropsten))

if w3.isConnected():
    print('\n \n web3.py instance is connected to ' + ropsten + '\n' 
    + 'client version: ' + w3.clientVersion + '\n'
    + 'current blocknumber: ' + str(w3.eth.blockNumber))
    
else:
    print('no connection')
      

# load private account with private key
# private key can be exported from metamask
priv_key = 'INSERT PRIVATE KEY HERE'
metamask_account = w3.eth.account.from_key(priv_key)
# check address, balance and current transaction count (=nonce)
print("" + str(metamask_account.address) + " balance: "+ str(w3.eth.getBalance(metamask_account.address)) + "\n"
+"metamask_account transaction count: " + str(w3.eth.getTransactionCount(metamask_account.address))+ '\n')

# set account as default account.
w3.eth.defaultAccount = str(metamask_account.address)

# regular transaction example
#transaction = {
#    'to': some_account.address, 
#    'value': 10000,
#    'gas': 21001,
#    'gasPrice': w3.toWei('70', 'gwei'),
#    'nonce': 4          
#}

#print( 'failed transaction ' + str(w3.eth.getTransaction('#transaction_hash#)))

# get bytecode
bytecode = compiled_sol['contracts']['Test_contract.sol']['collectionTester']['evm']['bytecode']['object']

# get abi
abi = json.loads(compiled_sol['contracts']['Test_contract.sol']['collectionTester']['metadata'])['output']['abi']

Tester_preDeployment = w3.eth.contract(abi=abi, bytecode=bytecode)
        
# Submit the transaction that deploys the contract 
# note: infura has deactivated the sendTransaction method. instead use sendRawTransaction
transaction = Tester_preDeployment.constructor().buildTransaction()
transaction['nonce'] = w3.eth.getTransactionCount(w3.eth.defaultAccount)

signed = w3.eth.account.signTransaction(transaction, metamask_account.privateKey)

# send the transaction that creates the contract
tx_hash = w3.eth.sendRawTransaction(signed.rawTransaction)
print("Contract Tester deployed; Waiting for transaction receipt...")

tx_receipt = w3.eth.waitForTransactionReceipt(tx_hash)
print(f"Contract Tester deployed to: {tx_receipt.contractAddress}. \n")

tester_postDeployment = w3.eth.contract(
    address=tx_receipt.contractAddress,
    abi=abi
)

transRange = 5
hexNumbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f']
for x in range(transRange):
    # addNumberToArray Method
    addNumberTx = tester_postDeployment.functions.addNumberToArray(x).buildTransaction()    
    addNumberTx['nonce'] = w3.eth.getTransactionCount(w3.eth.defaultAccount)    
    addNumberSigned = w3.eth.account.signTransaction(addNumberTx, metamask_account.privateKey)    
    antx_hash = w3.eth.sendRawTransaction(addNumberSigned.rawTransaction)
    # fire and forget -> no receipt
    #print("Function addNumberToArray called; Waiting for transaction receipt...")
    #tx_receipt = w3.eth.waitForTransactionReceipt(antx_hash)
    #print("Number of Numbers: " + str(tester_postDeployment.functions.howManyNumbers().call()))    

    # addAddress Method
    amount = rand.randint(0, 10)
    address = '0x'
    for y in range(40):
        address = address + rand.choice(hexNumbers)
    print("random Address: " + address + ", amount: " + str(amount) +", current loop: " + str(x))
    address = Web3.toChecksumAddress(address)  
    addAddressTx = tester_postDeployment.functions.addAddress(address, amount).buildTransaction()    
    addAddressTx['nonce'] = w3.eth.getTransactionCount(w3.eth.defaultAccount)    
    addAddressSigned = w3.eth.account.signTransaction(addAddressTx, metamask_account.privateKey)    
    aatx_hash = w3.eth.sendRawTransaction(addAddressSigned.rawTransaction)
    # fire and forget -> no receipt
    #print("Function addAddress called; Waiting for transaction receipt...")
    #tx_receipt = w3.eth.waitForTransactionReceipt(aatx_hash)
    #print("Number of Addresses: " + str(tester_postDeployment.functions.howManyAddresses().call()) + '\n')


