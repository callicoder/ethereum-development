// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

// contract is similar to a class in Java
contract SimpleStorage {
    
    // data types
    // state variables
    uint256 public myNumber = 5; // default value 0
    bool myBool = true;
    string myString = "Hello";
    int256 myInt = -10;
    address myAddress = 0x4ae110382de86cfC3ac59c06856DE9CBFB096bba;
    bytes32 myBytes = "cat";
    
    // external, public, internal, private (Default is internal)
    // state changing function calls are transactions
    // that's why making a function call costs a little bit of gas
    function store(uint256 _myNumber) public {
        myNumber = _myNumber;
    }
    
    // View function
    function retrieve() public view returns(uint256) {
        return myNumber;
    }
    
    // pure functions can't access or modify state
    function performComputation(uint256 favoriteNumber) public pure returns(uint256) {
        return favoriteNumber*20000;
    }
    
    // view and pure functions are non-state changing functions (denoted by blue color in remix)
    // public variables automatically are also "view" functions
    // calling these functions don't make a transactions because we're not changing the state.
}
