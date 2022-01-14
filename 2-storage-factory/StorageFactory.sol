// SPDX-License-Identifier: MIT

pragma solidity >=0.7.0 <0.9.0;

import "./SimpleStorage.sol";

// contract StorageFactory is SimpleStorage (Inheritance)
contract StorageFactory {
    SimpleStorage[] public simpleStorageArray;
    
    // Deploy a contract from another contract
    function createSimpleStorageContract() public {
        SimpleStorage simpleStorage = new SimpleStorage();
        simpleStorageArray.push(simpleStorage);
    }
    
    function sfStore(uint256 _simpleStorageIndex, uint256 _simpleStorageNumber) public {
        // To intract with a contract, you need its Address and its ABI (Application Binary interface) - from the import
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        simpleStorage.store(_simpleStorageNumber);
    }
    
    function sfGet(uint256 _simpleStorageIndex) public view returns(uint256) {
        SimpleStorage simpleStorage = SimpleStorage(address(simpleStorageArray[_simpleStorageIndex]));
        return simpleStorage.retrieve();       
    }
}
