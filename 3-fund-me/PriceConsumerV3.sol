// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

// npm package "@chainlink/contracts" (https://www.npmjs.com/package/@chainlink/contracts)
import "@chainlink/contracts/src/v0.8/interfaces/AggregatorV3Interface.sol";

// Requires Environment Web3 (There are no chainlink nodes on simulated Javascript VMs)
// We can also mock a chailink node returning data onto our blockchain
contract PriceConsumerV3 {

    AggregatorV3Interface internal priceFeed;

    /**
     * Network: Kovan
     * Aggregator: ETH/USD
     * Address: 0x9326BFA02ADD2366b30bacB125260Af641031331
     */
    constructor() {
        priceFeed = AggregatorV3Interface(0x9326BFA02ADD2366b30bacB125260Af641031331);
    }

    /**
     * Returns the latest price
     */
    function getLatestPrice() public view returns (int) {
        (
            uint80 roundID, 
            int price,
            uint startedAt,
            uint timeStamp,
            uint80 answeredInRound
        ) = priceFeed.latestRoundData();
        return price;
    }

    // price returned is in P * 10^8
    // Ex: 333315818475 = 3333.15818475
}