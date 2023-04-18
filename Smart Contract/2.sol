pragma solidity ^0.8.0;

contract Auction {
    address payable public owner;
    uint public desiredPrice;
    uint public auctionPeriod;
    uint public maxPrice;
    address payable public maxPriceOwner;
    mapping(address => uint) public returnPrices;

    event changedMaxPrice(uint changedPrice, address changedPriceOwner);
    event finalBid(uint finalPrice, address finalPriceOwner);

    constructor(uint price, uint period) public {
        owner = payable(msg.sender);
        desiredPrice = price;
        auctionPeriod = block.timestamp + period;
    }

    function bid() public payable {
        require(block.timestamp <= auctionPeriod, "auction time ended");
        require(msg.value > maxPrice, "below the current auction price");

        if (maxPriceOwner != address(0)) {
            returnPrices[maxPriceOwner] += maxPrice;
        }
        
        maxPriceOwner = payable(msg.sender);
        maxPrice = msg.value;

        emit changedMaxPrice(maxPrice, maxPriceOwner);

        if (desiredPrice <= maxPrice) {
            auctionPeriod = block.timestamp;
        }
    }

    function widthdraw() public{
        address payable sender = payable(msg.sender);
        uint amount = returnPrices[sender];
        require(amount > 0, "have no price to return");
        returnPrices[sender] = 0;
        sender.transfer(amount);
    }
    
    function finish() public {
        require(msg.sender == owner, "only owner can run it");
        require(block.timestamp >= auctionPeriod, "auction is not over yet");

        emit finalBid(maxPrice, maxPriceOwner);
        
        owner.transfer(maxPrice);
    }
}