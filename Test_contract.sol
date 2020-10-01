/** 
This is the contract file. There are is a plugin for visual studio code 
for code-highlighting etc.
 */
                pragma solidity ^0.7.0;

                contract Greeter {
                    string public greeting;

                    constructor() public {
                        greeting = 'Hello';
                    }

                    function setGreeting(string memory _greeting) public {
                        greeting = _greeting;
                    }

                    function greet() view public returns (string memory) {
                        return greeting;
                    }
                }
