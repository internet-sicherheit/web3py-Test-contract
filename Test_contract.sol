/** 
This is the contract file. There are is a plugin for visual studio code 
for code-highlighting etc.
 */
                pragma solidity ^0.7.0;

                contract collectionTester {
                    address owner;
                    uint[] public numbers;
                    mapping (address => uint) public accountBalance;
                    address[] public knownAccounts;
                    
                    constructor() public {
                        owner = msg.sender;                        
                    }
                    // syntax variableName[key] = value
                    function addAddress(address adr, uint amount) public {
                        require(msg.sender == owner);
                        accountBalance[adr] = amount;
                        knownAccounts.push(adr);
                        // mappings are not iterable in solidity
                        //accountBalance.push(adr);
                    }
                    function howManyAddresses() view public returns (uint) {
                        return knownAccounts.length;
                    }
                    function addNumberToArray(uint number) public {
                        require(msg.sender == owner);
                        numbers.push(number);
                    }

                    function howManyNumbers() view public returns (uint) {
                        return numbers.length;
                    }
                }
