// SPDX-License-Identifier: GPL-3.0

pragma solidity >=0.7.0 <0.9.0;

// Interfaces compile down to an ABI. It tells solidity what functions can be called on the contract
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// OpenZeppelin => import SafeMath or (import "@chainlink/contracts/src/v0.6/vendor/SafeMathChainlink.sol")
// Not needed from Solidity 0.0.8

// This contract should be able to accept some type of payment (Payable)
contract FundMe {

    AggregatorV3Interface internal priceFeed;
    address public owner;

    /**
     * Network: Kovan
     * Aggregator: ETH/USD
     * Address: 0x9326BFA02ADD2366b30bacB125260Af641031331
     */
    constructor() {
        // Find the address of where this contract is located (https://docs.chain.link/docs/ethereum-addresses/) (Kovan testnet)
        priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);

        // The one who deploys this smart contract
        owner = msg.sender;
    }

    mapping (address => uint256) public addressToAmountFunded; 
    address[] public funders; // no way to loop through a mapping that's why we have an array of funders

    function fund() public payable {
        uint256 minimumUSD = 50 * 10 ** 18; // Minimum $50

        require(getConversionRate(msg.value) >= minimumUSD, "You need to spend more Eth");

        // The sender and value are the keywords in every transaction message
        // msg.sender is the sender of the function call and msg.value is the value they sent
        addressToAmountFunded[msg.sender] += msg.value;
        funders.push(msg.sender); // When somebody funds multiple times, the funders array will have duplicates

        // What the ETH => USD conversion rates
        // Enter chainlink -> Modular decentralized oracle network that allows us to get data and do external computations
        // chainlink has data feeds or price feeds data.chain.link/eth-usd
        // https://docs.chain.link/docs/consuming-data-feeds/
    }

    function getVersion() public view returns(uint256) {
        // Invoke another contract
        return priceFeed.version();
    }

    function getPrice() public view returns(uint256) {
        (,int256 price,,,) = priceFeed.latestRoundData();

        // Ex price => 333315818475 => 3333.15818475 (1ETH = 3333.15818475 USD)
        // Watch out for unchecked integer overflow in versions lower than 0.0.8
        return uint256(price * 10**10); // Convert to lowest decimal (Wei is 10^18), Price is returned in 10^8. So we multiplied by 10^10
    }

    function getConversionRate(uint256 ethAmount) public view returns (uint256) {
        uint256 ethPrice = getPrice();
        uint256 ethAmountInUSD = (ethAmount * ethPrice) / 10**18; // (Divide by 10^18 because ethPrice has an additional 10^18 in it)
        return ethAmountInUSD; 
    }

    modifier onlyOwner {
        // only want the contract owner or admin

        require(msg.sender == owner); // first run the require
        _; // then run the rest of the code in the function
    }

    // Modifiers are used to change the behaviour of a function in a declarative way
    function withdraw() payable onlyOwner public {
        payable(msg.sender).transfer(address(this).balance);
        for(uint256 funderIdx = 0; funderIdx < funders.length; funderIdx++) {
            address funder = funders[funderIdx];
            addressToAmountFunded[funder] = 0;
        }

        funders = new address[](0);
    }
}