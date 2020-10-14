# web3py-Test-contract

This mini project is meant to test the limits of smart contracts. Right now
it focusses on upper limits for array-size and mapping-size. The code establishes
a connection to a network (infura ropsten) via HTTP. It then creates and
deploys a contract which has a few very simple functions that allow the contract
creator to add additional elements to a dynamic array and/or to a mapping.

As a last step the program repeatedly calls these functions for a previously
specified number of times and adds elements to both the array and the mapping
in the process.

### Setting up the environment

In order to run the python program it is necessary to follow these steps:

```terminal
# Install pip if it is not available:
$ which pip || curl https://bootstrap.pypa.io/get-pip.py | python

# Install virtualenv if it is not available:
$ which virtualenv || pip install --upgrade virtualenv

# *If* the above command displays an error, you can try installing as root:
$ sudo pip install virtualenv

# Create a virtual environment:
$ virtualenv -p python3 ~/.venv-py3

# Activate your new virtual environment:
$ source ~/.venv-py3/bin/activate

# With virtualenv active, make sure you have the latest packaging tools
$ pip install --upgrade pip setuptools

# Now we can install web3.py...
$ pip install --upgrade web3
```

I also use the the EthereumTesterProvider which can be installed with:  
`pip install -U web3[tester]`  
The EthereumTesterProvider is in use at the moment. ~~So feel free to remove
it from the source code if you don't feel like installing it.~~   
And crucially the [Solidity Compiler](https://solidity.readthedocs.io/en/latest/installing-solidity.html#binary-packages)  
Additional libraries: json, time, random

*all of these need to be installed in the virtual environment.*  

--------------
In order to run the program you need an Ethereum Account which can be easily
created and managed with [Metamask](https://metamask.io/).
Then export your private key from your metamask account and insert it into the
code at `priv_key = 'INSERT PRIVATE KEY HERE'`.   

Lastly I created an Infura Project that provides an URL that the program connects with.
Feel free to create your own [Infura Project](https://infura.io).
Alternatively (in theory) this program should work just fine on bloxberg. For some
reason it does not: The transactions are never confirmed.  
This is probably due to conflicting nonces or transactions that wait for other
transactions to be confirmed. I spent an entire day on trouble-shooting and eventually
gave up.

### Example Output

Right now the output inbetween transactions is deactivated. The program simply
"fires and forgets". This can be changed by removing the hashtags in the loop at
the very bottom of the file (this turns comments into functional code).
To set the number of elements that should be added to the array + mapping, change
transRange     
from `transRange = 5`  
to
`transRange = *desired number*`

And here is an example output:  


![example output](https://github.com/internet-sicherheit/web3py-Test-contract/blob/master/output_smartcontract_test.png "example output")

###### Results
After attempting to run the program on the EthereumTesterProvider with 1.000.000
loop iterations the process got killed after 195326 iterations:

![killed process](https://github.com/internet-sicherheit/web3py-Test-contract/blob/master/killed.png "killed process")

The reason remains unknown at this point in time.
Possible reasons that come to mind:
- the python program ran out of memory
- ~~we discovered the limits of the EVM regarding the size of arrays (unlikely)~~
- ~~we discovered the limits of the EVM regarding the size of mappings (more likely)~~
- ~~something else~~

`journalctl --since yesterday | grep -i -C 5 oom` revealed that the os actually
did shutdown the python process during the test.
Monitoring the memory usage while running showed that the program started of with
roughly 47mb:

![memory initial](https://github.com/internet-sicherheit/web3py-Test-contract/blob/master/memory_1.png "memory initial")

The memory usage increased with sporadic jumps to roughly 72mb after 1000 loop iterations:

![memory later](https://github.com/internet-sicherheit/web3py-Test-contract/blob/master/memory_1000.png "memory later")
